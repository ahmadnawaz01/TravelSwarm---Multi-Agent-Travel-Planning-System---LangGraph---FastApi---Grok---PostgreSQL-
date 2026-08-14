import os
import re
import certifi
import airportsdata
import pycountry
import requests
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "LHE")
BASE_URL = "https://api.aviationstack.com/v1/flights"


AIRPORTS = airportsdata.load("IATA")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "LHE") 


COUNTRY_MAIN_AIRPORT = {
    "PK": "LHE", 
    "BD": "DAC",
    "IN": "DEL", 
    "JP": "NRT",  
    "US": "JFK",                        
    "GB": "LHR",             
    "AE": "DXB", 
    "SA": "JED",  
    "QA": "DOH", 
    "TH": "BKK",  
}


COUNTRY_ALIASES = {
    "usa": "US", "u.s.a": "US", "america": "US", "united states": "US",
    "uk": "GB", "britain": "GB", "england": "GB",
    "uae": "AE", "dubai": "AE",
    "south korea": "KR", "korea": "KR",
    "pakistan": "PK", "india": "IN", "bangladesh": "BD", "japan": "JP"
}

def clean_text(text: str) -> str:
    """Normalizes text by removing non-alphanumeric chars and stop words."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    stop_words = {"flight", "flights", "ticket", "tickets", "trip", "travel", "plan", "days", "under", "budget"}
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words).strip()



def resolve_location_to_iata(location: str) -> str | None:
    if not location:
        return None
    
    raw_loc = location.strip().upper()
    if len(raw_loc) == 3 and raw_loc in AIRPORTS:
        return raw_loc
    
    loc_clean = clean_text(location)
    if not loc_clean:
        return None

    iso_code = COUNTRY_ALIASES.get(loc_clean)
    if not iso_code:
        try:
            iso_code = pycountry.countries.lookup(loc_clean).alpha_2
        except LookupError:
            iso_code = None

    if iso_code and iso_code in COUNTRY_MAIN_AIRPORT:
        return COUNTRY_MAIN_AIRPORT[iso_code]

    candidates = []
    for iata, airport in AIRPORTS.items():
        score = 0
        apt_country = airport.get("country", "").upper()
        apt_city = airport.get("city", "").lower()
        apt_name = airport.get("name", "").lower()

        if iso_code and apt_country == iso_code:
            score += 40

        if loc_clean in apt_city:
            score += 50
        elif apt_city and apt_city in loc_clean:
            score += 30

        if score > 0:
            if "lahore" in apt_name or "lahore" in apt_city:
                score += 30
            if "international" in apt_name or "intl" in apt_name:
                score += 20
            candidates.append((score, iata))

    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]

    return None

def parse_route(query: str):
    """Parses origin and destination IATA codes from query string."""
    q_lower = query.lower().strip()

    if any(k in q_lower for k in ["all country", "global flight", "all flights"]):
        return None, None

    match = re.search(r"\bfrom\s+(.+?)\s+\bto\s+(.+?)(?:\s+under|\s+for|\s+in|\.|$)", q_lower)
    if match:
        dep = resolve_location_to_iata(match.group(1))
        arr = resolve_location_to_iata(match.group(2))
        return dep, arr

    match = re.search(r"\bto\s+(.+?)\s+\bfrom\s+(.+?)(?:\s+under|\s+for|\s+in|\.|$)", q_lower)
    if match:
        arr = resolve_location_to_iata(match.group(1))
        dep = resolve_location_to_iata(match.group(2))
        return dep, arr

    match_to = re.search(r"\bto\s+(.+?)(?:\s+under|\s+for|\s+in|\.|$)", q_lower)
    if match_to:
        arr = resolve_location_to_iata(match_to.group(1))
        return DEFAULT_ORIGIN_IATA, arr

    return None, None

def format_flight(flight: dict) -> str:
    """Formats a single flight API object into structured Markdown text."""
    airline = flight.get("airline", {}).get("name") or "Unknown Airline"
    flight_num = flight.get("flight", {}).get("iata") or "N/A"
    status = flight.get("flight_status", "N/A").capitalize()

    dep = flight.get("departure", {}) or {}
    arr = flight.get("arrival", {}) or {}

    return (
        f"**Airline:** {airline} ({flight_num})\n"
        f"**Status:** {status}\n"
        f"**Departure:** {dep.get('airport', 'N/A')} ({dep.get('iata', 'N/A')}) | Gate: {dep.get('gate', 'N/A')} | Time: {dep.get('scheduled', 'N/A')}\n"
        f"**Arrival:** {arr.get('airport', 'N/A')} ({arr.get('iata', 'N/A')}) | Gate: {arr.get('gate', 'N/A')} | Time: {arr.get('scheduled', 'N/A')}"
    )

def search_flights(query: str, limit: int = 5) -> str:
    if not API_KEY:
        return "Flight API error: AVIATIONSTACK_API_KEY is missing from environment variables."

    dep_iata, arr_iata = parse_route(query)

    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }
    if dep_iata:
        params["dep_iata"] = dep_iata
    if arr_iata:
        params["arr_iata"] = arr_iata

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        data = response.json()
    except Exception as e:
        return f"Flight API request failed: {e}"

    if "error" in data:
        err = data["error"]
        return f"Flight API Error [{err.get('code')}]: {err.get('message')}"

    flight_data = data.get("data", [])
    if not flight_data:
        route_str = f"from {dep_iata} to {arr_iata}" if (dep_iata and arr_iata) else "for this selection"
        return f"No live flight data found {route_str}."

    formatted = [format_flight(f) for f in flight_data[:limit]]
    return "\n\n---\n\n".join(formatted)

if __name__ == "__main__":
    print(search_flights("Plan a 7 days Japan trip from Pakistan"))