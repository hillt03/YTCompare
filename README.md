# YTCompare
A GUI tool to compare YouTube playlist songs to songs on your local machine and outputs a text file with links to missing songs. Combine with [youtube-dl-gui](https://github.com/MrS0m30n3/youtube-dl-gui) to download any missing songs.  

This program will output a text file (song_urls.txt) containing the missing song URLs in the directory from which it was run.

## Requirements
Python 3

PySimpleGUI (`pip install PySimpleGUI` or `python -m pip install PySimpleGUI`)

 Requests (`pip install requests` or `python -m pip install requests`)
 
 You will have to provide a [YouTube Data v3 API key.](https://developers.google.com/youtube/v3/getting-started)

## Installation
Clone the repo or download `YTCompare.py`, run via command-line with `python YTCompare.py` and follow the prompts.

## FAQ
#### How do I find my YouTube playlist's ID?
Go to any video on your playlist and the URL will look similar to this:  
https://www.youtube.com/watch?v=HQs0u4i-wrU&list=PLdy_Z-y66LeLNgbrAq6fXnuO42Lolm_dD&index=241  
Copy the list attribute in the URL.  
In this example, the playlist ID would be `PLdy_Z-y66LeLNgbrAq6fXnuO42Lolm_dD`.

