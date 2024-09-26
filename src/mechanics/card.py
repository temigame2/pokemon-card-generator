from dataclasses import dataclass, field
from functools import cached_property

from src.content.style import Style
from src.mechanics.rarity import Rarity

STAR_UNICODE = "★ "


@dataclass
class Card:

    index: int
    name: str
    rarity: Rarity
    hp: int
    atk: int
    res: int
    spd: int
    part_of_evolution: bool = False
    style: Style = field(default_factory=Style)

    image_prompt: str | None = None
    visual_description: str | None = None

    def __repr__(self):
        rarity_stars = STAR_UNICODE * (self.rarity.index + 1)
        message = f"{self.name} \n"
        message += f"HP: {self.hp}\n"
        message += f"ATK: {self.atk}\n"
        message += f"RES: {self.res}\n"
        message += f"SPD: {self.spd}\n"
        message += f"Rarity: {rarity_stars} ({self.rarity.name})\n"

        message += f"Image Prompt:\n"
        message += f"{self.image_prompt}\n\n"
        return message

    def to_json(self):
        return {
            "index": self.index,
            "name": self.name,
            "rarity": self.rarity.name,
            "rarity_index": self.rarity.index,
            "hp": self.hp,
            "atk": self.atk,
            "res": self.res,
            "spd": self.spd,
            "image_prompt": self.image_prompt,
            "image_file": self.image_file,
        }

    @property
    def image_file(self):
        return f"{self.index:03d}_{self.snake_case_name}.png"

    @cached_property
    def snake_case_name(self):
        return self.name.lower().replace(" ", "_")
