import logging

import spotify.format_rating as fr
import spotify.generate_rating as gr
import spotify.url_parser as up
from django.http import HttpResponse
from django.shortcuts import render
from spotify.generate_rating import SpotifyAPIError

logger = logging.getLogger(__name__)

def favicon(request):
    return HttpResponse(status=204)


def index(request):
    """loads the index page."""
    return render(request, "spotify/index.html")


def rate(request):
    """Handle rating requests for Spotify music content"""
    context = {}

    if request.method != "POST":
        return render(request, "spotify/rate.html", context)

    try:
        # Get user input and change search type text in search box
        user_input = request.POST.get("user_input").strip()
        search_type = request.POST.get("search_type").strip()

        if not user_input:
            raise ValueError("No search query provided")

        # Handle different search types
        id = ""
        if search_type == "link":
            if not up.validate_url(user_input):
                  raise ValueError("Invalid Spotify link provided")

            search_type = up.get_url_type(user_input)
            id = up.get_url_id(user_input)  # is empty string if not url

            if not search_type or not id:
                raise ValueError("Could not parse Spotify URL")
        else:
            if len(user_input) > 50:
                raise ValueError("Search query too long")

        # get rating from api and description from json file

        result = gr.get_popularity(
                  content_type=search_type,
                  content_name=user_input,
                  input_id=id
                  )

        if result is None:
            raise ValueError(f"No {search_type} found matching your search")

        popularity, name, image = result
        desc, reaction_img = fr.format_rating(popularity, type=search_type)

        context.update({
                  "search_type": search_type,
                  "rating": popularity,
                  "description": desc,
                  "reaction": f"static/spotify/rating_reaction/{reaction_img}",
                  "image": image,
                  "name": name
                  })
    except ValueError as e:
        context["error"] = str(e)
        logger.warning(f"Validation error: {str(e)}", exc_info=True)

    except SpotifyAPIError as e:
        context["error"] = "Unable to fetch data from Spotify. Please try again later."
        logger.error(f"Spotify API error: {str(e)}", exc_info=True)

    except Exception as e:
        context["error"] = "An unexpected error occurred. Please try again later."
        logger.error(f"Unexpected error in rate view: {str(e)}", exc_info=True)

    return render(request, "spotify/rate.html", context)
