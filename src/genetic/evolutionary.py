from src.genetic.models.rule_set import (
    create_random_rule_set,
    print_ruleset_with_names,
    crossover,
)
from src.genetic.evaluate import evaluate_rule_set
import random
from tqdm import tqdm
import pickle


def evolutionary_algorithm(
    card_df,
    factions,
    stratagems,
    fitness_evaluator,
    population_size=20,
    generations=50,
    rule_count=100,
    mutation_rate=0.2,
    crossover_rate=0.3,
    tournament_size=3,
):
    population = [
        create_random_rule_set(card_df, factions, stratagems, rule_count)
        for _ in range(population_size)
    ]

    for gen in range(generations):
        print(f"--- Generation {gen} ---")
        fitness_scores = []
        for rs in tqdm(population, desc="Evaluating population"):
            score = evaluate_rule_set(rs, card_df, factions, stratagems, fitness_evaluator)
            fitness_scores.append((score, rs))

        fitness_scores.sort(reverse=True, key=lambda x: x[0])
        print(f"Best fitness: {fitness_scores[0][0]:.4f}")
        best_ruleset = fitness_scores[0][1]
        print_ruleset_with_names(best_ruleset, card_df)

        # Save best ruleset to file
        with open(f"rulesets/best_ruleset_gen_{gen}.pkl", "wb") as f:
            pickle.dump(best_ruleset, f)

        def select_parent():
            contenders = random.sample(fitness_scores, tournament_size)
            return max(contenders, key=lambda x: x[0])[1]

        new_population = [best_ruleset]
        while len(new_population) < population_size:
            parent1 = select_parent()
            parent2 = select_parent()

            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1

            if random.random() < mutation_rate:
                child = child.mutate(card_df, factions, stratagems)

            new_population.append(child)

        population = new_population

    final_fitness_scores = []
    for rs in tqdm(population, desc="Final evaluation"):
        score = evaluate_rule_set(rs, card_df, factions, stratagems, fitness_evaluator)
        final_fitness_scores.append((score, rs))

    final_fitness_scores.sort(reverse=True, key=lambda x: x[0])
    best_final = final_fitness_scores[0][1]

    print("\n=== Final Best RuleSet ===")
    print_ruleset_with_names(best_final, card_df)
    print(f"Final fitness: {final_fitness_scores[0][0]:.4f}")

    return best_final


