import pytest

from opencellid_downloader.client import OpenCellIdClient
from opencellid_downloader.exceptions import MissingApiKeyError, InvalidMccError


def test_client_accepts_api_key():
    client = OpenCellIdClient(api_key="fake-key")

    assert client.api_key == "fake-key"


def test_client_reads_api_key_from_environment(monkeypatch):
    monkeypatch.setenv("OPENCELLID_API_KEY", "env-fake-key")

    client = OpenCellIdClient(load_env=False)

    assert client.api_key == "env-fake-key"


def test_missing_api_key_raises_error(monkeypatch):
    monkeypatch.delenv("OPENCELLID_API_KEY", raising=False)

    client = OpenCellIdClient(load_env=False)

    with pytest.raises(MissingApiKeyError):
        client.build_mcc_download_url(334)


def test_build_mcc_download_url():
    client = OpenCellIdClient(api_key="fake-key")

    url = client.build_mcc_download_url(334)

    assert "https://opencellid.org/downloads.php" in url
    assert "token=fake-key" in url
    assert "type=mcc" in url
    assert "file=334.csv.gz" in url


def test_invalid_mcc_rejects_text():
    client = OpenCellIdClient(api_key="fake-key")

    with pytest.raises(InvalidMccError):
        client.build_mcc_download_url("Mexico")


def test_invalid_mcc_rejects_wrong_lenght():
    client = OpenCellIdClient(api_key="fake-key")

    with pytest.raises(InvalidMccError):
        client.build_mcc_download_url(33)
