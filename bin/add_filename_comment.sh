#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <project_directory>"
    exit 1
fi

project_dir="$1"
echo "The current working directory is: $project_dir"

# Add your script logic here, using $project_dir instead of hardcoded paths


# Define the resources
resources=('building' 'character' 'crafting' 'event' 'faction' 'floor_layout' 'floor' 'inventory' 'item' 'location' 'mission' 'npc' 'progression' 'skill' 'street' 'user')

# Loop through each resource to create import statements
for resource in "${resources[@]}"; do
    # Define the router, controller, and schema file names
    router_file="${project_dir}/routers/${resource}_router.py"
    controller_file="${project_dir}/controllers/${resource}_controller.py"
    schema_file="${project_dir}/schemas/${resource}_schema.py"
    model_file="${project_dir}/models/${resource}_model.py"

   
    # Check if the router file exists
    if [[ -f $router_file ]]; then
        # Add the imports to the router file if not already present
        if ! grep -q "# routers/${resource}_router.py" "$router_file"; then
            # Prepend the import statements
            {
                echo -e "# routers/${resource}_router.py"
                cat "$router_file"
            } > temp && mv temp "$router_file"
            echo "Added filename comment to $router_file"
        else
            echo "Filename comment already exists in $router_file"
        fi
    else
        echo "$router_file does not exist."
    fi

    # Check if the schema file exists
    if [[ -f $schema_file ]]; then
        # Add the imports to the router file if not already present
        if ! grep -q "# schemas/${resource}_schema.py" "$schema_file"; then
            # Prepend the import statements
            {
                echo -e "# schemas/${resource}_schema.py"
                cat "$schema_file"
            } > temp && mv temp "$schema_file"
            echo "Added filename comment to $schema_file"
        else
            echo "Filename comment already exists in $schema_file"
        fi
    else
        echo "$schema_file does not exist."
    fi

    # Check if the controller file exists
    if [[ -f $controller_file ]]; then
        # Add the imports to the router file if not already present
        if ! grep -q "# controllers/${resource}_controller.py" "$controller_file"; then
            # Prepend the import statements
            {
                echo -e "# controllers/${resource}_controller.py"
                cat "$controller_file"
            } > temp && mv temp "$controller_file"
            echo "Added filename comment to $controller_file"
        else
            echo "Filename comment already exists in $controller_file"
        fi
    else
        echo "$controller_file does not exist."
    fi

    # Check if the model file exists
    if [[ -f $model_file ]]; then
        # Add the imports to the router file if not already present
        if ! grep -q "# models/${resource}_model.py" "$model_file"; then
            # Prepend the import statements
            {
                echo -e "# models/${resource}_model.py"
                cat "$model_file"
            } > temp && mv temp "$model_file"
            echo "Added filename comment to $model_file"
        else
            echo "Filename comment already exists in $model_file"
        fi
    else
        echo "$model_file does not exist."
    fi
done

echo "Import addition completed."
