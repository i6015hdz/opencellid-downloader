import argparse
from pathlib import Path

from opencellid_downloader.client import OpenCellIdClient
from opencellid_downloader.exceptions import OpenCellIdDownloaderError


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="opencellid-download",
        description="Download OpenCellID data by country name or MCC code.",
    )

    parser.add_argument(
        "target",
        help='Country name or MCC code to download. Example: "Mexico" or "334".',
    )

    parser.add_argument(
        "--by-mcc",
        action="store_true",
        help="Treat the target as an MCC code instead of a country name.",
    )

    parser.add_argument(
        "--output",
        default="data",
        help="Output directory for downloaded files. Defaults to 'data'.",
    )

    parser.add_argument(
        "--token",
        default=None,
        help="OpenCellID API token. If omitted, OPENCELLID_API_KEY is used.",
    )

    parser.add_argument(
        "--unzip",
        action="store_true",
        help="Extract the downloaded .csv.gz file into a .csv file.",
    )

    parser.add_argument(
        "--remove-compressed",
        action="store_false",
        dest="keep_compressed",
        help="Delete the .csv.gz file after extraction. Only applies with --unzip.",
    )

    parser.set_defaults(keep_compressed=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the OpenCellID Downloader command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    client = OpenCellIdClient(api_key=args.token)

    try:
        if args.by_mcc:
            downloaded_path = client.download_mcc(
                args.target,
                output_dir=Path(args.output),
                unzip=args.unzip,
                keep_compressed=args.keep_compressed,
            )
            downloaded_files = [downloaded_path]
        else:
            downloaded_files = client.download_country(
                args.target,
                output_dir=Path(args.output),
                unzip=args.unzip,
                keep_compressed=args.keep_compressed,
            )

        print("Download complete:")
        for file_path in downloaded_files:
            print(f"- {file_path}")

        return 0

    except OpenCellIdDownloaderError as error:
        parser.exit(status=1, message=f"Error: {error}\n")
