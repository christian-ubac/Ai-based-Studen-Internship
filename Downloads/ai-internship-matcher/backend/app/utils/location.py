"""Location helper utilities.

Provides a stricter Philippines-location check used by the seeder and scraper.
"""
from typing import Optional

# Canonical tokens for Philippine locations, cities, provinces and common abbreviations.
# Keep tokens lowercase for simple substring matching.
PH_TOKENS = [
    "philippin", "philippines", "ph", "phil", "manila", "metro manila",
    "quezon city", "quezon", "qc", "makati", "cebu", "cebu city", "davao",
    "davao city", "iloilo", "bacolod", "baguio", "cagayan", "zamboanga",
    "pasig", "muntinlupa", "taguig", "las piñas", "valenzuela", "valenzuela city",
    "laguna", "batangas", "laguna province", "visayas", "mindanao", "luzon",
    "butuan", "pampanga", "bulacan", "oriental mindoro", "occidental mindoro",
    "cebu province", "iloilo city", "negros", "negros occidental", "negros oriental",
    "iloilo", "bicol", "palawan", "marikina", "iloilo",
]


def is_philippines_location(location: Optional[str], posting_url: Optional[str] = None,
                           description: Optional[str] = None, country: Optional[str] = None) -> bool:
    """Return True when the supplied fields strongly indicate the Philippines.

    Heuristics used (order matters):
    - explicit country match (e.g., country == 'Philippines' or 'PH')
    - .ph domain in posting_url
    - any PH token appears in location or description (case-insensitive)
    - phrases like 'remote (philippines)' or 'work from philippines'

    This is intentionally conservative: if uncertain, return False.
    """
    loc = (location or "").lower()
    url = (posting_url or "").lower()
    desc = (description or "").lower()
    c = (country or "").lower()

    # Country field check (exact match/starts-with)
    if c:
        if "philippin" in c or c in ("ph", "philippines", "phil"):
            return True

    # URL domain (.ph) or explicit 'philippines' in url
    if ".ph" in url or "philippines" in url:
        return True

    # Look for 'remote' paired with philippines in either loc or desc
    if "remote" in loc and "philippin" in loc:
        return True
    if "remote" in desc and "philippin" in desc:
        return True

    # Check canonical tokens inside location or description
    for token in PH_TOKENS:
        if token in loc:
            return True
        if token in desc:
            return True

    return False
