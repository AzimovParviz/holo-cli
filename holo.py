import subprocess
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re

ua = UserAgent(verify_ssl=False)
url="https://schedule.hololive.tv/lives/all"
response = requests.get(url, headers={'User-Agent':ua.chrome})
soup = BeautifulSoup(response.text, 'html.parser')
name = input("input the name of the holo(s) in kana(or hiragana i don't know the difference lmao): ")
streams = soup.find_all("a", class_="thumbnail")
for stream in streams:
    print(stream["href"])
    if stream.find(text=re.compile(name)):
        vid = stream["href"]
        print("link is: "+vid)
        cmd = 'mpv '+vid
        print("cmd is "+cmd)
subprocess.call(cmd, shell=True)
