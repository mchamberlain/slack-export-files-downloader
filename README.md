# Slack Export Files Downloader
A small Python package to download all the file uploads referenced in a Slack
JSON export.

## Dependencies
The project uses [Poetry](https://python-poetry.org) for dependency management.
Install Poetry and your system and then in the repo root run:

    $ poetry install

to install the dependencies.

## Usage
For the script to be able to access the file uploads on Slack, you need a valid
Slack API token with associated scope/permission to access the files. See 
https://api.slack.com/authentication/token-types.

Usage:

    $ poetry run slack-export-files-downloader --help
    usage: slack-export-files-downloader [-h] [--output-directory OUTPUT_DIRECTORY] [--dry-run]
                                     slack_api_token slack_export_json_dirs_or_files
                                     [slack_export_json_dirs_or_files ...]

    positional arguments:
    slack_api_token       Your Slack API token
    slack_export_json_dirs_or_files
                            Directorties containing Slack export JSON files, or JSON files themselves.

    options:
    -h, --help            show this help message and exit
    --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                            Base/root directory into which to download Slack export files. If not specified, the current
                            working directory is used
    --dry-run             Do not actually download anything or make any directories, but print/log what would be
                            downloaded.

