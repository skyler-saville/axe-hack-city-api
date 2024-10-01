#!/bin/bash

# Define the resources
resources=('building' 'character' 'crafting' 'event' 'faction' 'floor_layout' 'floor' 'inventory' 'item' 'location' 'mission' 'npc' 'progression' 'skill' 'street' 'user')

# Loop through each resource to create import statements
for resource in "${resources[@]}"; do
    # Define the router, controller, and schema file names
    router_file="routers/${resource}_router.py"
    controller_file="controllers/${resource}_controller.py"
    schema_file="schemas/${resource}_schema.py"

    # Construct the import statements
    import_statements="from ..controllers.${resource}_controller import ${resource^}Controller\n"
    import_statements+="from ..schemas.${resource}_schema import ${resource^}Schema, ${resource^}CreateSchema, ${resource^}UpdateSchema\n"
    import_statements+="from ..models.${resource}_model import ${resource^}\n"

    # Check if the router file exists
    if [[ -f $router_file ]]; then
        # Add the imports to the router file if not already present
        if ! grep -q "from ..models.${resource}_model" "$router_file"; then
            # Prepend the import statements
            {
                echo -e "$import_statements"
                cat "$router_file"
            } > temp && mv temp "$router_file"
            echo "Added imports to $router_file"
        else
            echo "Imports already exist in $router_file"
        fi
    else
        echo "$router_file does not exist."
    fi
done

echo "Import addition completed."
