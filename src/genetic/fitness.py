import pandas as pd
import os
import json
import numpy as np
from collections import defaultdict
from src.models.deck import Deck


class Fitness:
    """
    ## A class to evaluate the synergy and quality of Gwent decks using co-occurrence and usage data.

    This class internally loads card metadata and computes several private co-occurrence statistics:
    - Normalized card-to-card co-occurrence matrix based on historical deck data.
    - Normalized co-occurrence of cards with leader abilities.
    - Normalized co-occurrence of cards with stratagems.
    - Normalized card usage frequencies.

    The core functionality is to calculate a fitness score for a given deck. The score reflects:
    - Synergy between card pairs.
    - Overall popularity and frequency of individual cards.
    - Compatibility of cards with the selected leader ability.
    - Compatibility of cards with the selected stratagem.

    ### Methods:
        fitness(deck: Deck) -> float:
            Computes the fitness score of a deck by aggregating synergy, popularity,
            and alignment with leader ability and stratagem.
    """

    def __init__(self):
        self.__card_occurances = self.__calculate_card_ocurance()
        self.__normalized_occurances = self.__normalize_card_occurances(
            self.__card_occurances
        )
        self.__cooccurrence_matrix = self.__calculate_card_cooccurrence_matrix(
            self.__normalized_occurances
        )
        self.__card_leader_cooccurrence = self.__calculate_card_leader_cooccurrence()
        self.__card_stratagem_cooccurrence = (
            self.__calculate_card_stratagem_cooccurrence()
        )

    def fitness(self, deck: Deck) -> float:
        """
        Calculates the fitness score of a deck based on:
        - Co-occurrence between card pairs
        - Frequency of cards
        - Co-occurrence between each card and the deck's leader
        - Co-occurrence between each card and the deck's stratagem

        Args:
            deck (Deck): Deck object containing leader ability, stratagem, and cards.

        Returns:
            float: Fitness score.
        """
        score = 0
        card_frequency = {}
        for card in deck.cards:
            card_frequency[card.id] = card_frequency.get(card.id, 0) + 1

        leader = deck.leader_ability
        stratagem = deck.stratagem

        for i in range(len(deck.cards)):
            card_i = deck.cards[i].id
            card_i_count = card_frequency.get(card_i, 0)
            score += card_i_count

            leader_score = self.__card_leader_cooccurrence.get(card_i, {}).get(
                leader, 0
            )
            stratagem_score = self.__card_stratagem_cooccurrence.get(card_i, {}).get(
                stratagem, 0
            )

            score += leader_score
            score += stratagem_score

            for j in range(i + 1, len(deck.cards)):
                card_j = deck.cards[j].id
                if (
                    card_i in self.__cooccurrence_matrix.index
                    and card_j in self.__cooccurrence_matrix.columns
                ):
                    score += self.__cooccurrence_matrix.loc[card_i, card_j]

        return score

    def __read_card_df(self):
        card_df = pd.read_csv("data/card_database.csv")
        card_df.set_index("id", inplace=True)
        return card_df

    def __calculate_card_ocurance(self, deck_dir: str = "data/decks"):
        """
        Counts the total occurrences of each card across all deck JSON files in the given directory.

        Args:
            deck_dir (str, optional): Path to the directory containing deck JSON files.
                                    Defaults to "data/decks".

        Returns:
            dict: A dictionary mapping card IDs to their raw occurrence counts.
        """
        card_occurrences = {}

        deck_files = os.listdir(deck_dir)
        deck_json_files = [file for file in deck_files if file.endswith(".json")]

        for deck_file in deck_json_files:
            with open(os.path.join(deck_dir, deck_file), "r") as file:
                deck_data = json.load(file)

            for card in deck_data["Cards"]:
                card_id = card["id"]
                card_occurrences[card_id] = card_occurrences.get(card_id, 0) + 1

        return card_occurrences

    def __normalize_card_occurances(self, card_occurrences: dict):
        """
        Normalizes card occurrence counts by applying logarithmic scaling relative to the
        highest occurrence count, resulting in values between 0 and 1.

        Args:
            card_occurrences (dict): A dictionary mapping card IDs to their raw occurrence counts.

        Returns:
            dict: A dictionary mapping card IDs to their normalized occurrence scores.
        """
        top_occurring = max(card_occurrences.items(), key=lambda x: x[1])

        normalized_occurrences = {
            card: np.log(1 + count) / np.log(1 + top_occurring[1])
            for card, count in card_occurrences.items()
        }

        return normalized_occurrences

    def __calculate_card_cooccurrence_matrix(
        card_frequency: dict, deck_dir: str = "data/decks"
    ):
        """
        Generates a co-occurrence matrix of cards based on decks in the specified directory.
        Divides the co-occurrence counts by the frequency of the most frequent card.

        Args:
            card_df (pd.DataFrame): A DataFrame containing card metadata, indexed by card ID.
            deck_dir (str): Directory containing deck JSON files.

        Returns:
            np.ndarray: A co-occurrence matrix where each entry (i, j) represents the co-occurrence
                        count of card i and card j across all decks, normalized by card frequency.
        """
        card_cooccurrence = {}

        deck_files = os.listdir(deck_dir)
        deck_json_files = [file for file in deck_files if file.endswith(".json")]

        for deck_file in deck_json_files:
            with open(os.path.join(deck_dir, deck_file), "r") as file:
                deck_data = json.load(file)

            card_ids = [card["id"] for card in deck_data["Cards"]]

            for i in range(len(card_ids)):
                for j in range(i + 1, len(card_ids)):
                    card_i, card_j = card_ids[i], card_ids[j]

                    if card_i not in card_cooccurrence:
                        card_cooccurrence[card_i] = {}
                    if card_j not in card_cooccurrence[card_i]:
                        card_cooccurrence[card_i][card_j] = 0
                    card_cooccurrence[card_i][card_j] += 1

                    if card_j not in card_cooccurrence:
                        card_cooccurrence[card_j] = {}
                    if card_i not in card_cooccurrence[card_j]:
                        card_cooccurrence[card_j][card_i] = 0
                    card_cooccurrence[card_j][card_i] += 1

        for card_i in card_cooccurrence:
            for card_j in card_cooccurrence[card_i]:
                card_cooccurrence[card_i][card_j] /= max(
                    card_frequency.get(card_i, 1), card_frequency.get(card_j, 1)
                )

        # Create a DataFrame from the dictionary
        cooccurrence_matrix = pd.DataFrame.from_dict(
            {
                card_id: pd.Series(card_cooccurrence.get(card_id, {}))
                for card_id in card_cooccurrence
            },
            orient="index",
        ).fillna(0)

        return cooccurrence_matrix

    def __calculate_card_leader_cooccurrence(deck_dir: str = "data/decks"):
        """
        Calculates and normalizes the co-occurrence frequency between cards and leader abilities
        across all deck JSON files in the specified directory.

        For each card, the function counts how many times it appears alongside each leader ability
        in the decks. Then, it normalizes these counts by dividing each card-leader count by the total
        occurrences of that card across all leaders, resulting in normalized values between 0 and 1.

        Args:
            deck_dir (str, optional): Path to the directory containing deck JSON files.
                                    Defaults to "data/decks".

        Returns:
            defaultdict: A nested dictionary where the outer keys are card IDs,
                        and the inner dictionaries map leader abilities to the normalized co-occurrence values.
                        Format: {card_id: {leader: normalized_cooccurrence, ...}, ...}
        """
        raw_counts = defaultdict(lambda: defaultdict(int))

        deck_files = os.listdir(deck_dir)
        deck_json_files = [file for file in deck_files if file.endswith(".json")]

        for deck_file in deck_json_files:
            with open(os.path.join(deck_dir, deck_file), "r") as file:
                deck_data = json.load(file)

            leader = deck_data.get("Leader", "Unknown")

            for card in deck_data.get("Cards", []):
                card_id = card["id"]
                count = card.get("count", 1)
                raw_counts[card_id][leader] += count

        normalized_counts = defaultdict(dict)

        for card_id, leaders in raw_counts.items():
            total = sum(leaders.values())
            if total == 0:
                continue
            for leader, count in leaders.items():
                normalized_counts[card_id][leader] = count / total

        return normalized_counts

    def __calculate_card_stratagem_cooccurrence(deck_dir: str = "data/decks"):
        """
        Calculates and normalizes the co-occurrence frequency between cards and stratagems
        across all deck JSON files in the specified directory.

        For each card, this function counts how many times it appears alongside each stratagem
        in the decks. It then normalizes these counts by dividing each card-stratagem count
        by the total occurrences of that card across all stratagems, resulting in normalized
        values between 0 and 1.

        Args:
            deck_dir (str, optional): Path to the directory containing deck JSON files.
                                    Defaults to "data/decks".

        Returns:
            defaultdict: A nested dictionary where outer keys are card IDs, and inner dictionaries
                        map stratagem names to normalized co-occurrence values.
                        Format: {card_id: {stratagem: normalized_cooccurrence, ...}, ...}
        """
        raw_counts = defaultdict(lambda: defaultdict(int))

        deck_files = os.listdir(deck_dir)
        deck_json_files = [file for file in deck_files if file.endswith(".json")]

        for deck_file in deck_json_files:
            with open(os.path.join(deck_dir, deck_file), "r") as file:
                deck_data = json.load(file)

            stratagem = deck_data.get("Stratagem", "Unknown")

            for card in deck_data.get("Cards", []):
                card_id = card["id"]
                count = card.get("count", 1)
                raw_counts[card_id][stratagem] += count

        normalized_counts = defaultdict(dict)

        for card_id, stratagems in raw_counts.items():
            total = sum(stratagems.values())
            if total == 0:
                continue
            for stratagem, count in stratagems.items():
                normalized_counts[card_id][stratagem] = count / total

        return normalized_counts
