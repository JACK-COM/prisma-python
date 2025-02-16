# Make a release commit + tag, creating Changelog entry
# Set BUMP variable to any of supported (major, minor, patch)
# See 'bump-my-version show-bump' for options
# Variable BUMP defaults to 'patch' (v1.2.3 -> v1.2.4)
.PHONY: release changelog
BUMP=patch
release: 
	uvx bump-my-version bump ${BUMP}

# Generate a changelog using "angular" template and pipe output to CHANGELOG.md
changelog:
	git-changelog -io CHANGELOG.md -c angular
