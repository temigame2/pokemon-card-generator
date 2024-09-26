from dataclasses import dataclass
import random

from src.content.collection import Collection
from src.content.style import Style
from src.mechanics.card import Card
from src.mechanics.element import Element
from src.mechanics.rarity import Rarity
from src.pokemon_content.pokemon_content_pool import get_closest_match, get_creature_types, get_random_detail_adjective, \
    get_random_rarity_adjective, get_random_series_adjective, AMBIENCE_BY_ELEMENT, \
    get_random_ambience
from src.pokemon_content.pokemon_prompts import get_image_prompt, get_visual_description, generate_card_name
from src.util.gpt_call import gemini_client


@dataclass
class PokemonCollection(Collection):

    BASE_POINTS = 4
    ABILITY_TO_HP_PTS = 2  # 1 ability cost is worth 2 HP points.
    NEUTRAL_ELEMENT_CHANCE = 0.5
    MIXED_ELEMENT_CHANCE = 0.5

    def generate_card(
        self,
        element: Element,
        rarity: Rarity,
        inherited_style: Style = None,
        series_index: int | None = None,
        subject_override: str = None,
    ) -> Card:

        is_part_of_series = series_index is not None
        if is_part_of_series:
            max_ability_points = self.get_points_budget(rarity.index, series_index)
        else:
            max_ability_points = self.get_points_budget(rarity.index, 1)

        hp_points = random.randint(0, max_ability_points // 2)


        # Calculate HP
        bonus_hp_points = max_ability_points + (hp_points * self.ABILITY_TO_HP_PTS)

        hp = random.randint(1,10) * bonus_hp_points

        atk = random.randint(4,10)
        res = random.randint(1,8)
        spd = random.randint(1,10)

        style = self.generate_style(
            inherited_style, element, rarity, series_index, subject_override
        )

        card = Card(
            index=len(self.cards) + 1,
            name="Untitled Card",
            rarity=rarity,
            hp=hp,
            atk=atk,
            res=res,
            spd=spd,
            style=style,
        )

        card.image_prompt = get_image_prompt(card)
        card.visual_description = get_visual_description(card)

        # Generate a name for the card.
        if gemini_client().is_gemini_enabled:
            card.name = generate_card_name(card, self.card_names_seen)

        card.image_prompt = get_image_prompt(card)
        card.visual_description = get_visual_description(card)
        self.card_names_seen.add(card.name)
        self.cards.append(card)
        return card

    def generate_style(
        self,
        inherited_style: Style,
        element: Element,
        rarity: Rarity,
        series_index: int | None = None,
        subject_override: str = None,
    ) -> Style:

        style = Style(
            style_prefix=self.theme_style.style_prefix,
            style_suffix=self.theme_style.style_suffix,
        )

        style.subject_type = self.theme_style.subject_type

        # Pick the card's subject (creature type)
        if inherited_style is not None:
            style.subject = inherited_style.subject
            style.subject_adjectives = inherited_style.subject_adjectives
            style.detail = inherited_style.detail
            style.environment = inherited_style.environment
        else:

            if subject_override is not None:
                subject = get_closest_match(subject_override)
                style.subject = subject.name
            else:
                potential_subjects = get_creature_types(element)
                reduced_subjects: set = potential_subjects - self.subjects_seen
                if len(reduced_subjects) == 0:
                    reduced_subjects = potential_subjects

                subject = random.choice(list(reduced_subjects))
                self.subjects_seen.add(subject)
                style.subject = subject.name

            potential_details = set(subject.details)
            reduced_details: set = potential_details - self.subjects_seen
            if len(reduced_details) == 0:
                reduced_details = potential_details

            detail = random.choice(list(reduced_details))
            detail_adjective = get_random_detail_adjective(element=element)
            style.detail = detail.text(detail_adjective)

        # Pick adjective(s) for the subject.
        rarity_prefix = get_random_rarity_adjective(rarity.index)
        series_prefix = get_random_series_adjective(series_index)

        if series_index is not None:
            size_prefix = series_prefix
            if rarity.index >= 2:
                size_prefix += f" {rarity_prefix}"
        else:
            size_prefix = rarity_prefix

        style.subject_adjectives = [
            *self.theme_style.subject_adjectives,
            size_prefix,
        ]

        # Set the ambience
        if rarity.index >= 2 and series_index == 2:
            # Use the last background for the final card in the series.
            style.ambience = AMBIENCE_BY_ELEMENT.get(element)[-1]
        else:
            style.ambience = get_random_ambience(element) + " background"

        return style

    @staticmethod
    def get_points_budget(rarity_index: int, series_index: int) -> int:
        # Cards in a series start weaker, but get stronger as the series progresses.
        rarity_bonus = rarity_index
        series_bonus = series_index - 1
        return PokemonCollection.BASE_POINTS + rarity_bonus + series_bonus

    @staticmethod
    def get_ability_points_costs(ability_points: int, rarity_index: int) -> list[str]:
        # Determine how many abilities the card will have, and how many points each ability will cost.
        if ability_points >= 6:
            return [4, ability_points - 4]
        elif ability_points >= 4:
            first_ability_cost = random.choice([3, 4])
            if first_ability_cost == 4:
                return [4]
            else:
                return [first_ability_cost, ability_points - first_ability_cost]
        elif ability_points == 3:
            if rarity_index < 1:
                return [2, 1]
            else:
                return [3] if random.random() < 0.5 else [2, 1]
        else:
            return [ability_points]
