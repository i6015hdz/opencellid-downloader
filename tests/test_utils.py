import gzip

import pytest

from opencellid_downloader.exceptions import DownloadError
from opencellid_downloader.utils import extract_gzip_file


def test_extract_gzip_file_creates_csv(tmp_path):

    compressed_path = tmp_path / "sample.csv.gz"
    expected_content = b"radio,mcc\nLTE,334\n"

    with gzip.open(compressed_path, "wb") as file:
        file.write(expected_content)

    result = extract_gzip_file(compressed_path)

    assert result == tmp_path / "sample.csv"
    assert result.exists()
    assert result.read_bytes() == expected_content
    assert compressed_path.exists()


def test_extract_gzip_file_can_remove_compressed_file(tmp_path):

    compressed_path = tmp_path / "sample.csv.gz"
    expected_content = b"radio,mcc\nLTE,334\n"

    with gzip.open(compressed_path, "wb") as file:
        file.write(expected_content)

    result = extract_gzip_file(
        compressed_path,
        keep_compressed=False
    )

    assert result == tmp_path / "sample.csv"
    assert result.exists()
    assert result.read_bytes() == expected_content
    assert not compressed_path.exists()


def test_extract_gzip_file_raises_error_for_missing_file(tmp_path):
    missing_path = tmp_path / "missing.csv.gz"

    with pytest.raises(DownloadError):
        extract_gzip_file(missing_path)
