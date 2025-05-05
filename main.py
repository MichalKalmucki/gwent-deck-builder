from src.scraper import scrape_gwent_data
from src.display import print_random_deck
import pandas as pd


def main():
    # scrape_gwent_data()
    card_df = pd.read_csv("data/card_database.csv")
    card_df.set_index("id", inplace=True)

    print_random_deck(card_df)


if __name__ == "__main__":
    main()
