## GIT

### Extract all file in all commit-hash

```bash
#!/bin/bash

# Create a directory to store the extracted files
mkdir -p extracted_files

# Loop through each commit hash
for commit in $(git rev-list --all); do
    echo "Processing commit $commit"

    # Get the list of files changed in the commit
    files=$(git diff-tree --no-commit-id --name-only -r "$commit")

    # Loop through each file and extract its content
    for file in $files; do
        # Create directories as needed
        mkdir -p "extracted_files/$(dirname "$file")"

        # Save the file content to a new file
        git show "$commit:$file" > "extracted_files/$file-$commit.txt" 2>/dev/null
    done
done

echo "Extraction complete. Files are saved in the 'extracted_files' directory."
```
