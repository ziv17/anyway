import json
from typing import Iterable, Dict, Any, List, Tuple
from anyway.models import Streets
from anyway.app_and_db import db
import logging
import Levenshtein
import pandas as pd
import copy


OSM_STREETS_FN = '/mnt/c/Users/ZHARPAZ/Downloads/osm_streets.csv'


def find_closest_strings(streets: List[dict], osm_streets: List[dict]) -> List[dict]:
    osm_streets_dict = {x["name:he"]: x for x in osm_streets if "name:he" in x and pd.notna(x["name:he"])}
    closest_matches = []
    for street in streets:
        string_a = street.street_hebrew
        closest_match = min(osm_streets_dict.keys(), key=lambda osm_street: Levenshtein.distance(string_a, osm_street))
        osm = copy.copy(osm_streets_dict[closest_match])
        osm.pop("name:ar", None)  # Remove the Hebrew name to avoid duplication
        osm.update({"cbs_heb_name": street.street_hebrew, "cbs_code": street.street, "dist": Levenshtein.distance(string_a, closest_match)})
        closest_matches.append(osm)
    print(f"Found {len(closest_matches)} closest matches from {len(streets)} cbs streets.")
    return closest_matches


def load_streets() -> List[Streets]:
    res = db.session.query(Streets).filter(Streets.yishuv_symbol == 5000).all()
    return res


def load_osm_streets(filename: str = OSM_STREETS_FN) -> List:
    """
    Load streets data from a CSV file and return it as a DataFrame.

    :param filename: Path to the CSV file containing streets data.
    :return: DataFrame containing the streets data.
    """
    try:
        df = pd.read_csv(filename, encoding="utf-8")
        res = [x for x in df.to_dict(orient="records") if pd.notna(x["name:he"])]
        logging.info(f"Loaded {len(res)} streets from {filename}.")
        return res
    except Exception as e:
        logging.error(f"Error loading streets data from {filename}: {e}")
        raise


def main():
    # Example usage
    streets = load_streets()
    street_names = [street.street_hebrew for street in streets]
    osm_streets = load_osm_streets(OSM_STREETS_FN)
    found = find_closest_strings(osm_streets=osm_streets, streets=streets)
    output_filename = "matched_streets.csv"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(",".join(found[0].keys()) + "\n")
        for street in found:
            f.write(f"{','.join(map(str, street.values()))}\n")
    print(f"Matched streets written to {output_filename}")

if __name__ == "__main__":
    main()
