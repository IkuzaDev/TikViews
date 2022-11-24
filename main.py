import datetime
import os,sys
import random
import time
import inquirer
import colorama
import requests
from src import process
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


layout = Layout()
date = datetime.datetime.now()
logo =  " _____ _ _  __   ___\n"
logo2 = "|_   _(_) |_\ \ / (_)_____ __ _____ \n"
logo3 = "  | | | | / /\ V /| / -_) V  V (_-< \n"
logo4 = "  |_| |_|_\_\ \_/ |_\___|\_/\_//__/ V 2.0.1 \n"
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
    os.system("clear")
    init(autoreset=True)
    inject = process.ZefoyViews()
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
        url_video = "https://www.tiktok.com/@gkpernahfyp_570/video/7147255332195077403"    
    time.sleep(1)

    if inject.post_solve_captcha(captcha_result=inject.captcha_solver()): 

        print("\n[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Success Solve Captcha" + "\n")
        os.system("clear")
        table = Table(title="")
        table.add_column("Date", justify="center", style="cyan", no_wrap=True)
        table.add_column("Service", justify="center", style="magenta")
        table.add_column("info", justify="center", style="green")

        status_services = inject.get_status_services()
        if status_services is None: print("Failed to get status services, try again later"); exit()

        valid_services = []
        for service in status_services:
            if service['name'] == 'Berak':
                continue
            elif 'ago updated' in service['status']:
                valid_services.append(service['name'])

            table.add_row(str(date.year) + ":" + str(date.strftime("%d")) + ":" + str(date.strftime("%b")), service['name'], service['status'])

        table.title = Fore.YELLOW + " Total Online Services: " + str(len(valid_services))
        console = Console()
        console.print(table)

        questions = [
            inquirer.List('type', message="What services do you need?", choices=valid_services, carousel=True, ), ]
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
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Views: " +
                                      inject_views['data'], end="\r")


                            elif inject_views['message'] == "Successfully views sent.":
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Status : " + "Success")
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_views['message'])
                                                              
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Views: " + inject_views['data'], end="\n\n")                               

                            elif inject_views['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_views[
                                    'message'])
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
                                    print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" + str(date.year) + " ]" + " CoolDown: " + str(
                                        i) + " seconds", end="\r")
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
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Shares : " +
                                      inject_shares['data'], end="\n\n")
                                print()


                            elif inject_shares['message'] == "Shares successfully sent.":
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Status : " + "Success")
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_shares['message'])
                                                              
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Share: " + inject_shares['data'], end="\n\n")        
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
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Favorites : " +
                                      inject_favorites['data'], end="\r")


                            elif inject_favorites['message'] == "Favorites successfully sent.":
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Status : " + "Success")
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_favorites['message'])
                                                              
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Favorite: " + inject_favorites['data'], end="\n\n")  

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
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Hearts : " +
                                      inject_hearts['data'], end="\r")
                                      

                            elif inject_hearts['message'] == "Hearts successfully sent.":
                               spinner.start()
                               time.sleep(3)
                               spinner.stop()
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Status : " + "Success")
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_hearts['message'])
                                                              
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Hearts: " + inject_hearts['data'], end="\n\n")
                               print()

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
                        elif answers['type'] == 'Comments Hearts':

                    while True:
                        inject_CH = inject.send_multi_services(url_video=url_video, services=answers['type'], )

                        if inject_CH:                          

                            if inject_CH['message'] == "Please try again later":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_CH[
                                    'message'])
                                exit()

                            elif inject_CH['message'] == 'Another State':
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Comment : " +
                                      inject_CH['data'], end="\r")
                                      

                            elif inject_CH['message'] == "Hearts successfully sent.":
                               spinner.start()
                               time.sleep(3)
                               spinner.stop()
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Status : " + "Success")
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_CH['message'])
                                                              
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Hearts: " + inject_CH['data'], end="\n\n")
                               print()

                            elif inject_CH['message'] == "Session Expired. Please Re Login!":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_CH[
                                    'message'])
                                exit()

                            elif inject_CH['message'] == "Video not found.":
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_CH[
                                    'message'])
                                exit()

                            else:                           
                               spinner.start()
                               time.sleep(3) 
                               spinner.stop()
                               for i in range(int(inject_CH['message']), 0, -1):
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
                                print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Hearts : " +
                                      inject_hearts['data'], end="\r")
                                      

                            elif inject_follow['message'] == "Hearts successfully sent.":
                               spinner.start()
                               time.sleep(3)
                               spinner.stop()
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Status : " + "Success")
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + inject_follow['message'])
                                                              
                               print("[ " + str(date.strftime("%d")) + ":" + str(date.strftime("%b")) + ":" +  str(date.year)  +" ] " + "Current Followers: " + inject_follow['data'], end="\n\n")
                               print()

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

            except Exception as e:
                pass

    else:
        print("Failed to solve captcha.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os.system("clear")
        print("Exit")
        exit()
