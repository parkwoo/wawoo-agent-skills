# deployment — expectations (uplift pilot)

Static checks for Docker Compose YAML. Secret commit policy is a separate gate.

## Compose

- `[deploy-no-latest-tag]` Avoid `image: ...:latest`
- `[deploy-plain-secret-env]` Plaintext-looking `password`/`secret`/`api_key` values (not `${}` / `$$` refs)
- `[deploy-missing-healthcheck]` Service with `ports` but no `healthcheck`

## Files

`docker-compose.yml`, `compose.yml`, etc. (`.yml`/`.yaml`).

## Check

```bash
python3 scripts/skill_uplift_check.py deployment --path <repo-or-compose-dir>
```