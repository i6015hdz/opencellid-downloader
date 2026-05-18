from opencellid_downloader.exceptions import CountryNotFoundError


COUNTRY_MCC = {
    "mexico": [334],
    "germany": [262],
    "united states": [310, 311, 312, 313, 314, 315, 316],
    "canada": [302],
    "united kingdom": [234, 235],
    "spain": [214],
    "france": [208],
    "italy": [222],
    "brazil": [724],
    "argentina": [722],
    "colombia": [732],
}


COUNTRY_ALIASES = {
    "mx": "mexico",
    "mex": "mexico",
    "us": "united states",
    "usa": "united states",
    "u.s.": "united states",
    "u.s.a.": "united states",
    "uk": "united kingdom",
    "gb": "united kingdom",
    "great britain": "united kingdom",
}


def normalize_country_name(country: str) -> str:
    """ Normalize a country name or alias for lookup.

        args:
            country: Country name or alias to normalize. Such as "Mexico", "mx", "United States", "usa", etc.

        returns:
            Normalized country name for lookup key.

        raises:
            CountryNotFoundError: If the country name or alias is not recognized or valid.
    """
    if not isinstance(country, str):
        raise CountryNotFoundError(
            f"Invalid country name: {country}. Must be a string.")

    normalized = " ".join(country.strip().lower().replace("-", " ").split())

    if not normalized:
        raise CountryNotFoundError("Country name cannot be empty.")

    return COUNTRY_ALIASES.get(normalized, normalized)


def get_mcc_codes(country: str) -> list[int]:
    """ Return Mobile Country Codes (MCC) for a country name or alias.

        Args:
            country: Country name or alias to look up.

        Returns: 
            List of MCC codes associated with the country.

        Raises:
            CountryNotFoundError: If the country name or alias is not recognized or valid.
    """
    normalized_country = normalize_country_name(country)

    try:
        return COUNTRY_MCC[normalized_country]
    except KeyError as error:
        supported_countries = ", ".join(sorted(COUNTRY_MCC.keys()))
        raise CountryNotFoundError(
            f"Country '{country}' is not currently supported."
            f"Supported countries are: {supported_countries}."
        ) from error
