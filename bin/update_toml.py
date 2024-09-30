#!/usr/bin/env python3

import toml

def get_author_info():
    """Prompt the user for author name and email, and return a formatted author string."""
    author_name = input("Enter the author's name (leave blank if not applicable): ")
    if author_name:
        author_email = input("Enter the author's email address: ")
        return f"{author_name} <{author_email}>"
    return None

def get_project_description():
    """Prompt the user for project description, return None if not provided."""
    description = input("Enter the project description (leave blank for default): ")
    if description:
        return description
    return None

def update_pyproject_toml(author_string=None, description=None):
    """Update the pyproject.toml file with the given author and description."""
    with open('pyproject.toml', 'r') as f:
        data = toml.load(f)

    if author_string:
        data['tool']['poetry']['authors'] = [author_string]

    if description:
        data['tool']['poetry']['description'] = description

    with open('pyproject.toml', 'w') as f:
        toml.dump(data, f)

def main():
    """Main function to get user input and update the pyproject.toml file."""
    author_string = get_author_info()
    description = get_project_description()
    update_pyproject_toml(author_string, description)
    print("pyproject.toml has been updated.")

if __name__ == "__main__":
    main()
