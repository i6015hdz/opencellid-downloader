import pytest

from opencellid_downloader.client import OpenCellIdClient
from opencellid_downloader.exceptions import (
    CountryNotFoundError,
    InvalidMccError,
    MissingApiKeyError,
)


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

    assert "https://opencellid.org/ocid/downloads" in url
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


def test_download_country_downloads_single_mcc(monkeypatch, tmp_path):
    downloaded_mccs = []

    def fake_download_mcc(self,
                          mcc,
                          output_dir="data",
                          filename=None,
                          show_progress=True,
                          unzip=False,
                          keep_compressed=True
                          ):

        downloaded_mccs.append(mcc)
        return tmp_path / f"{mcc}.csv.gz"

    monkeypatch.setattr(OpenCellIdClient, "download_mcc", fake_download_mcc)

    client = OpenCellIdClient(api_key="fake-key")
    result = client.download_country(
        "Mexico",
        output_dir=tmp_path,
        show_progress=False,
    )

    assert downloaded_mccs == [334]
    assert result == [tmp_path / "334.csv.gz"]


def test_download_country_downloads_multiple_mccs(monkeypatch,
                                                  tmp_path,
                                                  unzip=False,
                                                  keep_compressed=True):
    downloaded_mccs = []

    def fake_download_mcc(self,
                          mcc,
                          output_dir="data",
                          filename=None,
                          show_progress=True,
                          unzip=False,
                          keep_compressed=True,
                          ):
        downloaded_mccs.append(mcc)
        return tmp_path / f"{mcc}.csv.gz"

    monkeypatch.setattr(OpenCellIdClient, "download_mcc", fake_download_mcc)

    client = OpenCellIdClient(api_key="fake-key")
    result = client.download_country(
        "USA",
        output_dir=tmp_path,
        show_progress=False,
    )

    assert downloaded_mccs == [310, 311, 312, 313, 314, 315, 316]
    assert result == [
        tmp_path / "310.csv.gz",
        tmp_path / "311.csv.gz",
        tmp_path / "312.csv.gz",
        tmp_path / "313.csv.gz",
        tmp_path / "314.csv.gz",
        tmp_path / "315.csv.gz",
        tmp_path / "316.csv.gz",
    ]


def test_download_country_raises_error_for_unknown_country(tmp_path):
    client = OpenCellIdClient(api_key="fake-key")

    with pytest.raises(CountryNotFoundError):
        client.download_country(
            "Atlantis",
            output_dir=tmp_path,
            show_progress=False,
        )


def test_download_mcc_returns_compressed_path_when_unzip_false(monkeypatch, tmp_path):
    def fake_download_file(url, output_path, show_progress=True):
        return output_path

    monkeypatch.setattr(
        "opencellid_downloader.client.download_file", fake_download_file)

    client = OpenCellIdClient(api_key="fake-key")
    result = client.download_mcc(
        334,
        output_dir=tmp_path,
        unzip=False,
        show_progress=False,
    )

    assert result == tmp_path / "334.csv.gz"


def test_download_mcc_unzips_when_requested(monkeypatch, tmp_path):
    def fake_download_file(url, output_path, show_progress=True):
        return output_path

    def fake_extract_gzip_file(gzip_path, keep_compressed=True):
        assert gzip_path == tmp_path / "334.csv.gz"
        assert keep_compressed is False
        return tmp_path / "334.csv"

    monkeypatch.setattr(
        "opencellid_downloader.client.download_file", fake_download_file)
    monkeypatch.setattr(
        "opencellid_downloader.client.extract_gzip_file",
        fake_extract_gzip_file,
    )

    client = OpenCellIdClient(api_key="fake-key")
    result = client.download_mcc(
        334,
        output_dir=tmp_path,
        unzip=True,
        keep_compressed=False,
        show_progress=False,
    )

    assert result == tmp_path / "334.csv"


def test_download_country_passes_unzip_options(monkeypatch, tmp_path):
    calls = []

    def fake_download_mcc(
        self,
        mcc,
        output_dir="data",
        filename=None,
        show_progress=True,
        unzip=False,
        keep_compressed=True,
    ):
        calls.append((mcc, unzip, keep_compressed))
        return tmp_path / f"{mcc}.csv"

    monkeypatch.setattr(OpenCellIdClient, "download_mcc", fake_download_mcc)

    client = OpenCellIdClient(api_key="fake-key")
    result = client.download_country(
        "Mexico",
        output_dir=tmp_path,
        unzip=True,
        keep_compressed=False,
        show_progress=False,
    )

    assert calls == [(334, True, False)]
    assert result == [tmp_path / "334.csv"]
