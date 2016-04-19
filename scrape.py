import sys
import json
import requests


seen_photos = {}


def recursive_scrape(url, count=0):

    # The API seems to link the images in a loop, so we can stop once we see an
    # image we have already seen.
    if url in seen_photos:
        return
    seen_photos[url] = True

    page = requests.get(url)
    photo_json = page.json()

    print photo_json
    yield photo_json

    next_url = 'https://earthview.withgoogle.com' + photo_json['nextApi']

    # Yielding from recursive functions is a bit funky
    for photo_json in recursive_scrape(next_url, count + 1):
        yield photo_json


if __name__ == "__main__":
    # Google Earth View contains around 1500 photos, so we need to up the
    # recursion limit
    sys.setrecursionlimit(2000)

    photos_json = json.dumps(list(recursive_scrape(
        'https://earthview.withgoogle.com/_api/polanczyk-poland-5484.json'
    )))

    with open('earthview.json', 'w+') as f:
        f.write(photos_json)
