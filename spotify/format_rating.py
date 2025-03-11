import json
import os
from django.contrib.staticfiles import finders
from django.conf import settings


def assign_letter_grade(pop_rating=0):
    """Assigns letter grade based on 0-100 popularity rating from Spotify API"""
    r = pop_rating

    if r > 90:
        return "A"
    elif r > 80:
        return "B"
    elif r > 70:
        return "C"
    elif r > 60:
        return "D"
    elif r > 50:
        return "F"
    elif r > 40:
        return "G"
    elif r > 30:
        return "H"
    else:
        return "Z"


def get_description(letter_rating, type="track"):
    """Gets description and image path from json file"""
    # file_path = os.path.join(settings.STATIC_ROOT, "spotify", "descriptions.json")

    json_path = finders.find("spotify/descriptions.json")

    if not json_path:
        json_path = os.path.join(settings.STATIC_ROOT, "spotify", "descriptions.json")

    # json_data = open(file_path, "r")
    with open(json_path, "r") as json_data:
        data = json.load(json_data)

    # json_data.close()

    desc = data[letter_rating][type]
    img = data[letter_rating]["reaction"]

    return desc, img


def format_rating(generated_rating=0, type="track"):
    """Used to return letter grade and image to view"""
    return get_description(assign_letter_grade(generated_rating), type)
