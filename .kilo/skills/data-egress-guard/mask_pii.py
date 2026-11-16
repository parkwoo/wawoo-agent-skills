#!/usr/bin/env python3
"""data-egress-guard: deterministic PII / secret masking before outbound calls.

No model, no network, standard library only. Replaces detected spans with
numbered placeholders (e.g. ``{{EMAIL_1}}``) and keeps a reversible map so a
provider response can be rehydrated. Rules are data-driven; optional checksums
(Luhn / IBAN mod-97) reduce false positives in ``--strict`` mode.

Privacy-first default: mask on format match even if a checksum fails (a missed
mask leaks; a rare extra mask only over-redacts). Use ``--strict`` to require
valid checksums.

CLI:
  echo "mail a@b.com card 4111 1111 1111 1111" | python3 mask_pii.py
  python3 mask_pii.py --input text.txt --locale generic,jp --json
  python3 mask_pii.py --selftest

Library:
  from mask_pii import PiiMasker
  m = PiiMasker(locales=["generic", "jp"])
  res = m.mask(text)          # {"text", "mapping", "counts"}
  m.unmask(res["text"], res["mapping"])
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Iterable


# --- checksums ---------------------------------------------------------------
def _luhn_ok(digits: str) -> bool:
    digits = re.sub(r"\D", "", digits)
    if len(digits) < 12:
        return False
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = ord(ch) - 48
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def _iban_ok(value: str) -> bool:
    s = re.sub(r"\s+", "", value).upper()
    if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]{10,30}$", s):
        return False
    rearranged = s[4:] + s[:4]
    digits = "".join(str(int(ch, 36)) for ch in rearranged)
    return int(digits) % 97 == 1


def _jp_mynumber_ok(digits: str) -> bool:
    d = re.sub(r"\D", "", digits)
    if len(d) != 12:
        return False
    total = 0
    for n in range(1, 12):
        p = n + 1 if n <= 6 else n - 5
        total += p * int(d[11 - n])
    check = 11 - (total % 11)
    if check >= 10:
        check = 0
    return check == int(d[11])


def _jp_corporate_ok(digits: str) -> bool:
    d = re.sub(r"\D", "", digits)
    if len(d) != 13:
        return False
    total = 0
    for i, ch in enumerate(d[1:]):
        weight = 1 if i % 2 == 0 else 2
        total += weight * int(ch)
    check = 9 - (total % 9)
    return check == int(d[0])


# --- rules -------------------------------------------------------------------
@dataclass
class Rule:
    name: str
    placeholder: str
    pattern: re.Pattern[str]
    locales: tuple[str, ...] = ("generic",)
    validator: Callable[[str], bool] | None = None
    group: int = 0


def _r(name: str, placeholder: str, pattern: str, locales=("generic",), validator=None) -> Rule:
    return Rule(name, placeholder, re.compile(pattern), locales=locales, validator=validator)


RULES: list[Rule] = [
    _r("PRIVATE_KEY", "PRIVATE_KEY", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    _r("JWT", "JWT", r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    _r("GITHUB_TOKEN", "GITHUB_TOKEN", r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    _r("AWS_KEY", "AWS_KEY", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    _r("API_KEY", "API_KEY", r"\b(?:sk-[A-Za-z0-9]{16,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{20,})\b"),
    _r("BEARER", "BEARER", r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}", validator=None),
    _r("IBAN", "IBAN", r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){10,30}\b", validator=_iban_ok),
    _r("CREDIT_CARD", "CARD", r"\b(?:\d[ -]?){12,18}\d\b", validator=_luhn_ok),
    _r("EMAIL", "EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    _r("IPV6", "IPV6", r"\b(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}\b"),
    _r("IPV4", "IPV4", r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    _r("MAC", "MAC", r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b"),
    _r("URL", "URL", r"\bhttps?://[^\s<>\"')]+"),
    # Japan-specific (format strong; checksums in strict mode)
    _r("JP_MYNUMBER", "MYNUMBER", r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b", locales=("jp",), validator=_jp_mynumber_ok),
    _r("JP_CORPORATE", "CORPORATE_NUMBER", r"\b\d{13}\b", locales=("jp",), validator=_jp_corporate_ok),
    _r("JP_PHONE", "PHONE", r"\b0\d{1,4}-\d{1,4}-\d{3,4}\b", locales=("jp",)),
    _r("JP_POSTAL", "POSTAL", r"\b\d{3}-\d{4}\b", locales=("jp",)),
    # generic phone: require a country code or separators to limit false positives
    _r("PHONE", "PHONE", r"(?<![\w-])\+\d{1,3}[ -]?\d{6,14}(?![\w-])"),
]


@dataclass
class MaskResult:
    text: str
    mapping: dict[str, str] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"text": self.text, "mapping": self.mapping, "counts": self.counts}


class PiiMasker:
    def __init__(self, locales: Iterable[str] = ("generic",), rules: Iterable[str] | None = None, strict: bool = False):
        wanted = [r.strip().lower() for r in locales if r and r.strip()]
        if "generic" not in wanted:
            wanted.append("generic")
        allow = {r.strip().upper() for r in rules} if rules else None
        self.rules = [
            rule for rule in RULES
            if (allow is None or rule.name in allow or rule.placeholder in allow)
            and any(loc in rule.locales for loc in wanted)
        ]
        self.strict = strict

    def mask(self, text: str) -> MaskResult:
        out: dict[str, str] = {}
        counts: dict[str, int] = {}
        seen: dict[tuple[str, str], str] = {}

        def repl(rule: Rule, match: re.Match[str]) -> str:
            value = match.group(rule.group)
            if self.strict and rule.validator and not rule.validator(value):
                return value
            key = (rule.placeholder, value)
            token = seen.get(key)
            if token is None:
                counts[rule.placeholder] = counts.get(rule.placeholder, 0) + 1
                token = f"{{{{{rule.placeholder}_{counts[rule.placeholder]}}}}}"
                seen[key] = token
                out[token] = value
            return token

        working = text
        for rule in self.rules:
            working = rule.pattern.sub(lambda m, r=rule: repl(r, m), working)
        return MaskResult(text=working, mapping=out, counts=counts)

    def mask_many(self, texts: Iterable[str]) -> list[MaskResult]:
        return [self.mask(t) for t in texts]

    def unmask(self, text: str, mapping: dict[str, str]) -> str:
        if not mapping:
            return text
        # Longest tokens first so {{EMAIL_1}} is not shadowed by {{EMAIL_1x}}.
        for token in sorted(mapping, key=len, reverse=True):
            text = text.replace(token, mapping[token])
        return text


def selftest() -> int:
    m = PiiMasker(locales=["generic", "jp"])
    src = (
        "Mail alice@example.com or call +81 90 1234 5678. "
        "Card 4111 1111 1111 1111, IP 10.2.3.4, URL https://internal.example.local/x?token=1 "
        "key AKIAABCDEFGHIJKLMNOP token eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijk "
        "mynumber 1234-5678-9012 corp 1234567890123"
    )
    res = m.mask(src)
    assert "alice@example.com" not in res.text, res.text
    assert "4111 1111 1111 1111" not in res.text
    assert "10.2.3.4" not in res.text
    assert "AKIAABCDEFGHIJKLMNOP" not in res.text
    assert "{{EMAIL_1}}" in res.text
    # reversible
    back = m.unmask(res.text, res.mapping)
    assert back == src, (back, src)
    # dedup: same email -> same token
    dup = m.mask("a@b.com then a@b.com")
    assert dup.text.count("{{EMAIL_1}}") == 2, dup.text
    # strict: an invalid card is left alone
    strict = PiiMasker(strict=True)
    assert "4111111111111112" in strict.mask("n 4111111111111112").text
    assert "4111111111111111" not in strict.mask("n 4111111111111111").text
    # determinism
    assert m.mask(src).to_dict() == res.to_dict()
    print("selftest OK:", json.dumps({"counts": res.counts}, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic PII/secret masking (no model, no network).")
    ap.add_argument("--input", help="text file (default: stdin)")
    ap.add_argument("--locale", default="generic", help="comma list: generic, jp")
    ap.add_argument("--rules", default="", help="comma list of rule names/placeholders to allow")
    ap.add_argument("--strict", action="store_true", help="require checksums (may leave invalid formats unmasked)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    text = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    masker = PiiMasker(
        locales=[x.strip() for x in args.locale.split(",") if x.strip()],
        rules=[x.strip() for x in args.rules.split(",") if x.strip()] or None,
        strict=args.strict,
    )
    res = masker.mask(text)
    if args.json:
        print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(res.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
