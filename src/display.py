import random
import os
import pandas as pd
import json


def print_random_deck(card_df: pd.DataFrame):
    """
    Prints details of a random deck, including the leader, stratagem, and cards used.

    This function:
    - Selects a random deck JSON file from the `data/decks` folder
    - Loads the deck's data, including the leader, stratagem, and cards
    - For each card in the deck, retrieves its details from the provided card DataFrame (`card_df`)
    - Prints out the name and count of each card, and the total number of cards in the deck

    Args:
        card_df (pd.DataFrame): A DataFrame containing card metadata, indexed by card ID.

    Outputs:
        - Prints deck leader, stratagem, and card names with counts.
        - Prints the total number of cards in the deck.
    """

    decks_path = "data/decks"
    deck_files = os.listdir(decks_path)
    deck_json_files = [file for file in deck_files if file.endswith(".json")]
    random_deck_file = random.choice(deck_json_files)

    with open(os.path.join(decks_path, random_deck_file), "r") as file:
        deck_data = json.load(file)

    print(deck_data["Leader"])
    print(deck_data["Stratagem"])
    print()
    total_cards = 0
    for card in deck_data["Cards"]:
        card_id = card["id"]
        card_info = card_df.loc[card_id]
        print(f"{card_info['name']}: {card['count']}")
        total_cards += card["count"]
    print(f"Total cards: {total_cards}")
