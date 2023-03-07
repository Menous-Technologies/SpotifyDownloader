import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import eyed3
from eyed3.id3.frames import ImageFrame
from pytube import YouTube
from moviepy.editor import *
import os
import youtube
from pytube import Search

clientId = "17afd740ee4a41ea9e6c79605a4a2a37"
clientSecret = "264e23c7d072426b89b4182edc0a524e"

def pdownload(url, name):
    req = requests.get(url)
    with open('images/'+name+'.jpg', 'wb') as file:
        file.write(req.content)


def Download(link, name):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download('music', filename=name+'.mp4')
    except:
        print("An error has occurred")

    video = VideoFileClip('music/'+name+".mp4")
    video.audio.write_audiofile('music/'+name+".mp3")
    os.remove('music/'+name+".mp4")

def searchYoutube(name):
    x = Search(name).results
    if len(x) == 0:
        return 'Not Found'
    else:
        return x[0].watch_url




# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(
    client_id=clientId, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
playlist_link = input('enter playlist link: ')
print('lol')
playlist = sp.playlist_tracks(playlist_link)


for i in playlist['items']:
    name = i['track']['name']
    artist = i['track']['artists'][0]['name']
    album = i['track']['album']['name']
    print(name)
    ur = i['track']['album']['images'][0]['url']
    pdownload(ur, name)

    url = searchYoutube(name+" "+artist)
    print(url)

    Download(url, name.replace(' ', '-'))
    audiofile = eyed3.load('music/'+name.replace(' ', '-')+'.mp3')
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(
        'images/'+name+'.jpg', 'rb').read(), 'image/jpeg')
    audiofile.tag.artist = artist
    audiofile.tag.title = name
    audiofile.tag.album = album
    audiofile.tag.save()

