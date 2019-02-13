"""
YTCompare
"""
import requests
"""
API Reference URL
https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=PLqq-6Pq4lTTZh5U8RbdXq0WaYvZBz2rbn&key=AIzaSyCg3WitBUQl5ifC2QygQaZUPOSRMKfSD5E&nextpage=1
"""


def gather_data(playlist_id_, page_token_=None):
    """Receive playlist data from YouTube's API"""
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    api_key = "ENTER API KEY HERE"
    max_results = 50 # 50 is max

    parameters = {"key": api_key,
                  "maxResults": max_results,
                  "playlistId": playlist_id_,
                  "part": "snippet",}

    if page_token_ is not None:
        parameters["pageToken"] = str(page_token_)

    response = requests.get(url, params=parameters)
    return response.json()


if __name__ == "__main__":
    domain = "www.youtube.com/watch?v="
    #playlist_id = "PLt-RfMTsSUDF0vjKuKmVS9r0xpwjI3vyj" # Mine
    playlist_id = "PLdy_Z-y66LeLNgbrAq6fXnuO42Lolm_dD" # Jordan's
    data = gather_data(playlist_id)
    page_token = data['nextPageToken']

    songs_and_urls = {}
    next_page_available = True
    use_token = False
    song_count = 0

    while next_page_available:
        if not use_token:
            data = gather_data(playlist_id)
        else:
            data = gather_data(playlist_id, page_token)
        try:
            page_token = data['nextPageToken']
        except KeyError:
            break
        for item in data['items']:
            songs_and_urls["Song " + str(song_count)] = {
                                                         "Title": item['snippet']['title'],
                                                         "URL": domain + item['snippet']['resourceId']['videoId'],
                                                        }
            #print(item['snippet']['title'])
            song_count += 1
        use_token = True
    print("Song count: " + str(song_count))

    for song in songs_and_urls:
        print("=====================================")
        print(song)
        print("Title: " + songs_and_urls[song]['Title'])
        print("URL: " + songs_and_urls[song]["URL"])



