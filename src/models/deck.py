from src.models.card import Card
from typing import List
import json
import pandas as pd


from collections import Counter


class Deck:
    def __init__(self, leader_ability: str, stratagem: str, cards: list, faction):
        """
        Represents a Gwent deck.

        Args:
            leader_ability (str): The leader ability used in the deck.
            stratagem (str): The stratagem selected for the deck.
            cards (list[Card]): A list of Card objects included in the deck.
            faction (Faction): The faction the deck belongs to.
        """
        self.leader_ability = leader_ability
        self.stratagem = stratagem
        self.cards = cards
        self.faction = faction

    def __repr__(self):
        return (
            f"Leader: {self.leader_ability}, Stratagem: {self.stratagem}, "
            f"Cards: {len(self.cards)} cards"
        )

    def is_feasible(self) -> bool:
        """
        Validates the deck against faction rules and leader ability constraints.

        Returns:
            bool: True if the deck meets all constraints, False otherwise.
        """
        if self.leader_ability not in self.faction.leader_abilities:
            return False

        provision_limit = self.faction.leader_abilities[self.leader_ability] + 150
        total_provision = sum(card.provision for card in self.cards)
        if total_provision > provision_limit:
            print("Provision limit exceeded")
            return False

        if len(self.cards) != 25:
            print("Deck length mismatch")
            return False

        unit_count = sum(1 for card in self.cards if card.type == "unit")
        if unit_count < 13:
            print("Too few units")
            return False

        count_by_id = Counter(card.id for card in self.cards)
        for card in self.cards:
            count = count_by_id[card.id]
            if card.group == "bronze" and count > 2:
                print("More than 2 copies of a bronze card")
                return False
            if card.group == "gold" and count > 1:
                print("More than 1 copy of a gold card")
                return False

            if card.faction != self.faction.name:
                if (
                    card.faction != "neutral"
                    and card.secondary_faction != self.faction.name
                ):
                    print(
                        f"Card: {card.name} faction not matching leader ability "
                        f"({card.faction}, {card.secondary_faction})"
                    )
                    return False

        return True


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
