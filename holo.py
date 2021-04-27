<<<<<<< HEAD
#!/usr/bin/env python
=======
#!/usr/bin/env python3
>>>>>>> a63b5b93176740338467a9fac114581113bd142b
import subprocess
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import sys, getopt
import datetime
import os

member_list = {
    "Sora" : "ときのそら",
    "Roboco" : "ロボ子",
    "Miko" : "さくらみこ",
    "Suisei" : "星街すいせい",
    "Mel" : "夜空メル",
    "Fubuki" : "白上フブキ",
    "Matsuri" : "夏色まつり",
    "Aki" : "アキロゼ",
    "Haato" : "赤井はあと",
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
    "Aruran" : "アルランディス",
    "Rikka" : "律可",
    "Astel" : "アステル・レダ",
    "Temma" : "岸堂天真",
    "Roberu" : "夕刻ロベル",
    "Kaoru" : "月下カオル",
    "Shien" : "影山シエン",
    "Oga" : "荒咬オウガ"
    }

def list_streams(streams, sv):
    print("currently live: "+str(len(streams)))
    i = 0
    for stream in streams:
        idol = " ".join(stream.text.split())
        idol_en = idol[6:]#removing the time of the broadcast from html elemenet containing the streamer's name
        idol_time = idol[:5]+':00'#getting the time of the broadcast
        now = datetime.datetime.now()
        current_time = datetime.datetime.strptime(idol_time,"%H:%M:%S")
        current_time = now.replace(hour=current_time.time().hour, minute=current_time.time().minute, second=current_time.time().second, microsecond=0)#changing the format of the current time to match the time format of the schedule website
        i += 1
        if sv == 'border: 3px red solid':
            for key, name in member_list.items():
                if name in idol:
                    idol_en = key
            print(str(i)+'. '+idol + " / romaji: "+ idol_en)
        elif sv == 'border: 0':
            for key, name in member_list.items():
                if (name in idol) & (idol_time>=str(current_time)):
                    idol_en = key
                    print(str(i)+'. '+idol + " / romaji: "+ idol_en)

def main(argv):
    search_value = ""#variable that will be used to determine whether live or upcoming livestreams are to be shown
    try:
        opts, args = getopt.getopt(argv,"hlu")
    except getopt.GetoptError:
        print ('holo.py -h for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('-l lists currently live streams\n -u lists upcoming streams')
            sys.exit()
        elif opt in ("-l"):
            search_value = 'border: 3px red solid'#currently live streams are marked with a red border on the schedule website
        elif opt in ("-u"):
            search_value = 'border: 0'#property of non live streams on the schedule website
    ua = UserAgent(verify_ssl=False)
    url="https://schedule.hololive.tv/lives/all"
    cookies = {'timezone':'Europe/Helsinki'}
    while(True):#while(True) so the user can repeatedly fetch new information from the schedule website after closing the stream they were watching before
        cmd=''
        response = requests.get(url, headers={'User-Agent':ua.chrome}, cookies=cookies)#making a request to the schedule website, using chrome headers from fake-useragent and cookies for the timezone
        soup = BeautifulSoup(response.text, 'html.parser')
        streams = soup.find_all("a", class_="thumbnail", style=lambda value: value and search_value in value)#finding the streams based on the option passed to the program
        list_streams(streams, search_value)
        name = input("input the name of the holo(s) separated by space: ")
        if " " in name:#case of passing several vtubers to open multiple streams
            name = name.split(" ")
            for item in name:
                print(item)
            for stream in streams:
                for item in name:
                    if item in member_list:
                        item = member_list[item]
                    if stream.find(text=re.compile(item)):
                        vid = stream["href"]
                        cmd += 'mpv --really-quiet '+vid+' & '

        else:#when only a single name is passed
            if name in member_list:
                name = member_list[name]
            for stream in streams:
                if stream.find(text=re.compile(name)):
                    vid = stream["href"]
                    cmd += 'mpv --really-quiet '+vid
        subprocess.call(cmd, shell=True)#executing the final command containing either one or several streams
        os.system('stty sane')#sometimes the inputted name(s) do not show up in the terminal
        #(may be related to system slowing down after having too many instances of mpv open
        #requires more testing
if __name__ == "__main__":
   main(sys.argv[1:])
