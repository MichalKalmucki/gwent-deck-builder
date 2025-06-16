from src.scraper import scrape_gwent_data
from src.display import print_random_deck
from src.models.faction import get_factions
from src.genetic.models.rule_set import (
    create_random_rule_set,
    print_ruleset_with_names,
    crossover,
)
from src.genetic.evaluate import evaluate_rule_set
from src.genetic.fitness import Fitness
import pandas as pd
from src.genetic.evolutionary import evolutionary_algorithm


def main():
    # scrape_gwent_data()
    card_df = pd.read_csv("data/card_database.csv")
    card_df.set_index("id", inplace=True)
    print(card_df)
    # raise Exception
    stratagems = ["Tactical Advantage", "Enchanted Armor"]
    fitness_evaluator = Fitness()

    factions = get_factions()
    # rs = create_random_rule_set(card_df, factions, [], 10)
    # print_ruleset_with_names(rs, card_df)

    # # CROSSOVER
    # rs2 = create_random_rule_set(card_df, factions, [], 10)
    # print_ruleset_with_names(rs2, card_df)

    # rs_cross = crossover(rs, rs2)
    # print_ruleset_with_names(rs_cross, card_df)

    # # MUTATE
    # rs = rs.mutate(card_df, factions, stratagems, mutation_rate=0.1)
    # print_ruleset_with_names(rs, card_df)

    # # RULESET FITNESS
    # fitness = evaluate_rule_set(rs, card_df, factions, stratagems, fitness_evaluator)
    # print(fitness)

    # EVOLUTION
    best_ruleset = evolutionary_algorithm(
        card_df=card_df,
        factions=factions,
        stratagems=stratagems,
        fitness_evaluator=fitness_evaluator,
        population_size=20,
        generations=50,
        rule_count=100,
        mutation_rate=0.1,
        tournament_size=3,
    )
    print_ruleset_with_names(best_ruleset, card_df)


if __name__ == "__main__":
    main()
