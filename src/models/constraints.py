from src.models.card import Card
from src.models.faction import Faction
from collections import Counter


def check_constraints(deck: list[Card], faction: Faction, leader_ability: str) -> bool:
    """
    Validates a Gwent deck against faction rules and leader ability constraints.

    Args:
        deck (list[Card]): List of Card objects representing the deck.
        faction (Faction): The faction the deck belongs to.
        leader_ability (str): The leader ability chosen for the deck.

    Returns:
        bool: True if the deck meets all constraints, False otherwise.
    """
    if leader_ability not in faction.leader_abilities:
        return False

    provision_limit = faction.leader_abilities[leader_ability] + 150
    total_provision = sum(card.provision for card in deck)
    if total_provision > provision_limit:
        print("Provision limit exceeded")
        return False

    if len(deck) > 25:
        print("Deck length exceeded")
        return False

    unit_count = sum(1 for card in deck if card.type == "unit")
    if unit_count < 13:
        print("Too few units")
        return False

    count_by_id = Counter(card.id for card in deck)
    for card in deck:
        count = count_by_id[card.id]
        if card.group == "bronze" and count > 2:
            print("More then 2 copies of a bronze card")
            return False
        if card.group == "gold" and count > 1:
            print("More then 1 copy of a gold card")
            return False

        if card.faction != faction.name:
            if card.faction != "neutral" and card.secondary_faction != faction.name:
                print(
                    f"card: {card.name} faction not matching leader ability ({card.faction}, {card.secondary_faction})"
                )
                return False

    return True
