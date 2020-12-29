import subprocess
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import romkan


member_list = {
    "Sora" : "ときのそら",
    "Roboco" : "ロボ子",
    "Miko" : "さくらみこ",
    "Suisei" : "星街すいせい",
    "Mel" : "夜空メル",
    "Fubuki" : "白上フブキ",
    "Matsuri" : "夏色まつり",
    "Aki" : "アキ・ローゼンタール",
    "Haachama" : "赤井はあと",
    "Aqua" : "湊あくあ",
    "Shion" : "紫咲シオン",
    "Ayame" : "百鬼あやめ",
    "Choco" : "癒月ちょこ",
    "Subaru" : "大空スバル",
    "Mio" : "大神ミオ",
    "Okayu" : "猫又おかゆ",
    "Korone" : "戌神ころね",
    "Pekora" : "兎田ぺこら",
    "Rushia" : "潤羽るしあ",
    "Flare" : "不知火フレア",
    "Marine" : "宝鐘マリン",
    "Noel" : "白銀ノエル",
    "Kanata" : "天音かなた",
    "Coco" : "桐生ココ",
    "Watame" : "角巻わため",
    "Towa" : "常闇トワ",
    "Luna" : "姫森ルーナ",
    "Lamy" : "雪花ラミィ",
    "Nene" : "桃鈴ねね",
    "Botan" : "獅白ぼたん",
    "Aloe" : "魔乃アロエ",
    "Polka" : "尾丸ポルカ",
    "Miyabi" : "花咲みやび",
    "Izuru" : "奏手イヅル",
    "Arurandeisu" : "アルランディス",
    "Rikka" : "律可",
    "Astel" : "アステル・レダ",
    "Temma" : "岸堂天真",
    "Roberu" : "夕刻ロベル",
    "Kaoru" : "月下カオル",
    "Shien" : "影山シエン",
    "Oga" : "荒咬オウガ"
    }

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
    if name in member_list:
        name = member_list[name]
    for stream in streams:
        if stream.find(text=re.compile(name)):
            vid = stream["href"]
            cmd = 'mpv '+vid
            print("cmd is "+cmd)
            subprocess.call(cmd, shell=True)
