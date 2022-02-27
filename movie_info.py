import sys
import traceback
import random

import os
import requests
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def movie_info():
    try:
        movie_ids = [98, 550, 634649]
        movie_id = random.choice(movie_ids)
        tmdb_api_key = os.getenv('TMDB_API_KEY')
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}")
        response.raise_for_status()
        status = response.status_code
        details = response.json()
        print(f"Response Status = {status}")
        title = details['title']
        tagline = details['tagline']
        genre = details['genres'][0]['name']
        poster_path = details['poster_path']
        # Poster sizes from https://api.themoviedb.org/3/configuration?api_key=<>
        poster_url = f"https://image.tmdb.org/t/p/w342/{poster_path}"
        print(f"Details: {title}, {tagline}, {genre}")
        print(f"Poster URL: {poster_url}")


        wikipedia_query = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&eititle=Template:Infobox film&format=json"
        response = requests.get(wikipedia_query)
        response.raise_for_status()
        wikipedia_info = response.json()
        pages = wikipedia_info['query']['pages'].values()
        print(f"Wikipedia query result pages: {pages}")
        page = list(pages)[0]
        print(f"Wikipedia query result first page: {page}")
        wikipedia_page_id = page['pageid']
        wikipedia_url = f"http://en.wikipedia.org/wiki?curid={wikipedia_page_id}"

        page_content = f"<html>" \
                       f"<body align='center'>" \
                       f"<H3>Movie Explorer</H3>" \
                       f"<p>{title}</p>" \
                       f"<p>{tagline}</p>" \
                       f"<p>Geners: {genre}</p>" \
                       f"<img src='{poster_url}'/>" \
                       f"<p><a href='{wikipedia_url}'>Click here to see Wikepedia Page for movie </a>" \
                       f"</body>" \
                       f"</html>"
        print(f"Page Content: {page_content}")
        return page_content
    except BaseException as e:
        traceback.print_exception(*sys.exc_info())
        return f"<html>" \
               f"<body align='center'><p> An error occurred. Please try again later</p></body>" \
               f"</html>"


if __name__ == "__main__":
    app.run()
    # data = movie_info()
    # print(data)