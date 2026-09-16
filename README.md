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

Point OpenClaw at this repo via `skills.load.extraDirs`, or symlink individual skills into `~/.openclaw/skills`.
