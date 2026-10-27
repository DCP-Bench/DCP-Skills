#!/usr/bin/env bash
# Prints a lychee report with a heading and a note on what was checked, for a
# job summary or an issue. lychee's own report is only a bare "Summary" table.
#
#     scripts/link-report.sh internal|all REPORT

set -euo pipefail
scope=$1 report=$2

case $scope in
  internal) cat <<'EOF'
## Link check: internal links

Every relative link and `#anchor` in `README.md`, `CONTRIBUTING.md` and `skills/`
must point at a file or heading that exists. External (`http`) links are not
fetched here: they are counted as *Excluded* and checked weekly by the Links
workflow instead.
EOF
  ;;
  all) cat <<'EOF'
## Link check: all links

The weekly check that every link in `README.md`, `CONTRIBUTING.md` and `skills/`
resolves, external websites included. An external link can fail because a site
was briefly down, so rerun the Links workflow before chasing one.
EOF
  ;;
  *) echo "usage: $0 internal|all REPORT" >&2; exit 2 ;;
esac

cat <<'EOF'

How to read the table: *Total* counts every link found, repeats included, and
*Unique* the distinct targets. *Successful* links resolve, *Excluded* ones were
not checked, and *Errors* are broken links, listed below the table. A broken
link inside a skill is fixed in the skill's source repository (see
`skills.lock.json`), not here.

EOF
# lychee's headings, two levels down so they sit under the one above.
sed -e 's/^#/###/' -e 's/^### Summary$/### Results/' "$report"
