.PHONY: changelog

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
changelog:
	echo "# Changelog" > CHANGELOG.md
	echo "" >> CHANGELOG.md
	echo "Generated on `date +'%A, %B %d, %Y'`" >> CHANGELOG.md
	echo "" >> CHANGELOG.md

	echo "## Latest changes" >> CHANGELOG.md
	echo "" >> CHANGELOG.md

	echo "Listing changes from the last 20 commits:" >> CHANGELOG.md
	echo "" >> CHANGELOG.md

	# Print the last 20 commit subject-lines to changelog
	git log -20 --no-merges --format=%B --pretty=%s >> CHANGELOG.md

