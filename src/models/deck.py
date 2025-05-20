from src.models.card import Card
from typing import List
import json
import pandas as pd


class Deck:
    def __init__(self, leader_ability: str, stratagem: str, cards: list):
        """
        Represents a Gwent deck.

        Args:
            leader_ability (str): The leader ability used in the deck.
            stratagem (str): The stratagem selected for the deck.
            cards (list[Card]): A list of Card objects included in the deck.
        """
        self.leader_ability = leader_ability
        self.stratagem = stratagem
        self.cards = cards

    def __repr__(self):
        return (
            f"Leader: {self.leader_ability}, Stratagem: {self.stratagem}, "
            f"Cards: {len(self.cards)} cards"
        )


def load_deck_from_json(deck_path: str, card_df: pd.DataFrame) -> Deck:
    """
    Loads a deck from a JSON file and returns a Deck object.

    Args:
        deck_path (str): Path to the JSON file containing the deck data.
        card_df (pd.DataFrame): DataFrame with card metadata indexed by card ID.

    Returns:
        Deck: A Deck object with leader, stratagem, and a list of Card objects.
    """
    with open(deck_path, "r") as file:
        deck_data = json.load(file)

    leader = deck_data["Leader"]
    stratagem = deck_data["Stratagem"]
    cards: List[Card] = []

    for card_entry in deck_data["Cards"]:
        card_id = card_entry["id"]
        count = card_entry["count"]

        if card_id not in card_df.index:
            continue

        card_info = card_df.loc[card_id]

        for _ in range(count):
            card = Card(
                id=card_id,
                name=card_info["name"],
                provision=card_info["provision"],
                group=card_info["group"],
                type=card_info["type"],
                faction=card_info["faction"],
                secondary_faction=card_info.get("secondary_faction", ""),
            )
            cards.append(card)

    return Deck(leader_ability=leader, stratagem=stratagem, cards=cards)
