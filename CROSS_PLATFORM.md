# Cross-Platform Support

Baker Street v0.4.3+ supports multiple AI agent platforms through a tool name abstraction layer.

## Supported Platforms

| Platform | Install | Invocation | Tool Names |
|----------|---------|------------|------------|
| **Claude Code** | `npx github:tywinlu1988/Baker-Street` | `/sherlock "query"` | WebFetch, Bash, Read, Write |
| **Codex CLI** | `npx github:tywinlu1988/Baker-Street --platform codex` | `@sherlock analyze "query"` | web_search, run_command, read_file, write_file |
| **Antigravity** | `npx github:tywinlu1988/Baker-Street --platform antigravity` | `/analyze --skill sherlock "query"` | fetch, exec, read, write |
| **Cursor** | `npx github:tywinlu1988/Baker-Street --platform cursor` | `@sherlock "query"` | web_search, terminal, read_file, save_file |

## Architecture

The framework uses **platform-agnostic tool names** internally (`web_search`, `run_command`, `read_file`, `write_file`). At install time, `tool-map.json` maps generic names to platform-specific names. Persona prompts, research agents, and the orchestration pipeline all use generic names — they never reference platform-specific tool APIs.

```
Persona prompt (generic)
    ↓
tool-map.json (resolve platform)
    ↓
Platform runtime (execute)
```

## Installation

### Automatic (Recommended)
```bash
# Claude Code
npx github:tywinlu1988/Baker-Street

# Other platforms
npx github:tywinlu1988/Baker-Street --platform codex
npx github:tywinlu1988/Baker-Street --platform antigravity
npx github:tywinlu1988/Baker-Street --platform cursor
```

### Manual
```bash
git clone https://github.com/tywinlu1988/Baker-Street.git
cp -r Baker-Street/.claude/skills/sherlock ~/.<platform>/skills/sherlock/
```

## Platform-Specific Notes

### Codex CLI
- Skills are registered via `~/.codex/skills/`
- Invocation uses `@sherlock analyze` command prefix
- All tools share generic names — no mapping needed

### Antigravity
- Skills are registered via `~/.antigravity/skills/`
- Invocation: `/analyze --skill sherlock`
- Tool names differ: `fetch` (web), `exec` (shell), `read`/`write` (files)

### Cursor
- Skills are registered via `~/.cursor/skills/`
- Invocation: `@sherlock`
- `terminal` replaces `run_command` for shell access

## Adding a New Platform

1. Add an entry to `tool-map.json` under `platforms`
2. Add an entry to `install.js` under `PLATFORM_DIRS`, `PLATFORM_NAMES`, `PLATFORM_USAGE`
3. Create a manifest in `platforms/<name>.json`
4. No changes needed to persona prompts, research agents, or orchestration

## Verification

All persona files, research prompt, scout prompt, and skill orchestration use generic tool names only. Verified zero hardcoded platform-specific tool references as of v0.4.1.
