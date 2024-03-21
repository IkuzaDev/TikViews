import re
import base64
import requests
import urllib.parse
import json
from datetime import datetime
from time import time, sleep
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper
import random
from hashlib import sha256
import os,sys
import random
import time
import inquirer
import colorama
import requests
import rich
from rich import *
from rich.table import Table
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from halo import Halo
from colorama import init, Fore

spinner = Halo(text='Loading', spinner='dots')
date = datetime.now()
class ZefoyViews:
    API_ZEFOY = 'https://zefoy.com/'
    API_VISION = 'http://127.0.0.1:8000/api/'
    TOKEN_FILE_PATH='metabypass.token'

    # Your Credentials
    CLIENT_ID='1374' #****CHANGE HERE WITH YOUR VALUE*******
    CLIENT_SECRET='NkuXGmViy9gQ3hYXlcVh3aPhbdtv7LXVdO6Egmok' #****CHANGE HERE WITH YOUR VALUE*******
    EMAIL='dragon.studio.official@gmail.com' #****CHANGE HERE WITH YOUR VALUE*******
    PASSWORD='084@151396074#3402641=!46' #****CHANGE HERE WITH YOUR VALUE*******

    STATIC_HEADERS = {
        'authority': 'zefoy.com',
        'origin': 'https://zefoy.com',
        'authority': 'zefoy.com',
        'cp-extension-installed': 'Yes',
        'X-Requested-With' : 'XMLHttpRequest',
        'Accept' : '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',         
    }

    STATIC_ENDPOINT = {}

    def __init__(self):
        self.key_views = None
        self.send_key = None
        self.session = requests.Session()
        self.cfProtect = None
        self.captcha = None
        self.spinner = None
        self.spoof = None
        self.captcha_ = {}
        self.STATIC_HEADERS = {
            'authority': 'zefoy.com',
            'origin': 'https://zefoy.com',
            'authority': 'zefoy.com',
            'Via' : self.spoof,
            'Client-IP' : self.spoof,
            'X-Forwarded-For' : self.spoof,
            'Real-IP' : self.spoof,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',         
        }
        self.scraper = cloudscraper.create_scraper(disableCloudflareV1=True, browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}, sess=self.session)
        self.phpsessid = requests.Session().cookies.get("PHPSESSID")

        #video info
        self.info = {}

    def google_ads_inject(self):
        #("Ads Injecting")
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Ads Injecting")
        #self.spinner = Halo(text='Ads Injecting', spinner='dots')
        #self.spinner.start()
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Start API Injecting")
        request_gfp = self.session.get(
            url='https://partner.googleadservices.com/gampad/cookie.js?domain=zefoy.com&callback=_gfp_s_&client=ca-pub-3192305768699763&gpid_exp=1',
            headers={
                "Host": "partner.googleadservices.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            }
        )

        self.session.cookies.set("_gads", request_gfp.text.strip().split('_value_":"')[1].split('","_expires_')[0], domain='zefoy.com')
        self.session.cookies.set("__gpi", request_gfp.text.strip().split('_value_":"')[2].split('","_expires_')[0], domain='zefoy.com')
        #exit(request_gfp.text.strip())
        ##print("Done Injecting")
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Done Injecting")
        #self.spinner.stop()
    
    def get_video_info(self, url, useapi):
        request = self.session.get(f'https://tiktok.livecounts.io/video/stats/{urlparse(url).path.rpartition("/")[2]}',headers={'authority':'tiktok.livecounts.io','origin':'https://livecounts.io','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}).json()
        if 'viewCount' in request: 
            self.info = request
            return self.info
        else: 
            self.info = {'viewCount':0, 'likeCount':0,'commentCount':0,'shareCount':0}
            return self.info
        
    def captcha_solver(self):
        ##print("start Solver")
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Captcha Solver")
        try:
            #access_token = self.getNewAccessToken()
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Start API Solver")
            solve_captcha = self.scraper.post(
                url='https://1c8e-119-235-221-36.ngrok-free.app/api/',
                headers={
                    'ngrok-skip-browser-warning': 'True',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                json={
                    'service': 'OCR',
                    'api_key': '1d32fd2958bd6010e5cab334c98fa896',
                    "image": base64.b64encode(open('captcha.png', 'rb').read()).decode('utf-8'),
                    'current_time': datetime.now().strftime("%H:%M:%S")
                }
            )
            return solve_captcha.json()['data']
        except TypeError:
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "RELOAD")
            return "reload"

    def get_session_captcha(self):
        ##print("get session")
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Getting Session")

        addr = [192, 168, 0, 1]
        d = '.'
        addr[0] = str(random.randrange(11, 197))
        addr[1] = str(random.randrange(0, 255))
        addr[2] = str(random.randrange(0, 255))
        addr[3] = str(random.randrange(2, 254))
        self.spoof = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]

        #self.spinner = Halo(text='Getting Session', spinner='dots')
        #self.spinner.start()
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Start API")
        homepage = self.session.get(
            url=self.API_ZEFOY,
            headers=self.STATIC_HEADERS
        )
        
        soup = BeautifulSoup(homepage.text, 'html.parser')
        if homepage.cookies.get_dict().get('gfp') is None:
            ##print("gfp Not found trying inject ads")
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Trying Ads Inject")
            self.google_ads_inject()

        try:
            request_captcha_image = self.session.get(
                url=self.API_ZEFOY + soup.find('img', {'onerror': 'imgOnError()'}).get('src'),
                headers=self.STATIC_HEADERS,
            )
            
            self.send_key = soup.find('input', {'oninput': 'this.value=this.value.toLowerCase()'}).get('name')
            #print("Send Key : " + soup.find('input', {'oninput': 'this.value=this.value.toLowerCase()'}).get('name'))
            
            with open('captcha.png', 'wb') as f:
                f.write(request_captcha_image.content)
        except AttributeError:
            self.get_session_captcha()
        #self.spinner.stop()
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Done Get Session")
        
    def post_solve_captcha(self, captcha_result):
        #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Post captcha result")
        try:
            #self.session.cookies.set("PHPSESSID", self.phpsessid, domain='zefoy.com')

            self.STATIC_HEADERS['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"
            
            
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Post to API Solver")
            self.captcha_[self.send_key] = captcha_result
            self.captcha_['captcha_secure'] = captcha_result

            try:
                post_captcha = self.scraper.post(
                    url=self.API_ZEFOY,
                    headers=self.STATIC_HEADERS,
                    data=self.captcha_
                )
                soup = BeautifulSoup(post_captcha.text, 'html.parser')
                #exit(soup)
                self.key_views = soup.find('input', {'placeholder': 'Enter Video URL'}).get('name')
                return True
            except ConnectionError :
                #print("Error: ")
                self.post_solve_captcha(captcha_result)
        except Exception as e:
            #print("Error: " + str(e))
            ##print(soup)
            return False
            

    def get_status_services(self):
        try:
            #print("Get Service List")
            temp_status_1 = []
            temp_status_2 = []

            self.STATIC_HEADERS['content-type'] = "text/html; charset=UTF-8"

            get_status_services = self.session.get(
                url=self.API_ZEFOY,
                headers=self.STATIC_HEADERS,
            )
            soup = BeautifulSoup(get_status_services.text, 'html.parser')
            #exit(soup)
            for x in soup.find_all('div', {'class': 'card m-b-20 card-ortlax'}):
                #print(x.find('form').get('action').strip() + " [Found]")
                temp_status_1.append({
                    'name': x.find('h5').text.strip(),
                    'key': x.find('form').get('action').strip(),
                })

            for i in soup.find_all('div', {'class': 'col-sm-4 col-xs-12 p-1 colsmenu'}):
                ##print(i.find('h5').text.strip() + " [Found]")
                temp_status_2.append({
                    'name': i.findNext('h5').text.strip(),
                    'status': i.findNext('small').text.strip()
                })

            for key in temp_status_1:
                for status in temp_status_2:
                    if key['name'] == status['name']:
                        self.STATIC_ENDPOINT.update(
                            {
                                status['name']: key['key']
                            }
                        )

            return temp_status_2

        except Exception:
            self.get_status_services()

    def send_multi_services(self, url_video, services):
        global soup
        try:

            self.STATIC_HEADERS['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"
            ##print(self.key_views)
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Start " + str(services) +" Service")
            post_services = self.session.post(
                url=self.API_ZEFOY + self.STATIC_ENDPOINT[services],
                headers=self.STATIC_HEADERS,
                data={self.key_views: url_video}
            )
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Decodeing " + str(services) +" Service")
            decode_old = base64.b64decode(urllib.parse.unquote(post_services.text[::-1])).decode()
            ##print(self.key_views)
            #exit(decode_old)
            soup = BeautifulSoup(decode_old, 'html.parser')
            #print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Parsing " + str(services) +" Service")

            if "This service is currently not working" in soup.text:
                exit("This service is currently not working")

            if "An error occurred. Please try again." in decode_old:
                try:
                    decode = self.force_send_multi_services(
                        url_video=url_video,
                        old_request=decode_old,
                        services=services
                    )
                    
                    soupDecode = BeautifulSoup(decode, 'html.parser')
                    #exit(soupDecode)
                    if "Successfully " + services.lower() + " sent." in soupDecode.text:
                        self.get_video_info(url_video, False)
                        return {'message': 'Successfully ' + services.lower() + ' sent.', 'data': soup.find('button').text.strip()}
                    elif services + " successfully sent" in soupDecode.find('span').text:
                        self.get_video_info(url_video, False)
                        return {'message': services + ' successfully sent.', 'data': soup.find('button').text.strip() + " > " + soupDecode.find('span').text.strip()}
                    else:
                        return {'message': 'Another State', 'data': soup.find('button').text.strip()}
                except Exception as err:
                    #print("Trying Again :" + str(err))
                    self.send_multi_services(url_video, services)

            elif "Successfully " + services.lower() + " sent." in decode_old:
                self.get_video_info(url_video, False)
                return {
                    'message': 'Successfully ' + services.lower() + ' sent.',
                    'data': soup.find('button').text.strip()
                }

            elif "Session Expired. Please Re Login!" in decode_old:
                return {
                    'message': 'Please try again later. Server too busy.',
                }

            elif "Not found video." in decode_old:
                return {
                    'message': 'Video not found.',
                }
            elif "Too many requests. Please slow down." in decode_old:
                return {
                    'message': 'Please Slow Down',
                }
            # Getting Timer
            try:

                return {
                    'message': re.search(r"var ltm=[0-9]+;", decode_old).group(0).replace("ltm=", "") \
                        .replace(";", "").replace("var", "").strip()
                }
            except:
                pass

        except Exception as e:

            return "Error: " + str(e)

    def force_send_multi_services(self, url_video, services, old_request):
        if 'tiktok' in url_video:
            if len(urlparse(url_video).path.split('/')[-1]) == 19:
                valid_id = urlparse(url_video).path.split('/')[-1]
            else:
                return False
        else:
            return False

        parse = BeautifulSoup(old_request, 'html.parser')
        #exit(parse)
        request_force_multiple_services = self.session.post(
            url=self.API_ZEFOY + self.STATIC_ENDPOINT[services],
            headers=self.STATIC_HEADERS,
            data={
                parse.find('input', {'type': 'hidden'}).get('name'): valid_id,
            }
        )
        decode = base64.b64decode(urllib.parse.unquote(request_force_multiple_services.text[::-1])).decode()
        return decode

                    
layout = Layout()
logo =  " _____ _ _  __   ___\n"
logo2 = "|_   _(_) |_\ \ / (_)_____ __ _____ \n"
logo3 = "  | | | | / /\ V /| / -_) V  V (_-< \n"
logo4 = "  |_| |_|_\_\ \_/ |_\___|\_/\_//__/ V 3.0 \n"
logo5 = "  by D5Studio"
text = Text()
console = Console()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    os.system("cls")
    init(autoreset=True)
    inject = ZefoyViews()
    inject.get_session_captcha()
    layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
    )
    layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="right"),
    )
    layout["upper"].split(
    Layout(Panel(Text(logo, style="blue") + Text(logo2, style="blue") + Text(logo3, style="blue") + Text(logo4, style="blue") + Text(logo5, style="blue")))
    )
    layout["right"].split(
    Layout(Panel(" FB : IkuzaDev \n Link : https://www.facebook.com/RRQ.IKz")),
    Layout(Panel(" YT : Ikuza Dev \n Link : https://www.facebook.com/RRQ.IKz")),  
    Layout(Panel("Credits : \n 1. Boby Ferdian \n 2. Seno \n 3. ARGHOZALIDEV"))
    )
    layout["left"].split(
    Layout(Panel("         How To Use      \n 1. Follow Facebook GW \n 2. copy link video \n 3. Paste pada tools \n 4. pilih layanan \n 5. tunggu cooldown \n 6. Finish")),
    )
    layout["upper"].size = 8
    layout["upper"].ratio = 1
    layout["left"].size = 30
    layout["right"].ratio = 3
    layout["left"].ratio = 3
    print(layout)
    
    console = Console()
    text.append("Example:", style="bold magenta")
    text.append("https://www.tiktok.com/@[User_Name]/video/[ID_Video]", style="bold blue")
    console.print(text)
    url_video = input("Enter URL Video: ")
    if url_video == "":
        url_video = "https://www.tiktok.com/@x.mbloo/video/7317539346972986630"    
    time.sleep(1)

    if inject.post_solve_captcha(captcha_result=inject.captcha_solver()): 

        print("\n[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Success Solve Captcha" + "\n")
        os.system("cls")
        table = Table(title="")
        table.add_column("Date", justify="center", style="cyan", no_wrap=True)
        table.add_column("Service", justify="center", style="magenta")
        table.add_column("info", justify="center", style="green")

        status_services = inject.get_status_services()
        if not status_services: 
            #print("Failed to get status services, try again later"); 
            status_services = inject.get_status_services()

        valid_services = []
        for service in status_services:
            if service['name'] == ' ' or service['name'] == ' ':
                continue
            elif 'ago updated' in service['status']:
                valid_services.append(service['name'])

            table.add_row(str(date.year) + ":" + str(date.strftime("%d")) + ":" + str(date.strftime("%b")), service['name'], service['status'])

        table.title = Fore.YELLOW + " Total Online Services: " + str(len(valid_services))
        console = Console()
        console.print(table)

        stats = inject.get_video_info(url_video, False)
        #exit(str(stats))
        print("[ " + "Video Stat"  +" ] " + "-Like : " + str(stats['likeCount']) + " -View : " + str(stats['viewCount']) + " -Share : " +  str(stats['shareCount']))
        
        questions = [inquirer.List('type', message="What services do you need?", choices=valid_services, carousel=True, ), ]
        answers = inquirer.prompt(questions)

        while True:

            try:

                if answers['type'] == 'Views':

                    while True:
                        inject_views = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_views:

                            if inject_views['message'] == "Please try again later":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_views[
                                    'message'])
                                exit()

                            elif inject_views['message'] == 'Another State':
                                spinner.start()
                                stats = inject.get_video_info(url_video, False)
                                spinner.stop()


                            elif inject_views['message'] == "Successfully views sent.":
                               spinner.start()
                               stats = inject.get_video_info(url_video, False)
                               spinner.stop()

                            elif inject_views['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_views['message'])
                                exit()

                            elif inject_views['message'] == "Video not found.":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_views[
                                    'message'])
                                exit()

                            else:
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               
                               for i in range(int(inject_views['message']), 0, -1):
                                    print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" + str(date.year) + " ]" + " CoolDown: " + str(i) + " seconds", end="\r")
                                    time.sleep(1)
                        else:
                            pass

                elif answers['type'] == 'Shares':

                    while True:
                        inject_shares = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_shares:

                            if inject_shares['message'] == "Please try again later":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_shares[
                                    'message'])
                                exit()

                            elif inject_shares['message'] == 'Another State':
                                spinner.start()
                                stats = inject.get_video_info(url_video, False)
                                spinner.stop()
                               


                            elif inject_shares['message'] == "Shares successfully sent.":
                               spinner.start()
                               stats = inject.get_video_info(url_video, False)
                               spinner.stop()
                            elif inject_shares['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_shares[
                                    'message'])
                                exit()

                            elif inject_shares['message'] == "Video not found.":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_shares[
                                    'message'])
                                exit()

                            else:
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               for i in range(int(inject_shares['message']), 0, -1):
                                    print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" + str(date.year) + " ]" + " CoolDown: " + str(
                                        i) + " seconds", end="\r")
                                    time.sleep(1)

                            time.sleep(random.randint(1, 5))

                        else:
                            pass

                elif answers['type'] == 'Favorites':

                    while True:
                        inject_favorites = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_favorites:

                            if inject_favorites['message'] == "Please try again later":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_favorites[
                                    'message'])
                                exit()
                            
                            elif inject_favorites['message'] == 'Another State':
                                spinner.start()
                                stats = inject.get_video_info(url_video, False)
                                spinner.stop()
                               

                            elif inject_favorites['message'] == "Favorites successfully sent.":
                               spinner.start()
                               stats = inject.get_video_info(url_video, False) 
                               spinner.stop()
                               
                            elif inject_favorites['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_favorites[
                                    'message'])
                                exit()

                            elif inject_favorites['message'] == "Video not found.":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_favorites[
                                    'message'])
                                exit()


                            else:
                              spinner.start()
                              time.sleep(3)
                              spinner.stop()
                              for i in range(int(inject_favorites['message']), 0, -1):
                                    print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" + str(date.year) + " ]" + " CoolDown: " + str(
                                        i) + " seconds.", end="\r")
                                    time.sleep(1)

                            time.sleep(random.randint(1, 5))

                        else:
                            pass

                elif answers['type'] == 'Hearts':

                    while True:
                        inject_hearts = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_hearts:                          

                            if inject_hearts['message'] == "Please try again later":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_hearts[
                                    'message'])
                                exit()

                            elif inject_hearts['message'] == 'Another State':
                                spinner.start()
                                stats = inject.get_video_info(url_video, False)
                                spinner.stop()
                                      

                            elif inject_hearts['message'] == "Hearts successfully sent.":
                               spinner.start()
                               stats = inject.get_video_info(url_video, False)
                               spinner.stop()
                               
                            elif inject_hearts['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_hearts[
                                    'message'])
                                exit()

                            elif inject_hearts['message'] == "Video not found.":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_hearts[
                                    'message'])
                                exit()

                            else:                           
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               for i in range(int(inject_hearts['message']), 0, -1):
                                    print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" + str(date.year) + " ]" + " CoolDown " + str(i) + " seconds.", end="\r")
                                    time.sleep(1)                                  
                        else:
                            pass
                
                elif answers['type'] == 'Followers':

                    while True:
                        inject_follow = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_follow:                          

                            if inject_follow['message'] == "Please try again later":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_follow[
                                    'message'])
                                exit()

                            elif inject_follow['message'] == 'Another State':
                                spinner.start()
                                stats = inject.get_video_info(url_video, False)
                                spinner.stop()
                                      

                            elif inject_follow['message'] == "Hearts successfully sent.":
                               spinner.start()
                               stats = inject.get_video_info(url_video, False)
                               spinner.stop()
                               
                            elif inject_follow['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_follow[
                                    'message'])
                                exit()

                            elif inject_follow['message'] == "Video not found.":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_follow[
                                    'message'])
                                exit()

                            else:                           
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               for i in range(int(inject_follow['message']), 0, -1):
                                    print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" + str(date.year) + " ]" + " CoolDown " + str(i) + " seconds.", end="\r")
                                    time.sleep(1)                                  
                        else:
                            pass
                
                elif answers['type'] == 'Comments Hearts':
                            spinner.start()
                            time.sleep(2)
                            spinner.stop()
                            print("under maintenance")

            except Exception as e:
                pass

    else:
        print("Failed to solve captcha.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os.system("cls")
        print("Exit")
        exit()


