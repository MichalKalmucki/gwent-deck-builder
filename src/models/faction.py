class Faction:
    def __init__(self, name: str, leaders: dict):
        self.name = name
        self.leader_abilities = {
            ability: provisions for ability, provisions in leaders.items()
        }


def get_factions() -> list[Faction]:
    """
    Returns a list of predefined Gwent factions, each with their associated leader abilities and provision bonuses.

    Each faction is represented as an instance of the `Faction` class, initialized with:
    - A name (str)
    - A dictionary mapping leader ability names (str) to their corresponding provision bonuses (int)

    Returns:
        list[Faction]: A list of `Faction` objects for Nilfgaard, Northern Realms, Skellige, Scoia'tael,
                       Monsters, and Syndicate with their respective leader abilities and provision values.
    """
    return [
        Faction(
            "nilfgaard",
            {
                "Tactical Decision": 16,
                "Imprisonment": 15,
                "Toussaintois Hospitality": 15,
                "Imperial Formation": 16,
                "Doulbe Cross": 16,
                "Enslave": 15,
                "Imposter": 15,
            },
        ),
        Faction(
            "northernrealms",
            {
                "Uprising": 16,
                "Inspired Zeal": 14,
                "Shieldwall": 16,
                "Mobilization": 16,
                "Stockpile": 15,
                "Pincer Maneuver": 15,
                "Royal Inspiration": 16,
            },
        ),
        Faction(
            "skellige",
            {
                "Rage of the Sea": 15,
                "Battle Trance": 17,
                "Onslaught": 16,
                "Reckless Fury": 16,
                "Ursine Ritual": 16,
                "Patricidal Fury": 15,
                "Blaze of Glory": 16,
            },
        ),
        Faction(
            "scoiatael",
            {
                "Deadeye Ambush": 16,
                "Precision Strike": 14,
                "Nature's Gift": 15,
                "Call of Harmony": 17,
                "Mahakam Forge": 17,
                "Guerilla Tactics": 15,
                "Invigorate": 17,
            },
        ),
        Faction(
            "monsters",
            {
                "Carapace": 15,
                "Force of Nature": 16,
                "White Frost": 15,
                "Arachas Swarm": 15,
                "Fruits of Ysgith": 14,
                "Blood Scent": 16,
                "Overwhelming Hunger": 15,
            },
        ),
        Faction(
            "syndicate",
            {
                "Jackpot": 15,
                "Lined Pockets": 15,
                "Blood Money": 16,
                "Pirate's Cove": 16,
                "Off the Books": 16,
                "Congregate": 18,
                "Hidden Cache": 16,
            },
        ),
    ]
