import pytest

from opencellid_downloader.countries import (
    get_mcc_codes,
    normalize_country_name,
)

from opencellid_downloader.exceptions import CountryNotFoundError


def test_normalize_country_name_lowercases_and_strips():
    assert normalize_country_name(" Mexico ") == "mexico"


def test_normalize_country_name_collapses_extra_spaces():
    assert normalize_country_name("United   States") == "united states"


def test_normalize_country_name_handles_aliases():
    assert normalize_country_name("mx") == "mexico"


def test_get_mcc_codes_for_mexico():
    assert get_mcc_codes("Mexico") == [334]


def test_get_mcc_codes_for_mexico_alias():
    assert get_mcc_codes("mx") == [334]


def test_get_mcc_codes_for_united_states_alias():
    assert get_mcc_codes("USA") == [310, 311, 312, 313, 314, 315, 316]


def test_get_mcc_codes_raises_error_for_unknown_country():
    with pytest.raises(CountryNotFoundError):
        get_mcc_codes("Atlantis")


def test_get_mcc_codes_raises_error_for_empty_country():
    with pytest.raises(CountryNotFoundError):
        get_mcc_codes("")
