import random
import pandas as pd
from src.models.deck import Deck
from src.genetic.fitness import *

def add_card_uniform(deck: Deck, card_pool):
    """
    Attempts to add one randomly chosen card to the deck using uniform distribution.
    Returns the updated deck or the original if no feasible addition found.
    """
    if len(deck) >= 25:
        return deck

    shuffled = card_pool[:]
    random.shuffle(shuffled)

    deck_copy = Deck(deck.leader_ability, deck.stratagem, deck.cards, deck.faction)
    for card in shuffled:
        deck_copy.cards.extend(card)
        if deck_copy.is_feasible():
            return deck_copy
        else: 
            deck_copy.cards.pop()

    return deck

def add_card_bayesian(deck: Deck, card_pool):
    """
    Attempts to add one card using a simple Bayesian update based on prior frequencies.
    prior_counts: a dictionary of card -> count (based on previous successful decks)
    """
    if len(deck) >= 25:
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

    return deck

