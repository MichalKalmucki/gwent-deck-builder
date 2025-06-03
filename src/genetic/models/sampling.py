import random
import pandas as pd
from src.models.deck import Deck
from src.genetic.fitness import *
from src.models.card import Card


def add_card_uniform(deck: Deck, card_pool: pd.DataFrame) -> bool:
    """
    Attempts to add one randomly chosen card from card_pool to the deck.
    Modifies the deck in-place if a feasible card is found.

    Returns:
        bool: True if a card was added, False otherwise.
    """
    if len(deck.cards) >= 25:
        return False

    cards = card_pool.reset_index().to_dict("records")  # <-- brings 'id' back as column
    random.shuffle(cards)

    for card_row in cards:
        # print(card_row)
        card = Card(
            id=card_row["id"],
            name=card_row["name"],
            provision=int(card_row["provision"]),
            group=card_row["group"],
            type=card_row["type"],
            faction=card_row["faction"],
            secondary_faction=card_row.get("secondary_faction"),
        )
        deck.cards.append(card)
        if deck.is_feasible():
            return True
        else:
            deck.cards.pop()

    return False


def add_card_bayesian(deck: Deck, card_pool):
    """
    Attempts to add one card using a simple Bayesian update based on prior frequencies.
    prior_counts: a dictionary of card -> count (based on previous successful decks)
    """
    if len(deck.cards) >= 25:
        return deck

    fit = Fitness()
    norm_counts = fit.__normalized_occurances

    deck_copy = Deck(deck.leader_ability, deck.stratagem, deck.cards, deck.faction)

    attempts = 100
    for _ in range(attempts):
        card = random.choices(card_pool, weights=norm_counts, k=1)[0]
        deck_copy.cards.extend(card)
        if deck_copy.is_feasible():
            return deck_copy
        else:
            deck_copy.cards.pop()
    deck_copy = add_card_uniform(deck, card_pool)

    return deck_copy
