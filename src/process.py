import re
import base64
import requests
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# source : https://github.com/sandrocods/Zefoy-Automation
# for debug
# from requests_toolbelt.utils import dump


class ZefoyViews:
    API_ZEFOY = 'https://zefoy.com/'
    API_VISION = 'https://api.sandroputraa.com/zefoy.php'

    STATIC_HEADERS = {
        "Host": "zefoy.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "origin": "https://zefoy.com",
    }

    STATIC_ENDPOINT = {
        "Views": "c2VuZC9mb2xsb3dlcnNfdGlrdG9V",
        "Shares": "c2VuZC9mb2xsb3dlcnNfdGlrdG9s",
        "Favorites": "c2VuZF9mb2xsb3dlcnNfdGlrdG9L",
        "Hearts": "c2VuZE9nb2xsb3dlcnNfdGlrdG9r"
    }

    def __init__(self):
        self.key_views = None
        self.session = requests.Session()
        self.google_ads_inject()
        self.captcha = None
        self.phpsessid = None

    def google_ads_inject(self):

        request_gfp = self.session.get(
            url='https://partner.googleadservices.com/gampad/cookie.js?domain=zefoy.com&callback=_gfp_s_&client=ca-pub-3192305768699763&gpid_exp=1 ',
            headers={
                "Host": "partner.googleadservices.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            }
        )
        self.session.cookies.set("_gads", request_gfp.text.strip().split('_value_":"')[1].split('","_expires_')[0],
                                 domain='zefoy.com')
        self.session.cookies.set("__gpi", request_gfp.text.strip().split('_value_":"')[2].split('","_expires_')[0],
                                 domain='zefoy.com')

    def captcha_solver(self):
        solve_captcha = requests.post(
            url=self.API_VISION,
            headers={
                'Content-Type': 'application/json',
                'Auth': 'sandroputraa',
                'Host': 'api.sandroputraa.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            },
            json={
                "img": base64.b64encode(open('captcha.png', 'rb').read()).decode('utf-8')
            }
        )
        if solve_captcha.status_code == 200 and solve_captcha.json()['message'] == 'Success':
            return solve_captcha.json()['Data']
        else:
            exit("Error Captcha : " + solve_captcha.json()['message'])

    def get_session_captcha(self):
        homepage = self.session.get(
            url=self.API_ZEFOY,
            headers=self.STATIC_HEADERS
        )
        soup = BeautifulSoup(homepage.text, 'html.parser')

        # Download Captcha Image
        try:

            request_captcha_image = self.session.get(
                url=self.API_ZEFOY + soup.find('img', {'alt': 'CAPTCHA code'}).get('src'),
                headers=self.STATIC_HEADERS,
            )

            with open('captcha.png', 'wb') as f:
                f.write(request_captcha_image.content)

        except AttributeError:
            self.get_session_captcha()

    def post_solve_captcha(self, captcha_result):
        try:

            self.STATIC_HEADERS['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"

            post_captcha = self.session.post(
                url=self.API_ZEFOY,
                headers=self.STATIC_HEADERS,
                data={
                    'captcha_secure': captcha_result,
                    'r75619cf53f5a5d7aa6af82edfec3bf0': '',
                }
            )
            soup = BeautifulSoup(post_captcha.text, 'html.parser')
            self.key_views = soup.find('input', {'placeholder': 'Enter Video URL'}).get('name')
            return True
        except Exception as e:
            return "Error: " + str(e)

    def get_status_services(self):
        try:
            temp_status = []

            self.STATIC_HEADERS['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"

            get_status_services = self.session.get(
                url=self.API_ZEFOY,
                headers=self.STATIC_HEADERS,
            )
            soup = BeautifulSoup(get_status_services.text, 'html.parser')
            for i in soup.find_all('div', {'class': 'col-sm-4 col-xs-12 p-1 colsmenu'}):
                temp_status.append({
                    'name': i.findNext('h5').text.strip(),
                    'status': i.findNext('small').text.strip()
                })
            return temp_status
        except Exception:
            self.get_status_services()

    def send_multi_services(self, url_video, services):
        global soup
        try:

            self.STATIC_HEADERS['content-type'] = "application/x-www-form-urlencoded; charset=UTF-8"

            post_services = self.session.post(
                url=self.API_ZEFOY + self.STATIC_ENDPOINT[services],
                headers=self.STATIC_HEADERS,
                data={
                    self.key_views: url_video,
                }
            )

            decode_old = base64.b64decode(urllib.parse.unquote(post_services.text[::-1])).decode()
            soup = BeautifulSoup(decode_old, 'html.parser')
            if "This service is currently not working" in soup.text:
                exit("This service is currently not working")

            if "An error occurred. Please try again." in decode_old:

                decode = self.force_send_multi_services(
                    url_video=url_video,
                    old_request=decode_old,
                    services=services
                )

                # print("Force Send: " + decode.__str__())
                soupDecode = BeautifulSoup(decode, 'html.parser')
                if "Successfully " + services.lower() + " sent." in soupDecode.text:
                    return {
                        'message': 'Successfully ' + services.lower() + ' sent.',
                        'data': soup.find('button').text.strip()
                    }

                elif services +" successfully sent" in soupDecode.find('span').text:
                    return {
                        'message': services + ' successfully sent.',
                        'data': soup.find('button').text.strip() + " + " + soupDecode.find('span').text.strip()
                    }

                else:
                    return {
                        'message': 'Another State',
                        'data': soup.find('button').text.strip()
                    }

            elif "Successfully " + services.lower() + " sent." in decode_old:
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
        request_force_multiple_services = self.session.post(
            url=self.API_ZEFOY + self.STATIC_ENDPOINT[services],
            headers=self.STATIC_HEADERS,
            data={
                parse.find('input', {'type': 'text'}).get('name'): valid_id,
            }
        )
        decode = base64.b64decode(urllib.parse.unquote(request_force_multiple_services.text[::-1])).decode()
        return decode
