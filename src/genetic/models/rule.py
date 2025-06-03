from src.models.deck import Deck
from src.models.card import Card
from src.models.faction import Faction
import pandas as pd
import random


class Rule:
    def __init__(self, conditions: dict, action: dict):
        self.conditions = (
            conditions  # e.g., {'leader': 'Uprising', 'has_card': 'Draug'}
        )
        self.action = action  # e.g., {'add_card': 'Reinforcements'}

    def __repr__(self):
        cond_str = ", ".join(f"{k}={v!r}" for k, v in self.conditions.items())
        action_str = ", ".join(f"{k}={v!r}" for k, v in self.action.items())
        return f"<Rule(conditions={{ {cond_str} }}, action={{ {action_str} }})>"

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


def create_random_rule(
    card_pool: pd.DataFrame, factions: list[Faction], stratagems: list
):
    """
    Generates a random rule for the evolutionary algorithm to apply when building decks.

    The rule consists of conditions based on a randomly selected faction and one of its leaders,
    optionally a stratagem, leftover provision range, and optionally a 'has_card' condition.
    The action is to add a randomly selected card compatible with the chosen faction.

    Args:
        card_pool (pd.DataFrame): DataFrame containing all available cards with their attributes.
        factions (list[Faction]): List of Faction objects to sample faction and leader from.
        stratagems (list): List of available stratagems to condition on.

    Returns:
        Rule: A Rule object containing the generated conditions and the action to add a card.
    """
    faction = random.choice(factions)
    leader = random.choice(list(faction.leader_abilities.keys()))

    conditions = {"leader": leader}

    # TODO: implement stratagem class and relation with Faction class (each faction has 1 own specific stratagem apart from neutrals)
    # if random.random() < 1 and stratagems:
    #     conditions["stratagem"] = random.choice(stratagems)

    max_leftover = 150
    leftover_min = random.randint(0, max_leftover)
    leftover_max = random.randint(leftover_min, max_leftover)
    conditions["leftover_provision_min"] = leftover_min
    conditions["leftover_provision_max"] = leftover_max

    candidates = card_pool[
        (card_pool["faction"] == faction.name)
        | (card_pool["faction"] == "neutral")
        | (card_pool["secondary_faction"] == faction.name)
    ]
    if candidates.empty:
        candidates = card_pool

    if random.random() < 0.5:
        has_card_candidate = candidates.sample(1).iloc[0]
        card_id = has_card_candidate.name
        conditions["has_card"] = card_id

    card_row = candidates.sample(1).iloc[0]
    card_id = card_row.name

    action = {"add_card": card_id}

    return Rule(conditions=conditions, action=action)
