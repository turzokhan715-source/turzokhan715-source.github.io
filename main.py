import os
import re
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# 🌐 ব্রাউজার ব্লকিং এবং ক্রস-অরিজিন (CORS) পলিসি শতভাগ পাস করার জন্য লেয়ার
CORS(app, resources={r"/*": {"origins": "*"}})

# 🎯 ফেসবুক লাইটের অফিশিয়াল মাইক্রোসফট অথেন্টিকেশন মেথড কোর ইঞ্জিন
def extract_fb_code_via_api(email, refresh_token, client_id):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    # মোবাইল অ্যাপের মতো নিখুঁত হেডার (যাতে মাইক্রোসফট ব্লক বা রিজেক্ট না করে)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json"
    }

    # ব্যাকআপ এবং মেইন সব ধরনের স্কোপ একসাথে লিস্ট করা হলো
    payload = {
        "client_id": client_id,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/User.Read offline_access"
    }

    try:
        # ১ম চেষ্টা: মডার্ন গ্রাফ এপিআই স্কোপ
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ২য় চেষ্টা: যদি প্রথমবার রিজেক্ট হয়, তবে ডাইরেক্ট ওডব্লিউএ (OWA) স্কোপ ট্রাই করবে
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ৩য় চেষ্টা: কোনো স্কোপ ছাড়া একদম বেসিক এক্সচেঞ্জ (যা কিছু প্যানেল ডিফল্ট করে)
        if res.status_code != 200:
            payload.pop("scope", None)
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        if res.status_code != 200:
            return f"Endpoint rejected token. Status: {res.status_code}"

        res_data = res.json()
        access_token = res_data.get("access_token")
        if not access_token:
            return "Access Token missing in token response."

        # ফেসবুক মেইল স্ক্র্যাপ করার জন্য ২ স্তরের এন্ডপয়েন্ট সার্চার
        messages_url = "https://graph.microsoft.com/v1.0/me/messages?$search=\"Facebook\"&$top=1"
        api_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
        }

        msg_res = requests.get(messages_url, headers=api_headers, timeout=15)

        # গ্রাফ এপিআই ফেইল করলে ওডব্লিউএ আউটলুক এপিআই কল করবে
        if msg_res.status_code != 200:
            messages_url = "https://outlook.office.com/api/v2.0/me/messages?$search=\"Facebook\"&$top=1"
            msg_res = requests.get(messages_url, headers=api_headers, timeout=15)

        if msg_res.status_code != 200:
            return f"Connected, but failed to fetch inbox (Status: {msg_res.status_code})."

        messages = msg_res.json().get("value", [])
        if not messages:
            return "No recent Facebook emails found in this inbox."

        latest_message = messages[0]
        body_content = latest_message.get("body", {}).get("content", "") or latest_message.get("Body", {}).get("Content", "")
        subject = latest_message.get("subject", "") or latest_message.get("Subject", "")

        combined_text = f"{subject} {body_content}"
        # বডি থেকে ফেসবুক সিকিউরিটি কোড (৫ বা ৬ ডিজিট) রিড করা
        code_match = re.search(r'\b(\d{5,6})\b', combined_text)

        if code_match:
            return code_match.group(1)
        else:
            return "Facebook email found, but couldn't parse code digits."

    except Exception as e:
        return f"System Connection Error: {str(e)}"

# 🔍 ইমেইল এক্সট্রাকশন ফিল্টার (যা ইনপুট স্ট্রিং থেকে নিখুঁত ইমেইল বের করে)
def extract_email_from_string(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    return match.group(0).strip() if match else None

# 🔮 রেন্ডার ক্লাউডের জন্য ম্যানুয়াল OPTIONS এবং রেসপন্স হেডারসহ মেইন এপিআই রুট
@app.route('/get-code', methods=['POST', 'OPTIONS'])
def get_code():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'CORS_Preflight_OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        data = request.get_json() or {}
        raw_input = data.get('raw_input', '').strip()

        if not raw_input:
            response = jsonify({'status': 'error', 'message': 'Input empty.'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        detected_email = extract_email_from_string(raw_input)
        if not detected_email:
            response = jsonify({'status': 'error', 'message': 'No valid email found in data.'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        # পাইপ (|) দিয়ে ডেটা আলাদা করা হচ্ছে এবং প্রতিটা পার্টের এক্সট্রা স্পেস ক্লিয়ার করা হচ্ছে
        parts = [p.strip() for p in raw_input.split('|') if p.strip()]
        
        # আপনার ১০০/১০০ কাজের মেথডের লজিক অনুসারে কমপক্ষে ৩টি পার্ট থাকতে হবে
        if len(parts) < 3:
            response = jsonify({'status': 'error', 'message': 'Format must be email|pass|token'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        email = detected_email
        password = parts[1]
        refresh_token = parts[2]
        
        # বুদ্ধিমান ফলব্যাক: ইনপুটে ৪ নম্বর পার্ট (client_id) না থাকলে এই ডিফল্ট আইডিটি নিজে থেকে বসে যাবে
        if len(parts) >= 4:
            client_id = parts[3]
        else:
            client_id = "f1e6c35b-1634-4bc0-b53d-24e526d140e6"

        # আপনার নিখুঁত ফেসবুক লাইট ইঞ্জিনে ডেটা পাঠানো হচ্ছে
        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        if fb_code.isdigit():
            response = jsonify({
                'status': 'success', 
                'email': email, 
                'code': fb_code
            })
        else:
            response = jsonify({
                'status': 'error', 
                'message': fb_code
            })
            
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except Exception as e:
        response = jsonify({'status': 'error', 'message': f"Server error: {str(e)}"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

@app.route('/')
def home():
    return "OTP Extractor API is Running Live and Synced with Web Design!"

if __name__ == '__main__':
    # রেন্ডার সার্ভারের ডায়নামিক পোর্ট অ্যাসাইনমেন্ট লজিক
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
