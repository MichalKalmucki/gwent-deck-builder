from src.models.deck import Deck
from src.models.card import Card
import pandas as pd


class Rule:
    def __init__(self, conditions: dict, action: dict):
        self.conditions = (
            conditions  # e.g., {'leader': 'Uprising', 'has_card': 'Draug'}
        )
        self.action = action  # e.g., {'add_card': 'Reinforcements'}

    def is_satisfied(self, deck: Deck) -> bool:
        for key, value in self.conditions.items():
            if key == "leader" and deck.leader_ability != value:
                return False
            if key == "stratagem" and deck.stratagem != value:
                return False
            if key == "has_card":
                if not any(card.id == value for card in deck.cards):
                    return False
            if key == "not_has_card":
                if any(card.id == value for card in deck.cards):
                    return False
        return True

    def apply(self, deck: Deck, card_pool: pd.DataFrame) -> bool:
        if not self.is_satisfied(deck):
            return False

        card_id = self.action.get("add_card")
        if not card_id or len(deck.cards) >= 25:
            return False

        card_row = card_pool.loc[card_pool["id"] == card_id]
        if card_row.empty:
            return False

        provision = int(card_row.iloc[0]["provision"])
        card = Card(
            id=card_row.iloc[0]["id"],
            name=card_row.iloc[0]["name"],
            provision=provision,
            group=card_row.iloc[0]["group"],
            type=card_row.iloc[0]["type"],
            faction=card_row.iloc[0]["faction"],
            secondary_faction=card_row.iloc[0].get("secondary_faction"),
        )

        deck.cards.append(card)
        if not deck.is_feasible():
            deck.cards.pop()
            return False

        return True
