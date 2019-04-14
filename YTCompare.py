"""
YTCompare
"""
import requests
import os
import PySimpleGUI as sg


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


def gather_local_data(directory):
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


def gather_YouTube_input_from_GUI():
    sg_layout = [
        [sg.Text("Enter your YouTube Data V3 API key")],
        [sg.InputText()],
        [sg.Text("Enter your YouTube playlist's ID")],
        [sg.InputText()],
        [sg.Button("Submit"), sg.Button("Exit")],
    ]

    window = sg.Window("YTCompare").Layout(sg_layout)
    event, values = window.Read()
    if event == "Exit":
        raise SystemExit("Closing")
    window.Close()
    return event, values


def gather_local_input_from_GUI():
    event, (fname,) = (
        sg.Window("YTCompare")
        .Layout(
            [
                [sg.Text("Select your local music directory")],
                [sg.In(), sg.FolderBrowse()],
                [sg.CloseButton("Accept"), sg.CloseButton("Exit")],
            ]
        )
        .Read()
    )
    if event == "Exit":
        raise SystemExit("Closing")
    if not fname:
        sg.Popup("Closing", "No folder supplied")
        raise SystemExit("Closing: No folder supplied")

    return event, fname


def determine_song_similarity_from_GUI(youtube_song_title_, local_song_):
    """
    Returns True if songs are the same, returns False if they are different.
    """
    window_size = (800, 250)
    first_song = "Song 1: " + youtube_song_title_
    second_song = "Song 2: " + local_song_

    sg_layout = [
        [sg.Text("Are these songs the same?", size=(200, 1), justification="center")],
        [sg.Text(first_song, size=(200, 1), justification="center")],
        [sg.Text(second_song, size=(200, 1), justification="center")],
        [sg.Button("Yes", size=(15, 2), pad=(350, 10))],
        [sg.Button("No", size=(15, 2), pad=(350, 10))],
        [sg.Button("Exit", button_color=("white", "red"), size=(10, 1), pad=(350, 10))],
    ]

    window = sg.Window("YTCompare").Layout(sg_layout).Finalize()
    window.Size = window_size
    event, values = window.Read()
    window.Close()
    if event == "Yes":
        return True
    elif event == "No":
        return False
    elif event == "Exit" or event is None:
        raise SystemExit("Closing")

    window.Close()


def finished_working_GUI():
    text = "All done. Your song URLs can be found in a text document within the directory from where you ran this tool. (song_urls.txt)"
    sg.PopupScrolled(text)
    raise SystemExit("Closing")


if __name__ == "__main__":
    domain = "www.youtube.com/watch?v="

    events, values = gather_YouTube_input_from_GUI()

    api_key = values[0]
    playlist_id = values[1]

    event, local_directory = gather_local_input_from_GUI()
    print(local_directory)

    local_song_list = gather_local_data(local_directory)

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
                    if determine_song_similarity_from_GUI(
                        youtube_song_title, local_song
                    ):
                        song_needed = False
                        break
                    else:
                        song_needed = True
                elif youtube_song_title != local_song:
                    song_needed = True
            except IndexError:
                if determine_song_similarity_from_GUI(youtube_song_title, local_song):
                    song_needed = False
                    break
                else:
                    song_needed = True
        if song_needed:
            needed_songs[song_number] = {
                "Title": youtube_song_title,
                "URL": songs_and_urls[song]["URL"],
            }
            song_number += 1

    save_song_urls_to_disk(needed_songs)

    finished_working_GUI()
    print("Finished")
