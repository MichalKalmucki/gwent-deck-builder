from src.models.deck import Deck
from src.genetic.models.rule import Rule
import pandas as pd


class RuleSet:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def apply(self, deck: Deck, card_pool: pd.DataFrame) -> tuple[Deck, int]:
        new_deck = Deck(
            leader_ability=deck.leader_ability,
            stratagem=deck.stratagem,
            cards=deck.cards.copy(),
            faction=deck.faction,
        )

        applied_count = 0
        for rule in self.rules:
            if rule.apply(new_deck, card_pool):
                applied_count += 1

        return new_deck, applied_count
