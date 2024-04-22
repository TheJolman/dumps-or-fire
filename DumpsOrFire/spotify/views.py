from django.shortcuts import render
from . import generate_rating as gr

# from django.http import JsonResponse

from . import format_rating as fr
from . import url_parser as up

# Create your views here.

def index(request):
    return render(request, 'spotify/index.html')

def rate(request):
    context = {}
    if request.method == 'POST':
        '''Get user input and change search type text in search box'''
        user_input = request.POST.get('user_input')
        search_type = request.POST.get('search_type')

        if len(user_input) > 50 and search_type != 'link':
            context['error'] = "Search query too long, please try again with a shorter query."
            return render(request, 'spotify/rate.html', context)

        # set default search type if none provided
        if not search_type:
            search_type = 'album'

        context['search_type'] = search_type

        if search_type == 'track':
            # track search
            result = gr.get_popularity(content_name = user_input)
            if result is not None:
                '''get rating from api and description from json file'''
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'track')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = gr.get_image(content_name=user_input)
                context['name'] = gr.get_name(content_name=user_input)
            else:
                context['error'] = f"No result with name {user_input} found."

        elif search_type == 'album':
            # album search
            result =  gr.get_popularity(content_type = "album", content_name = user_input)
            if result is not None:
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'album')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = gr.get_image(content_type="album", content_name=user_input)
                context['name'] = gr.get_name(content_type="album", content_name=user_input)
            else:
                context['error'] = f"No result with name {user_input} found."


        elif search_type == 'playlist':
            # playlist search
            result = gr.get_popularity(content_type = "playlist", content_name = user_input)
            if result is not None:
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'playlist')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = gr.get_image(content_type="playlist", content_name=user_input)
                context['name'] = gr.get_name(content_type="playlist", content_name=user_input)
            else:
                context['error'] = f"No result with name {user_input} found."

        elif search_type == 'link':
            # link search
            s_type = up.get_url_type(user_input)
            id = up.get_url_id(user_input)

            if s_type == 'track':
                result = gr.get_track_popularity("", id=id)
                context['rating'] = result

                desc, img = fr.format_rating(result, type = 'Track')
                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"



    return render(request, 'spotify/rate.html', context)
