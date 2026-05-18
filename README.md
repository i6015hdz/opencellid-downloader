# OpenCellID Downloader

A Python library and command-line tool for downloading OpenCellID data.

## Project Status

This project is currently in early development.

Current Phase: Phase 2 — Core downloader functionality

Current test status:

```bash
10 passed
```

## Goals

- Download OpenCellID data using an API key
- Support full downloads and country-specific downloads
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

This downloads the OpenCellID file for Mexico using its MCC code.

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
- Download by country name
- Auto-unzip for `.csv.gz` files
- Streaming downloads with `requests`
- Progress bar with `tqdm`
- Temporary `.part` file handling
- Custom exceptions
- Basic pytest test suite

## Coming Soon

- Download by country name
- Country-to-MCC lookup helper
- Auto-unzip for `.csv.gz` files
- Command-line arguments
- TestPyPI release
- PyPI release

## License

MIT License.

## Disclaimer

This package is not affiliated with OpenCellID or Unwired Labs.

Users are responsible for complying with OpenCellID's API usage, licensing, and attribution requirements.