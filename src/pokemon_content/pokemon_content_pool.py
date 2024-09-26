from dataclasses import dataclass, field
import random

from src.mechanics.element import Element
from src.pokemon_content.pokemon_elements import PokemonElements


@dataclass
class Detail:
    relation: str
    detail: str
    quantifier: str | None = None

    def text(self, adjective: str = None):
        quantifier = f"{self.quantifier} " if self.quantifier else ""
        if adjective:
            return f"{self.relation} {quantifier}{adjective} {self.detail}"
        return f"{self.relation} {quantifier}{self.detail}"

    def __hash__(self) -> int:
        return hash(self.detail)


@dataclass
class CreatuteType:
    name: str
    details: list[Detail] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.name)


HOLDABLE_WEAPONS = []


def with_holdable_weapon(detail: str, quantifier: str = None) -> Detail:
    detail = Detail(relation="holding", detail=detail, quantifier=quantifier)
    HOLDABLE_WEAPONS.append(detail)
    return detail


def with_detail(detail: str, quantifier: str = None) -> Detail:
    return Detail(relation="with", detail=detail, quantifier=quantifier)


def wearing_detail(detail: str, quantifier: str = None) -> Detail:
    return Detail(relation="wearing", detail=detail, quantifier=quantifier)


HOLD_SWORD = with_holdable_weapon("sword", "a")
HOLD_BOW = with_holdable_weapon("bow", "a")
HOLD_STAFF = with_holdable_weapon("staff", "a")
HOLD_SHIELD = with_holdable_weapon("shield", "a")
HOLD_AXE = with_holdable_weapon("axe", "an")
HOLD_DAGGER = with_holdable_weapon("dagger", "a")
HOLD_SPEAR = with_holdable_weapon("spear", "a")
HOLD_MACE = with_holdable_weapon("mace", "a")
HOLD_HAMMER = with_holdable_weapon("hammer", "a")
HOLD_CLUB = with_holdable_weapon("club", "a")
HOLD_LANCE = with_holdable_weapon("lance", "a")
HOLD_WHIP = with_holdable_weapon("whip", "a")
HOLD_GLAIVE = with_holdable_weapon("glaive", "a")

# WITH_EYES = with_detail("eyes")
WITH_CLAWS = with_detail("claws")
WITH_TAIL = with_detail("tail", "a")
WITH_HORNS = with_detail("horns")
WITH_HOOVES = with_detail("hooves")
WITH_TUSKS = with_detail("tusks")
WITH_FUR = with_detail("fur")
WITH_SKIN = with_detail("skin")
WITH_ANTLERS = with_detail("antlers")
WITH_SCALES = with_detail("scales")
WITH_SHELL = with_detail("shell")
WITH_HALO = with_detail("halo", "a")
WITH_WINGS = with_detail("wings")
WITH_FINS = with_detail("fins")
WITH_TENTACLES = with_detail("tentacles")
WITH_FEATHERS = with_detail("feathers")
WITH_TALONS = with_detail("talons")
WITH_BEAK = with_detail("beak", "a")
WITH_CARAPACE = with_detail("carapace", "")
WITH_TEXTURE = with_detail("texture")


WEARING_ARMOR = wearing_detail("armor")
WEARING_BRACERS = wearing_detail("bracers")
BODY_WEARABLES = [WEARING_ARMOR, WEARING_BRACERS]

WEARING_MASK = wearing_detail("mask", "a")
WEARING_CROWN = wearing_detail("crown", "a")
HEAD_WEARABLES = [WEARING_MASK, WEARING_CROWN]

ALL_WEARABLES = [*BODY_WEARABLES, *HEAD_WEARABLES]
LIZARD_DETAILS = [WITH_TAIL, WITH_SCALES, *ALL_WEARABLES, *HOLDABLE_WEAPONS]


REPTILE = CreatuteType("reptile", [WITH_TAIL, WITH_SKIN, WITH_CLAWS])
DRAGON = CreatuteType("dragon", [WITH_CLAWS, WITH_HORNS, WITH_SCALES, WITH_TAIL, WITH_WINGS])

REPTILES = [REPTILE, DRAGON]

INSECT_DETAILS = [WITH_WINGS]

BUTTERFLY = CreatuteType("butterfly", [*INSECT_DETAILS])
MANTIS = CreatuteType("mantis", [*INSECT_DETAILS])
BEETLE = CreatuteType("beetle", [*INSECT_DETAILS])
DRAGONFLY = CreatuteType("dragonfly", [*INSECT_DETAILS])
SPIDER = CreatuteType("spider", [])
SCORPION = CreatuteType("scorpion", [*INSECT_DETAILS])

INSECTS = [
    MANTIS,
    BEETLE,
    DRAGONFLY,
    SPIDER,
]

ABSTRACT_DETAILS = [WITH_TEXTURE]
PUMPKIN = CreatuteType("pumpkin", [WITH_SKIN])
GHOST = CreatuteType("ghost", [WITH_SKIN])
TREANT = CreatuteType("treant", [WITH_SKIN])
GOLEM = CreatuteType("golem", [*HOLDABLE_WEAPONS, *ALL_WEARABLES])
ABSTRACT_TYPES = [PUMPKIN, GHOST, TREANT, GOLEM]
ORC = CreatuteType("orc", [*HOLDABLE_WEAPONS, *ALL_WEARABLES])
ELF = CreatuteType("elf", [*HOLDABLE_WEAPONS, *ALL_WEARABLES])
GNOME = CreatuteType("gnome", [*HOLDABLE_WEAPONS, *ALL_WEARABLES])
GOBLIN = CreatuteType("goblin", [*HOLDABLE_WEAPONS, *ALL_WEARABLES])

LAND_CREATURES = [ORC, ELF, GNOME, GOBLIN]

ALL_CREATURES = [*LAND_CREATURES, *REPTILES, *INSECTS]

CREATURES_BY_ELEMENT = {
    PokemonElements.NEUTRAL: set(ALL_CREATURES)
}

GLOBAL_DETAIL_ADJECTIVES = [
    "dark",
    "golden",
    "ornate",
    "ancient",
    "rust",
    "broken",
    "royal",
    "enchanted"
]

AMBIENCE_BY_ELEMENT = {
    PokemonElements.NEUTRAL: [
        "parchment",
        "old paper",
        "off-white"
    ]
}

ALL_SUBJECTS = [*LAND_CREATURES, *REPTILES, *INSECTS]
ALL_SUBJECTS_BY_NAME = {subject.name: subject for subject in ALL_SUBJECTS}


def get_rarity_adjectives_set(rarity_index: int) -> set[str]:
    if rarity_index == 0:
        return {"simple", "basic"}
    if rarity_index == 1:
        return {"strong", "special"}
    if rarity_index == 2:
        return {"legendary", "epic", "mythical"}
    else:
        return {""}


def get_series_adjectives_set(series_index: int) -> set[str]:
    if series_index == 0:
        return {"common"}
    if series_index == 1:
        return {"normal"}
    if series_index == 2:
        return {"massive"}
    if series_index == 3:
        return {"gigantic"}
    else:
        return {""}


def get_random_rarity_adjective(rarity_index: int) -> str:
    return random.choice(list(get_rarity_adjectives_set(rarity_index)))


def get_random_series_adjective(series_index: int | None) -> str:
    if series_index is None:
        return ""
    return random.choice(list(get_series_adjectives_set(series_index)))


def get_creature_types(element: Element) -> set[CreatuteType]:
    return CREATURES_BY_ELEMENT.get(element)


def get_closest_match(subject_override: str):
    if subject_override in ALL_SUBJECTS_BY_NAME:
        return ALL_SUBJECTS_BY_NAME[subject_override]
    else:
        # Create a new subject with the name of the override.
        return CreatuteType(subject_override, [WEARING_ARMOR])


def get_random_ambience(element: Element) -> str:
    # Get a random ambience, but don't return the last one, which is for fully evolved pokemon.
    return random.choice(AMBIENCE_BY_ELEMENT.get(element)[:-1])


def get_random_detail_adjective(element: Element) -> str:
    joined_adjectives = GLOBAL_DETAIL_ADJECTIVES
    return random.choice(joined_adjectives)
