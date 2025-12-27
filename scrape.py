'''
Scraper for the CCC Marketplace Website

Checks every in a random intervall between 0 and X seconds if there are Tickets available to buy.
This is done by searching for a specific phrase in the text of the Website, e.g: "no tickets available"
also make a "DING" Sound and opens the browser automatically for you
'''
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import subprocess

# replace URL with Marketplace-URL of the current Year
URL = "https://tickets.events.ccc.de/39c3/secondhand/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (ticket-checker; +https://example.com)"
}

# phrase to look for, when there are no tickets
text = "no tickets available at the moment. check back later!"

# Checks every 0 - X Seconds 
check_interval = 15

# on other OS-es, try a terminal based soundplayer - change path to the Soundfile
def beep():
    subprocess.Popen([
        "paplay",
        "/usr/share/sounds/freedesktop/stereo/complete.oga"
    ])

def check_tickets(text,url,headers):
    '''
    requests the Website and searches for the specific phrase

    also saves the HTML on success for later analysis
    '''
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Beispiel: Textsuche (robust, aber simpel)
    page_text = soup.get_text().lower()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if text not in page_text:
        print(f"JETZT {url} at {timestamp}")
        beep()
        subprocess.Popen([
            "firefox",
            "--new-window",
            url
        ])
        filename = f"responses/secondhand_{timestamp}.html"
        with open(filename, "w",encoding="utf-8") as f:
            f.write(r.text)
        return True
    else:
        print(f"nicht {url} at {timestamp}")
        return False

def main(check_interval,text,url,headers = {"User-Agent": "Mozilla/5.0 (ticket-checker; +https://example.com)"}):    
    '''
    glues everything together

    scrapes the website every 0 to check_interval seconds

    Parameters:
        check_interval(int): maximum time between checks
        text(str): phrase to look for in the html-webpage (e.g. no ticket available)
        url(str): url to the Marketpage
        headers(dict): common headers to supply
    
    '''
    while True:
        try:
            available = check_tickets(text,url,headers)

            if available:
                print("🎉 TICKETS MÖGLICHERWEISE VERFÜGBAR!")
                # hier könntest du abbrechen oder benachrichtigen
            else:
                print("❌ Keine Tickets verfügbar")

        except Exception as e:
            print("⚠️ Fehler beim Abrufen:", e)

        time.sleep(random.randint(0,check_interval))

if __name__ == "__main__":
    main(check_interval,text,URL,HEADERS)