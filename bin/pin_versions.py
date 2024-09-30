#!/usr/bin/env python3

import toml
import subprocess

# Function to get the installed version of a package
def get_installed_version(package_name):
    try:
        # Use Poetry to show installed version, alternatively use pip if you prefer
        result = subprocess.run(["poetry", "show", package_name], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if line.startswith(package_name):
                return line.split()[1]  # Returns the version
    except Exception as e:
        print(f"Error fetching version for {package_name}: {e}")
    return None

# Function to update dependencies in a specific group (main, dev, optional groups, etc.)
def update_dependencies(group, group_key):
    if group in group_key:
        for package, version in group_key[group].items():
            if version == "*":
                installed_version = get_installed_version(package)
                if installed_version:
                    print(f"Updating {package} in {group} from '*' to '{installed_version}'")
                    group_key[group][package] = f"^{installed_version}"

# Load the pyproject.toml file
def main():
    try:
        with open("pyproject.toml", "r") as file:
            data = toml.load(file)

        # Update main dependencies
        update_dependencies('dependencies', data['tool']['poetry'])

        # Update dev dependencies
        update_dependencies('dev-dependencies', data['tool']['poetry'])

        # Check for optional dependency groups under [tool.poetry.group]
        if 'group' in data['tool']['poetry']:
            for group_name, group_content in data['tool']['poetry']['group'].items():
                if 'dependencies' in group_content:
                    group_key = f"group.{group_name}.dependencies"
                    print(f"\nProcessing group: {group_key}")
                    update_dependencies('dependencies', group_content)

        # Save the updated TOML back to the file
        with open("pyproject.toml", "w") as file:
            toml.dump(data, file)

        print("pyproject.toml updated successfully.")
    
    except FileNotFoundError:
        print("Error: pyproject.toml not found in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
