class Card:
    def __init__(
        self,
        id: int,
        name: str,
        provision: int,
        group: str,
        type: str,
        faction: str,
        secondary_faction: str = "",
    ):
        """
        Represents a Gwent card with its key attributes.

        Args:
            id (int): Unique card ID.
            name (str): Name of the card.
            provision (int): Provision cost of the card.
            group (str): Card group (e.g., bronze, gold).
            type (str): Card type (e.g., unit, special).
            faction (str): Primary faction of the card.
            secondary_faction (str, optional): Secondary faction if any. Defaults to empty string.
        """
        self.id = id
        self.name = name
        self.provision = provision
        self.group = group
        self.type = type
        self.faction = faction
        self.secondary_faction = secondary_faction

    def __repr__(self):
        return f"{self.name} (Prov: {self.provision})"
