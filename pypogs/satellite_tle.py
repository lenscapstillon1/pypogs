import requests

def fetch_tle_from_celestrak(norad_id, category='gp.php?GROUP=active&FORMAT=tle'):
    """
    Fetch TLE for a specific NORAD ID from Celestrak.
    :param norad_id: Satellite NORAD catalog number (int or str)
    :param category: Celestrak endpoint (default: gp.php?GROUP=active&FORMAT=tle)
    :return: Tuple (name, line1, line2) or None if not found
    """
    url = f"https://celestrak.com/NORAD/elements/{category}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.strip().split('\n')
        for i in range(0, len(lines), 3):
            if len(lines) - i < 3:
                break
            name = lines[i].strip()
            line1 = lines[i+1].strip()
            line2 = lines[i+2].strip()
            if str(norad_id) in line1[2:7]:
                return (name, line1, line2)
        return None
    except Exception as e:
        print(f"Error fetching TLE: {e}")
        return None

def fetch_all_tles(norad_ids, category='gp.php?GROUP=active&FORMAT=tle'):
    """
    Fetch TLEs for multiple NORAD IDs.
    :return: dict of {norad_id: (name, line1, line2)}
    """
    tles = {}
    for nid in norad_ids:
        tle = fetch_tle_from_celestrak(nid, category)
        if tle:
            tles[nid] = tle
    return tles