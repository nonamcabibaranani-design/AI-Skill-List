# AI-Skill-List

Shared skill collection. Each skill is a git submodule.

| Dir | Upstream | Skills path | Notes |
|-----|----------|-------------|-------|
| `caveman/` | https://github.com/JuliusBrussee/caveman | `caveman/skills/` | caveman, caveman-commit, caveman-compress, ... |
| `ponytail/` | https://github.com/DietrichGebert/ponytail | `ponytail/skills/` | ponytail, ponytail-audit, ponytail-debt, ... |
| `superpowers/` | https://github.com/obra/superpowers | `superpowers/skills/` | brainstorming, systematic-debugging, test-driven-development, ... |
| `impeccable/` | https://github.com/pbakaus/impeccable | `impeccable/.agents/skills/impeccable/` (also `plugin/skills/impeccable/`) | design language skill (shallow clone) |
| `vercel-skills/` | https://github.com/vercel-labs/skills | `vercel-skills/skills/` | find-skills |

## Usage

```bash
git clone --recurse-submodules https://github.com/nonamcabibaranani-design/AI-Skill-List
# update all
git submodule update --remote --merge
```

This repo is agent-agnostic. Each submodule keeps its native installer, so any agent (not only OpenClaw) can consume it.

## Per-agent usage

### OpenClaw
Point at this repo via `skills.load.extraDirs`, or symlink individual skills into `~/.openclaw/skills`:
```json
{ "skills": { "load": { "extraDirs": ["/path/to/AI-Skill-List"] } } }
```

### Claude Code
- caveman: `claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman`
- superpowers: install `superpowers` from the official Claude plugin marketplace
- ponytail: plugin in `ponytail/` (`.claude-plugin/`)
- impeccable: `npx impeccable install` then `/impeccable init`
- any skill: `npx skills add <owner/repo>`

### Codex (CLI / App)
- caveman: `npx skills add JuliusBrussee/caveman -a codex -g`
- ponytail: plugin in `ponytail/` (`.codex-plugin/`)
- superpowers: see `superpowers/README.md` Codex section
- impeccable: `npx impeccable install --providers=codex`
- any skill: `npx skills use <owner/repo> --agent codex` (vercel-skills)

### Cursor / Windsurf / Cline / others
- caveman: `npx skills add JuliusBrussee/caveman -a cursor -g` (same pattern for windsurf, cline, etc.)
- ponytail: `.cursor/`, `.windsurf/`, `.devin-plugin/`, `.kiro/`, etc. in `ponytail/`
- superpowers: see `superpowers/README.md` per-harness table (Cursor, Opencode, Pi, Hermes, Gemini, Copilot, Grok, ...)
- impeccable: `npx impeccable install --providers=claude,codex,cursor,grok,hermes,veto`
- generic: `npx skills add <owner/repo> -a <agent> -g` (see `vercel-skills/README.md` for 75+ agents)

### Offline / vendored
```bash
git clone --recurse-submodules https://github.com/nonamcabibaranani-design/AI-Skill-List
```
Then point the agent at the local `*/skills/` path above. No MCP needed for static skills.
