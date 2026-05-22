# OpenCellID Downloader

A Python library and command-line tool for downloading OpenCellID data by MCC code or country name.

## Project Status

This project is currently in active development.

Current Phase: Phase 4 — Command-line interface functionality

Current test status:

```bash
32 passed
```

## Goals

- Download OpenCellID data using an API key
- Support downloads by MCC code
- Support downloads by country name
- Provide a Python library interface
- Provide a command-line interface
- Support automatic `.csv.gz` extraction
- Prepare the package for TestPyPI and PyPI release

## Installation

Installation from PyPI is coming soon.

For local development, install the package in editable mode:

```bash
pip install -e .
```

## Development Setup

Create and activate the conda environment:

```bash
conda create -n opencellid-downloader python=3.11
conda activate opencellid-downloader
```

Install the package locally:

```bash
pip install -e .
```

Run the test suite:

```bash
pytest
```

## API Key Setup

Create a local `.env` file in the project root:

```env
OPENCELLID_API_KEY=your_api_key_here
```

Do not commit your `.env` file to GitHub.

The project includes `.env.example` as a safe template:

```env
OPENCELLID_API_KEY=your_api_key_here
```

You can also pass a token directly through the CLI with:

```bash
opencellid-download Mexico --token YOUR_TOKEN
```

## Python Usage

### Build a download URL

```python
from opencellid_downloader import OpenCellIdClient

client = OpenCellIdClient(api_key="fake-key")
url = client.build_mcc_download_url(334)

print(url)
```

Expected output:

```text
https://opencellid.org/downloads.php?token=fake-key&type=mcc&file=334.csv.gz
```

### Download by MCC

```python
from opencellid_downloader import OpenCellIdClient

client = OpenCellIdClient()
client.download_mcc(334, output_dir="data")
```

This downloads the OpenCellID file for MCC `334`, which corresponds to Mexico.

The file will be saved as:

```text
data/334.csv.gz
```

### Download by country name

```python
from opencellid_downloader import OpenCellIdClient

client = OpenCellIdClient()
client.download_country("Mexico", output_dir="data")
```

This downloads the OpenCellID file for Mexico using the country-to-MCC lookup helper.

### Download and unzip

```python
from opencellid_downloader import OpenCellIdClient

client = OpenCellIdClient()
client.download_country(
    "Mexico",
    output_dir="data",
    unzip=True,
    keep_compressed=True,
)
```

This downloads:

```text
data/334.csv.gz
```

and extracts:

```text
data/334.csv
```

If you do not want to keep the compressed file, use:

```python
client.download_country(
    "Mexico",
    output_dir="data",
    unzip=True,
    keep_compressed=False,
)
```

## Command-Line Usage

After installing the package locally with:

```bash
pip install -e .
```

you can use the CLI command:

```bash
opencellid-download --help
```

### Download by country name

```bash
opencellid-download Mexico
```

This downloads OpenCellID data for Mexico using the country-to-MCC lookup helper.

### Download by MCC code

```bash
opencellid-download 334 --by-mcc
```

This downloads OpenCellID data for MCC `334`.

### Choose an output folder

```bash
opencellid-download Mexico --output data
```

### Use a token directly

```bash
opencellid-download Mexico --token YOUR_TOKEN
```

If `--token` is not provided, the package will try to read the token from:

```env
OPENCELLID_API_KEY=your_api_key_here
```

### Download and unzip

```bash
opencellid-download Mexico --unzip
```

This downloads the `.csv.gz` file and extracts it to `.csv`.

### Download, unzip, and remove the compressed file

```bash
opencellid-download Mexico --unzip --remove-compressed
```

This keeps the extracted `.csv` file and removes the original `.csv.gz` file.

### Download by MCC, unzip, and choose output folder

```bash
opencellid-download 334 --by-mcc --output data --unzip
```

## How Downloads Work

The downloader uses streaming so large files are not loaded into memory all at once.

The file is downloaded in chunks and first written to a temporary `.part` file. After the download completes successfully, the `.part` file is renamed to the final filename.

This helps prevent broken or incomplete files from appearing as valid downloads.

## Current Features

- `OpenCellIdClient`
- API key support through direct argument or `.env`
- MCC download URL builder
- Download by MCC code
- Country name to MCC lookup
- Country aliases such as `MX`, `USA`, and `UK`
- Download by country name
- Support for countries with multiple MCC codes
- Auto-unzip for `.csv.gz` files
- Option to keep or remove compressed files after extraction
- Streaming downloads with `requests`
- Progress bar with `tqdm`
- Temporary `.part` file handling
- Custom exceptions
- Command-line interface with `opencellid-download`
- CLI support for country downloads
- CLI support for MCC downloads
- CLI support for `--output`, `--token`, `--unzip`, and `--remove-compressed`
- Pytest test suite with mocked downloads and CLI tests

## Coming Soon

- TestPyPI release
- PyPI release
- More complete country/MCC coverage
- Improved documentation
- Optional CI testing with GitHub Actions

## License

MIT License.

## Disclaimer

This package is not affiliated with OpenCellID or Unwired Labs.

Users are responsible for complying with OpenCellID's API usage, licensing, and attribution requirements.