import os
import json
import requests
import uuid

from .logging import get_logger


def download_files_from_json(slack_api_token: str, json_file_path: str, download_dir: str, dry_run: bool=False) -> list:
    """ Download all file entries from the `json_file_path` that has `url_private_download` URLs. 
    
    Parameters
    ----------
    slack_api_token: str
        Slack API token.
    json_file_path: str
        Path to the Slack export JSON file to download files from.
    download_dir: str
        Path to the directory to save the downloaded files into.
    dry_run: bool
        Defaults to False. If True, don't actually download any files
        or create any directories, but log what would be downloaded.

    Returns
    -------
    downloaded_files: list
        A list of the files that were downloaded.

    """
    logger = get_logger()

    # Load the Slack JSON export file
    with open(json_file_path, 'rb') as f:
        slack_export = json.load(f)

    # Build the Slack auth header
    headers = {'Authorization': f'Bearer {slack_api_token}'}

    # Loop through the exported files and download them
    downloaded_files = []
    for export_entry in slack_export:
        if 'files' not in export_entry:
            continue

        for file_entry in export_entry['files']:
            file_id = file_entry.get('id')
            file_url = file_entry.get('url_private_download')
            if not file_url:
                logger.warning(
                    'Cannot download entry with id: %s: no "url_private_download" key.', file_id or None)
                continue

            file_name = file_entry.get('name')
            if not file_name:
                logger.warning(
                    'Cannot download file with URL %s, no "name" key.', file_url)
                continue

            file_path = os.path.join(download_dir, file_name)

            if dry_run:
                downloaded_files.append(file_path)
                logger.info('Downloaded %s to %s', file_name, file_path)
                continue

            # Make the download_dir if missing
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # Send a GET request to the Slack API to download the file
            response = requests.get(file_url, headers=headers)

            # If the request succeeds, save the file to the specified directory,
            # otherwise log an error.
            if response.status_code == 200:
                # If a file with this name already exists, make a unique name
                if os.path.exists(file_path):
                    file_head, file_ext = os.path.splitext(file_path)
                    file_path = f'{file_head}_{str(uuid.uuid4())}{file_ext}'
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                downloaded_files.append(file_path)
                logger.info('Downloaded %s to %s', file_name, file_path)
            else:
                logger.error('Failed to download %s: status code = %d', file_name, response.status_code)

    return downloaded_files


def download_all_files_from_slack_export_directory(slack_api_token: str, slack_json_export_directory: str, base_download_directory: str, dry_run:bool=False) -> dict:
    """ Walk the `slack_json_export_directory` for JSON files and call `download_files_from_json()` 
    to download the files.

    Downloaded files are placed in a sub-directory of `base_download_directory`
    based on the Slack JSON export file path relative to 
    `slack_json_export_directory`.

    Parameters
    ----------
    slack_api_token: str
        Your Slack API token
    slack_json_export_directory: str
        Path to the directory containing Slack JSON export files
    base_download_directory: str
        Path to the directory to save the downloaded files into.
    dry_run: bool
        Defaults to False. If True, don't actually download any files
        or create any directories, but log what would be downloaded.

    Returns
    -------
    downloaded_files_dict: dict
        A dict of Slack JSON export files to a list of files downloaded from 
        that JSON file.
    
    """
    logger = get_logger()

    # Map of JSON file to list of all files downloaded from that JSON file
    downloaded_files_dict = {}
    for dirpath, dirnames, filenames in os.walk(slack_json_export_directory):
        # Relative path from our walk root, slack_json_export_directory, to dirpath.
        reldirpath = os.path.relpath(dirpath, slack_json_export_directory)
        # Join the reldirpath to our base_download_directory to form our download_dir for this path
        download_dir = os.path.abspath(os.path.join(base_download_directory, reldirpath))
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() != '.json':
                continue

            json_filepath = os.path.join(dirpath, filename)

            logger.info('Processing %s', json_filepath)

            downloaded_files = download_files_from_json(
                slack_api_token, json_filepath, download_dir, dry_run=dry_run)
            downloaded_files_dict[json_filepath] = downloaded_files

    return downloaded_files_dict
