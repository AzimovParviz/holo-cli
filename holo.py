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
streams = soup.find_all("a", class_="thumbnail", style=lambda value: value and 'border: 3px red solid' in value)
#lives = streams.find_all("div", class_="name")
print("currently live: "+str(len(streams)))
cmd=''
i = 0
for stream in streams:
    print(stream.text.strip())
    i += 1
    if stream.find(text=re.compile(name)):
        vid = stream["href"]
        cmd = 'mpv '+vid
if cmd:
    print("cmd is "+cmd)
    subprocess.call(cmd, shell=True)
else:
    print("No live events found")
