import subprocess
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import romkan

def list_streams(streams):
    print("currently live: "+str(len(streams)))
    i = 0
    for stream in streams:
        idol = " ".join(stream.text.split())
        i += 1
        print(str(i)+'. '+idol + " / romaji: "+romkan.to_roma(idol)[6:])

ua = UserAgent(verify_ssl=False)
url="https://schedule.hololive.tv/lives/all"
cmd=''
while(True):
    response = requests.get(url, headers={'User-Agent':ua.chrome})
    soup = BeautifulSoup(response.text, 'html.parser')
    streams = soup.find_all("a", class_="thumbnail", style=lambda value: value and 'border: 3px red solid' in value)
    list_streams(streams)
    name = input("input the name of the holo: ")
    for stream in streams:
        if stream.find(text=re.compile(name)):
            vid = stream["href"]
            cmd = 'mpv '+vid
            print("cmd is "+cmd)
            subprocess.call(cmd, shell=True)
