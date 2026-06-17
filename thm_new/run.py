from flask import Flask
import requests
import time
import os
import random

app = Flask(__name__)

# --- CONFIGURATION (Updated with your fresh headers/tokens) ---
ROOM_CODE = "jrsecanalystintrouxo"
# Updated CSRF Token from your new logs
CSRF_TOKEN = "nehsQcHD-L3RxVKA06q6iuygboXgJ-C2cInk"

# Target Endpoints
URL_INSIGHTS = "https://tryhackme.com/api/v2/client-insights"
URL_RESET = "https://tryhackme.com/api/v2/rooms/reset-progress"
URL_ANSWER = "https://tryhackme.com/api/v2/rooms/answer"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "csrf-token": CSRF_TOKEN,
    "Origin": "https://tryhackme.com",
    "Referer": f"https://tryhackme.com/room/{ROOM_CODE}",
    "X-Requested-With": "XMLHttpRequest"
}

# Updated Cookies from your new logs
COOKIES_RAW = 'thm-aid=cfda34c3-9d56-4d20-b7c9-31f3f5a1bc2c; cf_clearance=FXt_YMqlaT_gjDqmrtfMpP.BxDbfhl9yrAS9yI0uDBQ-1777135255-1.2.1.1-4jMwcuiLmmNGqpzElnR8Pccp3k9qKlHVHFGH54hQY9EOVITwAls3ezJycwSu_2i7uu9ummiIF6AhgrWwBPgX49t7u8U7gAncjccPSuyEauDGU_9SRIi5ss4srQ_1FP9sw5.swVfD1uHBaKS_wgAoBCpOPVqSI.NxpRfrFFudE7zhZNLLlFfK6ElbS5eEucKCdOMrfBr4sfTd7EjIPvTV4x2.LErQNgStVCMzCblDY28v4s7xX7fkWmZ5MW8yZg.e4hh0H0nyZ5cSBTg7dgZYGi4Zr24BnkrDR6k9KsNuILSHYL1szlEAA8SDbfZSY2ECkjNvIaxVXZt6xQC2AWLMrg; logged-in-hint=6708c29182c39c903daaed3e; connect.sid=s%3AavOnSqj8edty3XL8scros56EJwnC4tcE.nJ5nvQT8MN9XeA4ZgOOUr5mDB%2BFt76VVHhzmXLcyyb4; _csrf=abJu8CUR5P9joovruZofW6GH; cookie_consent_preferences={"essential":true,"analytics":false,"marketing":false}'

PAYLOADS = [
    {"answer": "soc", "questionNo": 1, "roomCode": ROOM_CODE, "taskId": "60f99f4af22897005a54942b"},
    {"answer": "", "questionNo": 1, "roomCode": ROOM_CODE, "taskId": "60facdc2554f2a005dd43d87"},
    {"answer": "", "questionNo": 1, "roomCode": ROOM_CODE, "taskId": "60f7157d3a74ca00411ced4c"},
    {"answer": "221.181.185.159", "questionNo": 2, "roomCode": ROOM_CODE, "taskId": "60f7157d3a74ca00411ced4c"},
    {"answer": "Will Griffin", "questionNo": 3, "roomCode": ROOM_CODE, "taskId": "60f7157d3a74ca00411ced4c"},
    {"answer": "THM{until-we-meet-again}", "questionNo": 4, "roomCode": ROOM_CODE, "taskId": "60f7157d3a74ca00411ced4c"}
]

def get_cookie_dict(raw):
    return {c.split('=')[0].strip(): c.split('=')[1].strip() for c in raw.split(';') if '=' in c}

@app.route("/")
def run_job():
    print("[*] Automation Triggered...")
    cookie_dict = get_cookie_dict(COOKIES_RAW)
    results = []

    with requests.Session() as session:
        session.cookies.update(cookie_dict)

        # 1. Reset Progress Step 1: Client Insights
        print("[*] Sending Reset Insight...")
        insight_payload = {
            "event": "reset-progress-clicked",
            "properties": {"room_code": ROOM_CODE, "answered_question": True, "completed_room": False}
        }
        session.post(URL_INSIGHTS, json=insight_payload, headers=HEADERS)
        time.sleep(3)

        # 2. Reset Progress Step 2: Clear Progress
        print("[*] Clearing Room Progress...")
        reset_payload = {"roomCode": ROOM_CODE}
        session.post(URL_RESET, json=reset_payload, headers=HEADERS)
        
        # Long cooldown after reset to reset server side rate counters
        print("[*] Progress Reset. Cooling down for 12s...")
        time.sleep(12)

        # 3. Main Task Loop
        for i, data in enumerate(PAYLOADS, 1):
            try:
                response = session.post(URL_ANSWER, json=data, headers=HEADERS, timeout=15)
                
                if response.status_code == 200:
                    status = "Success"
                elif response.status_code == 429:
                    status = "Rate Limited (429)"
                else:
                    status = f"Error {response.status_code}"
                
                print(f"[*] Task {i}: {status}")
                results.append(f"Task {i}: {status}")

            except Exception as e:
                results.append(f"Task {i}: Exception")

            # High jitter delay to ensure Task 4 bypasses the filter
            time.sleep(random.uniform(9.0, 14.0))

    return f"Full Automation Finished. Status: {', '.join(results)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
