# PW1-WP11-NEATLOGIC-SOURCE-PIN-001 Validation

## Commands

- `git ls-remote https://gitee.com/neat-logic/neatlogic-itom-all.git HEAD refs/heads/develop4.0.0 refs/tags/4.0.0`
- `git ls-remote https://gitee.com/neat-logic/neatlogic-itom-all.git 'refs/tags/4.0.0^{}'`
- `git diff --check -- neatlogic-governance-index.md`
- `rg -n "PW1-WP11|4\\.0\\.0|Legal evidence pointer|Code-movement stop condition|fedf80" neatlogic-governance-index.md`

## Result

All validation commands passed.
