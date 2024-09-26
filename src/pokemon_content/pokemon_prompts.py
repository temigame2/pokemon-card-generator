import string

from src.mechanics.card import Card
from src.util.gpt_call import gemini_client


def get_visual_description(card: Card) -> str:
    segments = []
    subject_line = get_full_subject_description(card)
    segments.append(subject_line)
    segments.append(f"It can be found in {card.style.environment}-like environments.")
    message = " ".join(segments)
    return message


def get_image_prompt(card: Card):

    segments = []
    subject_line = get_subject_description(card)

    subject_line += get_detail_description(card)
    segments.append(subject_line)
    segments.append(card.style.ambience)
    segments.append(card.style.style_suffix)

    message = ", ".join(segments)
    message = message.replace("  ", " ")
    message = message.replace(" ,", ",")

    message = f"{card.name}, enemy, " + message
    return message


def get_subject_description(card: Card):
    subject_section = ["a"]
    subject_section.extend(card.style.subject_adjectives)
    subject_section.append(card.style.subject)
    subject_line = " ".join(subject_section)
    subject_line = subject_line.replace(" ,", ",")
    return subject_line


def get_detail_description(card: Card) -> str:
    # Skip this if the card is a basic.
    if card.style.detail and card.rarity.index > 0:
        return ", " + card.style.detail
    else:
        return ""


def get_full_subject_description(card: Card):
    subject_line = get_subject_description(card)
    subject_line += get_detail_description(card)
    return subject_line


def generate_card_name(card: Card, seen_names: set[str]) -> str:

    if not gemini_client().is_gemini_enabled:
        return "Untitled Card"

    # Generate a name for the card.
    # additional_modifier = "(max 2 words), "
    if card.rarity.index == 0:
        additional_modifier = "short, single-word, "
    else:
        additional_modifier = "single-word, "

    prompt = f"Generate a unique, orignal, creative,{additional_modifier} {card.style.subject_type} name for a {get_visual_description(card)}"
    prompt += f" (without using the word {card.style.subject_type.lower()} or neutral):\n"
    print(prompt)
    response = gemini_client().get_completion(prompt)

    potential_names = set()
    print(potential_names)
    for potential_name in response:
        print(potential_name)
        try :
            name = potential_name.text
            print(name)
            name = name.strip()
            name = "".join([c for c in name if c.isalpha() or c == " " or c == "-"])
            name = string.capwords(name)
            potential_names.add(name)
            print(name)
        except Exception as e:
            name = "Error"
            potential_names.add(name)


    # Pick the shortest name.
    filtered_names = set(potential_names) - seen_names
    if len(filtered_names) > 0:
        potential_names = filtered_names

    potential_names = sorted(potential_names, key=lambda x: len(x))
    name = potential_names[0]
    return name
