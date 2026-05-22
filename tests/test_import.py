from opencellid_downloader import __version__
from opencellid_downloader import OpenCellIdClient


def test_package_import():
    """Test that the package can be imported and the version is correct."""
    assert __version__ == "0.1.1"


def test_client_can_be_created():
    """Test that the OpenCellIdClient can be instantiated."""
    client = OpenCellIdClient(api_key="fake-key")
    assert client.api_key == "fake-key"
