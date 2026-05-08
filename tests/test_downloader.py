import pytest
import requests

from opencellid_downloader.downloader import download_file
from opencellid_downloader.exceptions import DownloadError


class FakeSuccessfulResponse:
    """ Fake successful HTTP response for testing downloads """

    status_code = 200
    headers = {"Content-Length": "11"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        return False

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size=1024):
        yield b"Hello"
        yield b"world"


class FakeFailedResponse:
    """ Fake failed HTTP response for testing download errors """
    status_code = 403  # status code indicating the server understands your request but refuses to authorize it
    headers = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        return False

    def raise_for_status(self):
        raise requests.HTTPError("Forbidden")

    def iter_content(self, chunk_size=1024):
        yield b""


def test_download_file_writes_content(monkeypatch, tmp_path):
    def fake_get(*args, **kwargs):
        return FakeSuccessfulResponse()

    monkeypatch.setattr(
        "opencellid_downloader.downloader.requests.get", fake_get)

    output_path = tmp_path / "test.csv.gz"

    result_path = download_file(
        url="https://example.com/test.csv.gz",
        output_path=output_path,
        show_progress=False,
    )

    assert result_path == output_path
    assert output_path.exists()
    assert output_path.read_bytes() == b"Helloworld"


def test_download_file_raises_download_error_on_http_error(monkeypatch, tmp_path):
    def fake_get(*args, **kwargs):
        return FakeFailedResponse()

    monkeypatch.setattr(
        "opencellid_downloader.downloader.requests.get", fake_get)

    output_path = tmp_path / "failed.csv.gz"

    with pytest.raises(DownloadError):
        download_file(
            url="https://example.com/failed.csv.gz",
            output_path=output_path,
            show_progress=False,
        )

    assert not output_path.exists()
