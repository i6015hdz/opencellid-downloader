from pathlib import Path

import pytest

from opencellid_downloader.cli import build_parser, main
from opencellid_downloader.exceptions import MissingApiKeyError


def test_cli_parser_defaults():
    parser = build_parser()

    args = parser.parse_args(["Mexico"])

    assert args.target == "Mexico"
    assert args.by_mcc is False
    assert args.output == "data"
    assert args.token is None
    assert args.unzip is False
    assert args.keep_compressed is True


def test_cli_parser_mcc_and_unzip_options():
    parser = build_parser()

    args = parser.parse_args(
        [
            "334",
            "--by-mcc",
            "--output",
            "downloads",
            "--token",
            "fake-token",
            "--unzip",
            "--remove-compressed",
        ]
    )

    assert args.target == "334"
    assert args.by_mcc is True
    assert args.output == "downloads"
    assert args.token == "fake-token"
    assert args.unzip is True
    assert args.keep_compressed is False


def test_cli_downloads_country(monkeypatch, tmp_path, capsys):
    calls = []

    class FakeClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        def download_country(
            self,
            country,
            output_dir="data",
            unzip=False,
            keep_compressed=True,
        ):
            calls.append(
                {
                    "api_key": self.api_key,
                    "country": country,
                    "output_dir": output_dir,
                    "unzip": unzip,
                    "keep_compressed": keep_compressed,
                }
            )
            return [Path(output_dir) / "334.csv.gz"]

    monkeypatch.setattr(
        "opencellid_downloader.cli.OpenCellIdClient", FakeClient)

    exit_code = main(
        [
            "Mexico",
            "--output",
            str(tmp_path),
            "--token",
            "fake-token",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert calls == [
        {
            "api_key": "fake-token",
            "country": "Mexico",
            "output_dir": tmp_path,
            "unzip": False,
            "keep_compressed": True,
        }
    ]
    assert "Download complete:" in captured.out
    assert "334.csv.gz" in captured.out


def test_cli_downloads_mcc_with_unzip_options(monkeypatch, tmp_path, capsys):
    calls = []

    class FakeClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        def download_mcc(
            self,
            mcc,
            output_dir="data",
            filename=None,
            show_progress=True,
            unzip=False,
            keep_compressed=True,
        ):
            calls.append(
                {
                    "api_key": self.api_key,
                    "mcc": mcc,
                    "output_dir": output_dir,
                    "unzip": unzip,
                    "keep_compressed": keep_compressed,
                }
            )
            return Path(output_dir) / "334.csv"

    monkeypatch.setattr(
        "opencellid_downloader.cli.OpenCellIdClient", FakeClient)

    exit_code = main(
        [
            "334",
            "--by-mcc",
            "--output",
            str(tmp_path),
            "--token",
            "fake-token",
            "--unzip",
            "--remove-compressed",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert calls == [
        {
            "api_key": "fake-token",
            "mcc": "334",
            "output_dir": tmp_path,
            "unzip": True,
            "keep_compressed": False,
        }
    ]
    assert "Download complete:" in captured.out
    assert "334.csv" in captured.out


def test_cli_exits_with_error_message(monkeypatch, capsys):
    class FakeClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        def download_country(
            self,
            country,
            output_dir="data",
            unzip=False,
            keep_compressed=True,
        ):
            raise MissingApiKeyError("Missing token for test.")

    monkeypatch.setattr(
        "opencellid_downloader.cli.OpenCellIdClient", FakeClient)

    with pytest.raises(SystemExit) as error:
        main(["Mexico"])

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert "Error: Missing token for test." in captured.err
