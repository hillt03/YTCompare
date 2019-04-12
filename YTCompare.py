"""
YTCompare
"""
import requests
import os


def gather_data(playlist_id_, api_key_, page_token_=None):
    """Receive playlist data from YouTube's API"""
    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    max_results = 50  # 50 is YouTube's max for a request

    parameters = {
        "key": api_key_,
        "maxResults": max_results,
        "playlistId": playlist_id_,
        "part": "snippet",
    }

    if page_token_ is not None:
        parameters["pageToken"] = str(page_token_)

    response = requests.get(url, params=parameters)
    return response.json()


def gather_local_data():
    directory = input(
        "Enter the directory where your music"
        + " is stored. \n(Example: C:\\Users\\User\\Desktop\\Misc\\Music\\):"
    )
    local_songs = os.listdir(directory)
    i = 0
    for song_ in local_songs:
        local_songs[i] = os.path.splitext(song_)[0]
        i = i + 1
    return local_songs


def save_song_urls_to_disk(needed_songs_):
    with open("song_urls.txt", "w") as file:
        for song_ in needed_songs_:
            file.write(needed_songs_[song_]["URL"] + "\n")


if __name__ == "__main__":
    domain = "www.youtube.com/watch?v="
    local_song_list = gather_local_data()
    playlist_id = input("Enter your YouTube Playlist ID: ")
    api_key = input("Enter your YouTube Data v3 API key: ")

    data = gather_data(playlist_id, api_key)
    page_token = data["nextPageToken"]
    songs_and_urls = {}
    next_page_available = True
    use_token = False
    song_count = 0

    while next_page_available:
        if not use_token:
            data = gather_data(playlist_id, api_key)
        else:
            data = gather_data(playlist_id, api_key, page_token)
        try:
            page_token = data["nextPageToken"]
        except KeyError:
            break
        for item in data["items"]:
            songs_and_urls["Song " + str(song_count)] = {
                "Title": item["snippet"]["title"],
                "URL": domain + item["snippet"]["resourceId"]["videoId"],
            }
            # print(item['snippet']['title'])
            song_count += 1
        use_token = True
    print("Song count: " + str(song_count))

    needed_songs = {}

    song_number = 0
    for song in songs_and_urls:
        song_needed = False
        youtube_song_title = songs_and_urls[song]["Title"]
        for local_song in local_song_list:
            try:
                if youtube_song_title == local_song:
                    song_needed = False
                    break
                elif youtube_song_title[0:16] == local_song[0:16]:
                    print("Song 1: " + youtube_song_title)
                    print("Song 2: " + local_song)
                    user_input = input(
                        "Are these songs the same? (Enter 1 if yes (or just press enter), enter 2 if not): "
                    )
                    if user_input.lower() == "2" or user_input.lower() == "no":
                        song_needed = True
                    else:
                        song_needed = False
                        break
                elif youtube_song_title != local_song:
                    song_needed = True
            except IndexError:
                print("Song 1: " + youtube_song_title)
                print("Song 2: " + local_song)
                user_input = input(
                    "Are these songs the same? (Enter 1 if yes, enter 2 if not."
                )
                if user_input.lower() == "2" or user_input.lower() == "no":
                    song_needed = True
                else:
                    song_needed = False
        if song_needed:
            needed_songs[song_number] = {
                "Title": youtube_song_title,
                "URL": songs_and_urls[song]["URL"],
            }
            song_number += 1

    save_song_urls_to_disk(needed_songs)

    print(
        "Finished. Your song URLs can be found in a text document within the directory from where you ran this tool."
    )
