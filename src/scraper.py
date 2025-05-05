import requests
from bs4 import BeautifulSoup
import json
import html
import pandas as pd
import random
import time
import ast
from tqdm import tqdm


def __get_sublinks():
    """
    Fetches Gwent deck guide links from the official Gwent decks page.

    Returns:
        list[str]: A list of full URLs pointing to individual deck guide pages.

    Raises:
        json.JSONDecodeError: If the embedded JSON data cannot be decoded.
        KeyError: If the expected "guides" key is not found in the decoded data.
    """
    headers = {"User-Agent": "Mozilla/5.0"}

    main_url = "https://www.playgwent.com/en/decks/"
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    div = soup.find("div", attrs={"data-state": True})

    raw_data = div["data-state"]
    decoded = html.unescape(raw_data)

    try:
        data = json.loads(decoded)
    except json.JSONDecodeError as e:
        print("JSON decode failed:", e)
        print(decoded[:500])
        raise

    if isinstance(data, dict) and "guides" in data:
        guides = data["guides"]
        deck_links = [
            f"https://www.playgwent.com/en/decks/guides/{guide['id']}"
            for guide in guides
        ]
    else:
        print("Unexpected JSON structure")

    return deck_links


def scrape_gwent_data(sleep: bool = False):
    """
    Scrapes deck data and card metadata from Gwent's official decks page.

    This function:
    - Retrieves deck guide links via __get_sublinks()
    - Downloads each deck’s JSON structure and saves it locally
    - Builds a card database of unique cards used across all decks
    - Converts 'secondaryFactions' to readable strings using a predefined map
    - Exports the card database to a CSV file

    Args:
        sleep (bool): If True, introduces a random delay (1–3 seconds) between requests to avoid rate-limiting.

    Outputs:
        - Saves deck JSON files to `data/decks/`
        - Saves the full card database to `data/card_database.csv`
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    card_database = {}
    deck_links = __get_sublinks()

    for i, deck_url in enumerate(tqdm(deck_links, desc="Processing decks"), 1):
        res = requests.get(deck_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        div = soup.find("div", attrs={"data-state": True})
        raw = html.unescape(div["data-state"])
        data = json.loads(raw)

        deck_data = data["guide"]["deck"]
        cards = deck_data["cards"]
        leader = deck_data["leader"]["name"]
        stratagem = deck_data["stratagem"]["name"]

        deck_json = {
            "Leader": leader,
            "Stratagem": stratagem,
            "Cards": [
                {"id": card["id"], "count": card["repeatCount"] + 1} for card in cards
            ],
        }
        with open(f"data/decks/{i}.json", "w", encoding="utf-8") as f:
            json.dump(deck_json, f, indent=4, ensure_ascii=False)

        for card in cards:
            card_id = card.get("id")
            if card_id not in card_database:
                card_database[card_id] = {
                    "id": card_id,
                    "name": card.get("name"),
                    "provision": card.get("provisionsCost"),
                    "group": card.get("cardGroup"),
                    "type": card.get("type"),
                    "faction": card.get("faction", {}).get("slug"),
                    "secondary_faction": card.get("secondaryFactions"),
                }

        if sleep:
            time.sleep(random.uniform(1, 3))

    card_df = pd.DataFrame.from_dict(card_database, orient="index").reset_index(
        drop=True
    )

    # gwent page has weird way of saving secondary factions with non given enum
    faction_map = {
        1: "monsters",
        2: "nilfgard",
        3: "northernrealms",
        4: "scoiatael",
        5: "skellige",
    }

    def parse_secondary_faction(faction_str):
        try:
            faction_data = ast.literal_eval(faction_str)
            if faction_data and isinstance(faction_data, list):
                faction_value = faction_data[0].get("value")
                return faction_map.get(faction_value, "")
        except (ValueError, SyntaxError):
            return ""
        return ""

    card_df["secondary_faction"] = card_df["secondary_faction"].apply(
        parse_secondary_faction
    )

    card_df.to_csv("data/card_database.csv", index=False)
