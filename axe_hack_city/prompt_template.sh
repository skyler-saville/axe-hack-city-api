#!/bin/bash

read -p "Enter the keyword: " keyword

# Create a temporary file
temp_file=$(mktemp)

resources=('building' 'character' 'crafting' 'event' 'faction' 'floor_layout' 'floor' 'inventory' 'item' 'location' 'mission' 'npc' 'progression' 'skill' 'street' 'user')

# Insert defaults into temporary file
echo "Take the following ${keyword} files and simplify them to remove the local file imports (routers, models, controllers, or schemas). Add Google Style Docstrings and Type Hints, for better DX. These will be the base before making the application more complex." >> "$temp_file"

echo "" >> "$temp_file"
echo "------------------" >> "$temp_file"
echo "" >> "$temp_file"

for resource in "${resources[@]}"; do
  # Insert the contents of the files into the temporary file
  cat "${keyword}s/${resource}_${keyword}.py" >> "$temp_file"
  echo "" >> "$temp_file"
  echo "------------------" >> "$temp_file"
  echo "" >> "$temp_file"
done

# Print the contents of the temporary file
cat "$temp_file"

# Remove the temporary file
rm "$temp_file"
