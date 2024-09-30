#!/bin/bash

# Dictionary for predefined package categories and groups
declare -A package_categories=(
    ["Web Frameworks"]="fastapi flask django"
    ["Extended Web Frameworks"]="fastapi-extras flask-extras django-extras"
    ["Machine Learning"]="pytorch tensorflow"
    ["Data Science"]="data-science"
    ["Web Scraping"]="scrapy beautifulsoup pyppeteer"
    ["Desktop Applications"]="tkinter pyqt kivy"
    ["CLI Tools"]="argparse click typer"
    ["NLP"]="spacy nltk hugging-face"
    ["Audio Processing"]="librosa pydub pysndfx"
    ["Task Scheduling"]="apscheduler celery cron"
    ["DevOps"]="fabric ansible boto3"
    ["Security"]="security auth"
    ["Monitoring"]="monitoring"
    ["Documentation"]="mkdocs sphinx"
    ["Performance"]="performance"
    ["Asynchronous"]="async"
)

# Dictionary for predefined package groups
declare -A package_groups=(
    ["fastapi"]="fastapi uvicorn pydantic httpx"
    ["fastapi-extras"]="fastapi uvicorn pydantic httpx fastapi-admin fastapi-login fastapi-mail jinja2"
    ["flask"]="flask gunicorn httpx"
    ["flask-extras"]="flask gunicorn httpx jinja2"
    ["django"]="django djangorestframework gunicorn httpx"
    ["django-extras"]="django djangorestframework gunicorn httpx django-debug-toolbar django-allauth django-filter django-q2 pytest-djang"
    ["pytorch"]="torch torchvision torchaudio scikit-learn numpy pandas matplotlib"
    ["tensorflow"]="tensorflow keras scikit-learn numpy pandas matplotlib"
    ["data-science"]="matplotlib seaborn scipy"
    ["scrapy"]="scrapy parsel lxml"
    ["beautifulsoup"]="beautifulsoup4 lxml"
    ["pyppeteer"]="pyppeteer lxml"
    ["tkinter"]="pyautogui"
    ["pyqt"]="pyqt5 pyqt5-tools qtpy"
    ["kivy"]="kivy"
    ["argparse"]="argparse"
    ["click"]="click"
    ["typer"]="typer"
    ["spacy"]="spacy https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.7.1/en_core_web_md-3.7.1-py3-none-any.whl https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1/en_core_web_lg-3.7.1-py3-none-any.whl"
    ["nltk"]="nltk"
    ["hugging-face"]="transformers@^4.44.2 tokenizers@^0.19 datasets@^3.0.0"
    ["librosa"]="librosa soundfile sounddevice"
    ["pydub"]="pydub ffmpeg-python sounddevice"
    ["pysndfx"]="pysndfx sounddevice"
    ["apscheduler"]="apscheduler pytz"
    ["celery"]="celery"
    ["cron"]="cron-descriptor croniter"
    ["fabric"]="fabric paramiko"
    ["ansible"]="ansible ansible-core paramiko"
    ["boto3"]="boto3 paramiko"
    ["security"]="oauthlib bandit safety cryptography"
    ["auth"]="argon2-cffi python-jose authlib pyjwt"
    ["monitoring"]="prometheus-client loguru sentry-sdk"
    ["mkdocs"]="mkdocs"
    ["sphinx"]="sphinx"
    ["performance"]="cachetools aiohttp"
    ["async"]="motor"
)

# Associative array for main dependencies
declare -A main_dependencies=(
    ["python-dotenv"]="^1.0.1"
    ["requests"]="^2.32.3"
    ["packaging"]="^24.1"
)

# List of dev dependencies
dev_dependencies=(
    "black@^24.8.0"
    "isort@^5.13.2"
    "flake8@^7.1.1"
    "pylint@^3.2.7"
    "pytest@^8.3.3"
    "pytest-cov@^5.0.0"
    "mypy@^1.11.2"
    "bandit@^1.7.9"
    "safety@^3.2.7"
    "coverage@^7.6.1"
    "toml@^0.10.2"
)

# Associative array for database groups
declare -A database_options=(
    ["postgres"]="psycopg2-binary asyncpg"
    ["mysql"]="pymysql aiomysql"
    ["sqlite"]="sqlite-utils aiosqlite"
    ["mongodb"]="pymongo mongoengine"
    ["redis"]="redis aioredis"
)

# Function to prompt for yes/no input
prompt_for_input() {
    local prompt_message=$1
    read -p "$prompt_message (y/n): " choice
    case "$choice" in
        [Yy]* ) return 0;;  # Yes
        [Nn]* ) return 1;;  # No
        '' )    return 1;;  # Default to No if no input
        * )     echo "Invalid response. Please answer y or n."; return 1;;  # Invalid input
    esac
}

# Function to prompt for selection from a list
select_from_list() {
    local prompt_message=$1
    shift
    local options=("$@")
    
    PS3="$prompt_message "
    select opt in "${options[@]}"; do
        if [[ -n "$opt" ]]; then
            echo "$opt"
            return
        else
            echo "Invalid option. Please choose a valid option."
        fi
    done
}

# Function to install a group of packages using poetry
install_group() {
    local group_name=$1
    local packages=$2

    echo "Installing packages for $group_name..."
    for package in $packages; do
        echo "Installing $package for group $group_name..."
        poetry add "$package"
    done
}

# Function to install main dependencies
install_main_dependencies() {
    echo "Installing main dependencies..."
    for package in "${!main_dependencies[@]}"; do
        poetry add "$package${main_dependencies[$package]}"
    done
    echo "Main dependencies installed."
}

# Function to install development dependencies
install_dev_dependencies() {
    echo "Installing development dependencies..."
    for dev_package in "${dev_dependencies[@]}"; do
        poetry add "$dev_package" --group dev
    done
    echo "Development dependencies installed."
}

# Function to set up predefined templates within a selected category
setup_predefined_templates() {
    echo "Available categories:"
    local categories=("${!package_categories[@]}")
    local selected_category=$(select_from_list "Select a category" "${categories[@]}")
    
    if [ -n "$selected_category" ]; then
        echo "Selected category: $selected_category"
        local groups=${package_categories[$selected_category]}
        
        echo "Available groups in $selected_category:"
        local group_to_install=$(select_from_list "Select a group to install" $groups)
        
        if [ -n "$group_to_install" ]; then
            if prompt_for_input "Do you want to install the $group_to_install group?"; then
                install_group "$group_to_install" "${package_groups[$group_to_install]}"
                echo "$group_to_install setup completed."
                return
            fi
        fi
    fi
}

# Fallback function to allow custom group creation and installation
setup_custom_groups() {
    echo "Setting up custom groups..."

    while true; do
        read -p "Enter a custom group name (or press Enter to finish): " custom_group
        if [ -z "$custom_group" ]; then
            echo "Finished setting up custom groups."
            break
        fi

        read -p "Enter the packages you want to add to the $custom_group group (separated by spaces): " custom_packages

        # Install the custom packages using poetry add
        echo "Installing custom packages for the $custom_group group..."
        for package in $custom_packages; do
            poetry add "$package" --group "$custom_group"
        done
    done
}

# Function to set up the database, including the common SQL group
setup_database() {
    echo "Setting up database..."

    # Install common SQL packages
    echo "Installing common SQL dependencies..."
    poetry add sqlalchemy databases --group sql-common

    # Prompt for database selection
    echo "Select a database to install:"
    select db_option in "${!database_options[@]}"; do
        if [[ -n "$db_option" ]]; then
            echo "Installing $db_option packages..."
            install_group "$db_option" "${database_options[$db_option]}"
            break
        else
            echo "Invalid selection. Please choose a valid option."
        fi
    done
}

# Function to create and activate virtual environment
setup_virtualenv() {
    if [ ! -d ".venv" ]; then
        # Create a virtual environment
        echo "Creating Python virtual environment..."
        python3 -m venv .venv
        echo "Python virtual environment created at .venv"
    fi

    # Activate the virtual environment
    echo "Activating the virtual environment..."
    source .venv/bin/activate
    echo "Virtual environment activated."
}

# Function to initialize Git repository
setup_git() {
    if [ ! -d ".git" ]; then
        echo "Initializing Git repository..."
        git init
        echo "Git repository initialized."
    else
        echo "Git repository already initialized."
    fi
}

# Main function to prompt user for predefined or custom setup
main() {
    echo "Starting the setup process..."

    # Setup and activate virtual environment first
    setup_virtualenv

    # Setup Git repository
    setup_git

    # Install main dependencies
    install_main_dependencies

    # Install development dependencies
    install_dev_dependencies

    # Setup Database
    setup_database

    if prompt_for_input "Do you want to use predefined templates?"; then
        setup_predefined_templates
    else
        setup_custom_groups
    fi
}

main
