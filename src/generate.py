#!/usr/bin/env python

import argparse
import random
import time

from pokemon_content.pokemon_collection import PokemonCollection
from pokemon_content.pokemon_elements import PokemonElements
from content.style import Style
from pokemon_content.pokemon_rarity import PokemonRarity


def main():

    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-s",
        "--subject",
        type=str,
        default=None,
        help="What type of monster to generate (e.g. monkey, dragon, etc.).",
    )

    args = argparser.parse_args()
    subject_override = args.subject


    pokemon_style: Style = Style(
        subject_type="Moster",
        style_suffix="--niji",
    )

    classic_collection = PokemonCollection(
        "pokemon-classic",
        theme_style=pokemon_style,
        elements=PokemonElements.NEUTRAL,
        rarities=PokemonRarity.ALL,
    )

    all_collections = [
        classic_collection,
    ]

    collection_seed = random.randint(0, 1000000)
    for current_collection in all_collections:
        random.seed(collection_seed)

        monsters = current_collection.generate_random_cards(
            element=PokemonElements.NEUTRAL, subject_override=subject_override
        )
        print(*monsters, sep="\n\n")
        current_collection.export()



if __name__ == "__main__":
    main()
