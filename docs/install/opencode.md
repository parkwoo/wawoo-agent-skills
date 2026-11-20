# Install — OpenCode

Official: [opencode.ai](https://opencode.ai). Same config works for **Paseo** built-in OpenCode.

## One-shot

```bash
python3 scripts/install_opencode.py
python3 scripts/install_opencode.py --memory-writable
```

Writes `~/.config/opencode/opencode.json` with local MCP:

```json
{
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "/abs/path/to/wawoo-skills/mcp/server.py"],
      "enabled": true,
      "environment": {
        "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
        "WAWOO_MEMORY_READONLY": "1"
      }
    }
  }
}
```

No native slash workflows — use **`interpret_intent` → `workflow_get` → `skill_get`**.

Restart OpenCode / `paseo daemon restart` after env changes.

Full reference: [USAGE §2.5](../USAGE.md)