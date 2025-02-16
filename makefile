.PHONY: all changelog start migrate-start migrate help

all: ## | "List all available commands"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' \
	| column -t -s '|'

# Generate a changelog using "angular" template and pipe output to CHANGELOG.md
# Format is:
# 
# # Changelog
# 
# Generated on (date)
# 
# ## Latest changes
# 
# Listing changes from the last 20 commits:
# 
# [ changes ]
changelog: ## | "Generate a changelog for the last 20 commits"
	echo "Generating changelog..."
	echo "# Changelog" > CHANGELOG.md
	echo "" >> CHANGELOG.md
	echo "Generated on `date +'%A, %B %d, %Y'`" >> CHANGELOG.md
	echo "" >> CHANGELOG.md

	echo "## Latest changes" >> CHANGELOG.md
	echo "" >> CHANGELOG.md

	echo "Listing changes from the last 20 commits:" >> CHANGELOG.md
	echo "" >> CHANGELOG.md

	# Print the last 20 commit subject-lines to changelog
	# git log -20 --no-merges --format=%B --pretty=%s >> CHANGELOG.md
	git log -20 --no-merges --format=%B >> CHANGELOG.md
	echo "Changelog generated."

start: ## | "Start the (dev or production) server (shroter than the "uv" version)."
	uv run dev.py


migrate-start: ## | "Run a db migration BEFORE starting the server."
	uv run dev.py --migrate

# Run a db migration WITHOUT starting the server.
migrate:
	uv run scripts/db_migrate.py
