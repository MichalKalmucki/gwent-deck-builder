from src.genetic.fitness import Fitness
from src.models.faction import Faction
from src.genetic.models.rule_set import RuleSet
from src.models.deck import Deck
from src.genetic.models.sampling import add_card_uniform
import pandas as pd
import random


def evaluate_rule_set(
    ruleset: RuleSet,
    card_pool: pd.DataFrame,
    factions: list[Faction],
    stratagems: list,
    fitness_evaluator: Fitness,
    n: int = 20,
) -> float:
    """
    Evaluates the average fitness of decks generated using a given RuleSet.

    For each of `n` iterations, this function:
    - Randomly selects a faction, leader, and stratagem
    - Builds a deck by applying the ruleset
    - Fills the remaining cards using the provided `add_card_uniform` function
    - Computes the fitness if the resulting deck is complete and feasible

    Args:
        ruleset (RuleSet): The rule set used to construct the decks.
        card_pool (pd.DataFrame): Available cards to build decks from.
        factions (list[Faction]): List of factions to sample from.
        stratagems (list): List of possible stratagems.
        fitness_evaluator (Fitness): Object for computing deck fitness.
        n (int): Number of sample decks to generate and evaluate.

    Returns:
        float: The average fitness score of the generated decks.
    """
    total_fitness = 0.0
    successful_decks = 0
    starting_deck_size = 10

    for _ in range(n):
        faction = random.choice(factions)
        leader = random.choice(list(faction.leader_abilities.keys()))
        stratagem = random.choice(stratagems)
        deck = Deck(
            leader_ability=leader,
            stratagem=stratagem,
            cards=[],
            faction=faction,
        )

        while len(deck.cards) < starting_deck_size:
            add_card_uniform(deck, card_pool)

        deck, applied_count = ruleset.apply(deck, card_pool)

        while len(deck.cards) < 25:
            if not add_card_uniform(deck, card_pool):
                break

        factor = applied_count / (25 - starting_deck_size)  # penelize not using rules

        if len(deck.cards) == 25 and deck.is_feasible():
            # print(f"CREATED DECK: {deck}")
            total_fitness += fitness_evaluator.fitness(deck) * factor
            successful_decks += 1

    return total_fitness
