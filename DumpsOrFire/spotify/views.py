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
            result = None
            try:
                result = gr.get_popularity(content_name = user_input)
            except Exception as e:
                context['error'] = "Error fetching data from Spotify API, please try a different track or again later."
                print(str(e))
                return render(request, 'spotify/rate.html', context)

            if result is not None:
                popularity, name, image = result

                '''get rating from api and description from json file'''
                context['rating'] = popularity

                desc, img = fr.format_rating(popularity, type = 'track')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = image
                context['name'] = name

        elif search_type == 'album':
            # album search
            try:
                result =  gr.get_popularity(content_type = "album", content_name = user_input)
            except Exception as e:
                print(str(e))
                context['error'] = "Error fetching data from Spotify API, please try a different album or again later."
                return render(request, 'spotify/rate.html', context)

            if result is not None:
                popularity, name, image = result
                context['rating'] = popularity

                desc, img = fr.format_rating(popularity, type = 'album')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = image
                context['name'] = name
            else:
                context['error'] = f"No result with name {user_input} found."


        elif search_type == 'playlist':
            # playlist search
            try:
                result = gr.get_popularity(content_type = "playlist", content_name = user_input)
            except Exception as e:
                print(str(e))
                context['error'] = "Error fetching data from Spotify API, please try a different playlist or again later."
                return render(request, 'spotify/rate.html', context)
            if result is not None:
                popularity, name, image = result
                context['rating'] = popularity

                desc, img = fr.format_rating(popularity, type = 'playlist')

                context['description'] =  desc
                context['reaction'] = f"static/spotify/rating_reaction/{img}"

                context['image'] = image
                context['name'] = name
            else:
                context['error'] = f"No result with name {user_input} found."

        elif search_type == 'link':
            # link search

            # validate url
            if not up.validate_url(user_input):
                context['error'] = "Invalid Spotify link, please try again with a valid link."
                return render(request, 'spotify/rate.html', context)

            s_type = up.get_url_type(user_input)
            id = up.get_url_id(user_input)

            if s_type == 'track' or s_type == 'album' or s_type == 'playlist':
                try:
                    result = gr.get_popularity(content_type = s_type, input_id = id)
                except Exception as e:
                    print(str(e))
                    context['error'] = "Error fetching data from Spotify API, please try a different URL or again later."
                    return render(request, 'spotify/rate.html', context)

                if result is not None:
                    popularity, name, image = result
                    context['rating'] = popularity

                    desc, img = fr.format_rating(popularity, type = s_type)
                    context['description'] =  desc
                    context['reaction'] = f"static/spotify/rating_reaction/{img}"

                    context['image'] = image
                    context['name'] = name


    return render(request, 'spotify/rate.html', context)
