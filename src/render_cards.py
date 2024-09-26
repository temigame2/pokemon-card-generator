import argparse
import json
import os
import pathlib
from PIL import Image, ImageFont, ImageDraw

from pokemon_content.pokemon_rarity import PokemonRarity
from src.mechanics.ability import Ability
from src.mechanics.card import Card

MONSTER_IMAGE_SCALE = 0.255
MONSTER_IMAGE_SCALE_SQ = 0.355
IDEAL_CARD_WIDTH = 450

ABILITY_WIDTH = 370
ABILITY_HEIGHT = 72
ABILITY_COST_WIDTH = 76
ABILITY_COST_GAP = 12
ELEMENT_SIZE = 30
ABILITY_GAP = 4
POWER_WIDTH = 64

STATUS_Y_POSITION = 568
STATUS_X_GAP = 82
STATUS_SIZE = 20


def render_cards(collection_path: str):
    card_path = pathlib.Path(collection_path, "cards")
    card_render_path = pathlib.Path(collection_path, "renders")
    os.makedirs(card_render_path, exist_ok=True)

    for card_path in card_path.iterdir():
        # Only render .json files.
        if not card_path.suffix == ".json":
            continue

        with open(card_path) as f:
            data = json.load(f)
            card = card_from_json(data)
            card_image = render_card(card, collection_path)
            image_name = f"{card.index:03d}_{card.snake_case_name}.png"
            card_image.save(card_render_path / f"{image_name}")


def render_card(card: Card, collection_path: str):
    print(f"Rendering {card.name}")
    card_template_name = f"neutral_card.png"
    card_image = Image.open(f"../resources/cards/{card_template_name}")

    card_art_path = pathlib.Path(collection_path, "images", card.image_file)

    if pathlib.Path(card_art_path).exists():
        canvas = Image.new("RGBA", card_image.size, (0, 0, 0, 0))
        card_art_image = Image.open(card_art_path)

        # Rescale the image to fit the card.
        rescale_factor = IDEAL_CARD_WIDTH / card_art_image.size[0]
        resized_image_shape = (
            int(card_art_image.size[0] * rescale_factor),
            int(card_art_image.size[1] * rescale_factor),
        )
        card_art_image = card_art_image.resize(resized_image_shape)

        # Center the image.
        card_center_x = card_image.size[0] / 2
        card_center_y = 330
        monster_image_x = card_center_x - (card_art_image.size[0] / 2)
        monster_image_y = card_center_y - (card_art_image.size[1] / 2)
        canvas.paste(card_art_image, (int(monster_image_x), int(monster_image_y)))
        canvas.paste(card_image, (0, 0), card_image)
        card_image = canvas
    else:
        # Print in yellow ASCII.
        print(f"\033[93m [WARN] {card_art_path} not found.\033[0m")

    # Write the name of the card.
    name_text_position = (160, 85)
    title_font = ImageFont.truetype("../resources/font/Cabin-Bold.ttf", 45)
    name_text = card.name

    # Draw the name text onto the card.
    draw = ImageDraw.Draw(card_image)
    draw.text(
        name_text_position, name_text, font=title_font, fill=(0, 0, 0), anchor="ls"
    )

    # Draw the HP on the card.
    hp_position = (180, 555)
    hp_font = ImageFont.truetype("../resources/font/Cabin-Bold.ttf", 28)
    hp_text = f"{card.hp} PV"
    draw.text(
        hp_position,
        hp_text,
        font=hp_font,
        fill=(0, 0, 0),
        anchor="rs",
    )

    # Draw the ATK on the card.
    atk_position = (165, 615)
    atk_font = ImageFont.truetype("../resources/font/Cabin-Bold.ttf", 28)
    atk_text = f"{card.atk} ATK"
    draw.text(
        atk_position,
        atk_text,
        font=atk_font,
        fill=(0, 0, 0),
        anchor="rs",
    )

    # Draw the RES on the card.
    res_position = (165, 665)
    res_font = ImageFont.truetype("../resources/font/Cabin-Bold.ttf", 28)
    res_text = f"{card.res} RES"
    draw.text(
        res_position,
        res_text,
        font=res_font,
        fill=(0, 0, 0),
        anchor="rs",
    )

    # Draw the SPD on the card.
    spd_position = (180, 713)
    spd_font = ImageFont.truetype("../resources/font/Cabin-Bold.ttf", 28)
    spd_text = f"{card.spd} SPD"
    draw.text(
        spd_position,
        spd_text,
        font=spd_font,
        fill=(0, 0, 0),
        anchor="rs",
    )

    # Write the rarity of the Pokémon.
    rarity_symbol_position = (card_image.width - 64, 605)
    symbol_font = ImageFont.truetype("../resources/font/NotoSansSymbols2-Regular.ttf", 22)
    rarity_symbols = ["⬤", "◆", "★"]
    rarity_symbol_sizes = [10, 14, 22]

    symbol_text = rarity_symbols[card.rarity.index]
    symbol_font = ImageFont.truetype(
        "../resources/font/NotoSansSymbols2-Regular.ttf",
        rarity_symbol_sizes[card.rarity.index],
    )

    draw.text(
        rarity_symbol_position,
        symbol_text,
        font=symbol_font,
        fill=(0, 0, 0),
        anchor="mm",
    )

    return card_image


def card_from_json(data: dict) -> Card:
    card = Card(
        index=data["index"],
        name=data["name"],
        rarity=PokemonRarity.get_rarity_by_name(data["rarity"]),
        hp=data["hp"],
        atk=data["atk"],
        res=data["res"],
        spd=data["spd"],


    )
    return card


def ability_from_json(data: dict) -> Ability:
    return Ability(
        name=data["name"],
        cost=data["cost"],
        is_mixed_element=data["is_mixed_element"],
    )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--collection",
        help="File path to the collection to render",
        default="output/pokemon-classic",
    )
    collection_path = argparser.parse_args().collection
    render_cards(collection_path)


if __name__ == "__main__":
    main()
