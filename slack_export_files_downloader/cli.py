import argparse
import os
import sys

from . import api
from .logging import get_logger


def main():
    logger = get_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'slack_api_token', type=str, help='Your Slack API token',
    )
    parser.add_argument(
        'slack_export_json_dirs_or_files', type=str, nargs='+',
        help='Directorties containing Slack export JSON files, or JSON files '
             'themselves.'
    )
    parser.add_argument(
        '--output-directory', '-o', type=str, default=None, 
        help='Base/root directory into which to download Slack export files. '
             'If not specified, the current working directory is used'
    )
    parser.add_argument(
        '--dry-run', action='store_true', 
        help='Do not actually download anything or make any directories, but '
             'print/log what would be downloaded.'
    )
    
    args = parser.parse_args(sys.argv[1:])

    download_dir = args.output_directory or os.getcwd()

    for dir_or_filepath in args.slack_export_json_dirs_or_files:
        if os.path.isfile(dir_or_filepath):
            api.download_files_from_json(
                args.slack_api_token, dir_or_filepath, download_dir, 
                dry_run=args.dry_run
            )
        elif os.path.isdir(dir_or_filepath):
            api.download_all_files_from_slack_export_directory(
                args.slack_api_token, dir_or_filepath, download_dir,
                dry_run=args.dry_run
            )
        else:
            logger.warning('Skipping %s, not a directory or file.', dir_or_filepath)

    return 0


if __name__ == '__main__':
    sys.exit(main())
