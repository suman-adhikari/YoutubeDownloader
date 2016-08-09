import urllib2
import urllib
import subprocess
import time
import re
import string
from easygui import *
from random import randint

play_list = fileopenbox(msg="Select your playlist", title="List",default="~/")
#audio_video = buttonbox("Choose your format",choices=["Audio","video"])
save_location = diropenbox(msg="Where would you like to save?",title="Target location",default="~/Videos")
error_log = open(save_location+'/Log.txt','a')
playlist = open(play_list,'r')
songs = playlist.readlines()
playlist.close()
song_flag = 0


for row in songs:
    item = row.split("-")
    song = item[0]
    format = item[1]
    print item
    query = song
    url = "http://www.google.com/search?&"
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    query = urllib.urlencode( {'q' : query } )
    print url+query
    response = opener.open(url+query).read()
    #urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response)
    urls = re.findall(r"https?://\w+\.\w+[\.|\w+|/|=|?|&|-]+",response)

    for url in urls:
        if re.search(r'https://www.youtube.com/watch\?v=',url,re.M|re.I):
            url = string.replace(url,"</cite><span","")
            print "downloading "+ song + ": " + url
            decoded_url=urllib.unquote(url).decode('utf8')
            print decoded_url
            if format=='a\n':
                subprocess.call(['youtube-dl','-o',save_location+'/audio/%(title)s.%(ext)s',"--extract-audio","--audio-format","mp3",decoded_url])
                song_flag = 1
            elif format=='v\n':
                subprocess.call(['youtube-dl','-o',save_location+'/video/%(title)s.%(ext)s',decoded_url])
                song_flag = 1
            break;
    else:
        print url

    if song_flag:
        msg = song + " Downloaded"
        print msg
        print "_______________________________________"
        error_log.write(msg)
    else:
        msg = song + " Failed Downloading"
        print msg
        print "_______________________________________"
        error_log.write(msg)









