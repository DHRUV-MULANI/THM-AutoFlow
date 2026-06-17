#!/usr/bin/env python3
import requests
import time

# Configuration
URL = "https://tryhackme.com/api/v2/rooms/answer"
CSRF_TOKEN = "CbVClS29-CrJE-aL6X0hMUUxSbdDqoNyQw_U"

# Headers from your capture
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "csrf-token": CSRF_TOKEN,
    "Origin": "https://tryhackme.com",
    "Referer": "https://tryhackme.com/room/jrsecanalystintrouxo",
}

# Your full session cookies
COOKIES_RAW = 'thm-aid=cfda34c3-9d56-4d20-b7c9-31f3f5a1bc2c; cookie_consent_preferences={"essential":true,"analytics":false,"marketing":false}; cookieconsent_status=dismiss; _csrf=abJu8CUR5P9joovruZofW6GH; cf_clearance=wE.0E1lDmFctE5qMR3.ZrA4yDL33Syhqd9UP7Zh7I58-1776965178-1.2.1.1-nB5AipaREd713eR_g_GonobNITXusb4LUspJyKBycO9IuAmXY3cV96AowwJ7q6R008MFqjjoor61V43T__6GS28hDElwMzmF2my5fk20.1.0C5JqVnGcyz_gTZagdh37btRKnUCXsf2BU4EllF20jBAT4q_GwK9Vt1HjXTyUu0eKjUncgSfEj9owjJmNjvTFi.tp..orcjWAEImoX0_FyzOpuflwSDZc97eKxageiHw7eko9tMRTy_xrbpvjjnEGw_3wH3PKHh7ESMeZsT_ZBNHxRu6Q45bRsC1.2wcR3tPUq2Kl2SLVxkwll8Aq0PMe0MzVj3zP989xkGbiDkkGlQ; logged-in-hint=6708c29182c39c903daaed3e; connect.sid=s%3AavOnSqj8edty3XL8scros56EJwnC4tcE.nJ5nvQT8MN9XeA4ZgOOUr5mDB%2BFt76VVHhzmXLcyyb4;'

# Unified list of all tasks provided
payloads = [
    {"answer": "soc", "questionNo": 1, "roomCode": "jrsecanalystintrouxo", "taskId": "60f99f4af22897005a54942b"},
    {"answer": "", "questionNo": 1, "roomCode": "jrsecanalystintrouxo", "taskId": "60facdc2554f2a005dd43d87"},
    {"answer": "", "questionNo": 1, "roomCode": "jrsecanalystintrouxo", "taskId": "60f7157d3a74ca00411ced4c"}, # Task 3
    {"answer": "221.181.185.159", "questionNo": 2, "roomCode": "jrsecanalystintrouxo", "taskId": "60f7157d3a74ca00411ced4c"}, # Task 4
    {"answer": "Will Griffin", "questionNo": 3, "roomCode": "jrsecanalystintrouxo", "taskId": "60f7157d3a74ca00411ced4c"}, # Task 5
    {"answer": "THM{until-we-meet-again}", "questionNo": 4, "roomCode": "jrsecanalystintrouxo", "taskId": "60f7157d3a74ca00411ced4c"} # Task 6
]

def get_cookie_dict(raw):
    return {c.split('=')[0].strip(): c.split('=')[1].strip() for c in raw.split(';') if '=' in c}

def solve_room():
    cookie_dict = get_cookie_dict(COOKIES_RAW)

    with requests.Session() as session:
        print(f"[*] Starting automation for room: {payloads[0]['roomCode']}\n" + "-"*40)

        for i, data in enumerate(payloads, 1):
            print(f"[*] Submitting Task {i} (Q# {data['questionNo']})...")

            try:
                response = session.post(URL, json=data, headers=HEADERS, cookies=cookie_dict)

                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get("status") == "success" and res_json["data"]["isCorrect"]:
                        print(f"[+] Correct! Score: {res_json['data']['totalPoints']}")
                        if res_json["data"].get("isRoomCompleted"):
                            print("[!!!] ROOM COMPLETED! [!!!]")
                    else:
                        print(f"[-] Failed: {res_json}")
                else:
                    print(f"[!] HTTP Error {response.status_code}: {response.text}")

            except Exception as e:
                print(f"[!] Request failed: {e}")

            # Rate limiting is key on THM
            time.sleep(2.5)

if __name__ == "__main__":
    solve_room()
