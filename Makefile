# The commands this repository is run with; CI runs the same ones. `make` alone lists them.

# The Agent Skills reference validator, pinned to a commit of agentskills/agentskills.
SKILLS_REF_COMMIT ?= 69ef37e9424c0a7ea9dd2293b559e43ec8176379
SKILLS_REF = uvx -q --from "git+https://github.com/agentskills/agentskills@$(SKILLS_REF_COMMIT)\#subdirectory=skills-ref" skills-ref
LYCHEE_VERSION ?= 0.24.2
LINK_INPUTS = 'README.md' 'CONTRIBUTING.md' 'skills/**/*.md'
# For `make sync`: e.g. LOCAL=dcp-rosetta=../DCP-Rosetta to sync from a checkout instead of GitHub.
LOCAL ?=

.DEFAULT_GOAL := help
.PHONY: help sync check lock spec links

help: ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[1m%-8s\033[0m %s\n", $$1, $$2}'

sync: ## Mirror the skills from their sources (LOCAL=id=path for a checkout)
	uv run -q scripts/sync.py $(if $(LOCAL),--local $(LOCAL))

check: lock spec ## Run the checks CI gates on (links run separately, see `links`)

lock: ## skills/ is exactly what the last sync wrote
	uv run -q scripts/check.py

spec: ## Every skill follows the Agent Skills specification
	@status=0; for skill in skills/*/; do $(SKILLS_REF) validate "$${skill%/}" >/dev/null || { $(SKILLS_REF) validate "$${skill%/}"; status=1; }; done; \
	[ $$status -eq 0 ] && echo "all skills valid"; exit $$status

links: ## Check internal links and anchors (needs Docker; CI uses the lychee action)
	docker run --rm -v "$(CURDIR)":/input:ro -w /input lycheeverse/lychee:$(LYCHEE_VERSION) \
		--offline --no-progress --include-fragments $(LINK_INPUTS)
