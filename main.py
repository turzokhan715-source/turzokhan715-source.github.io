import os
import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 🌐 ব্রাউজার এবং রেন্ডার ক্লাউডের CORS পলিসি শতভাগ পাস করার সিকিউরিটি লেয়ার
CORS(app, resources={r"/*": {"origins": "*"}})

# 🎯 মাইক্রোসফট কোর ওটিপি এক্সট্রাকশন ইঞ্জিন
def extract_fb_code_via_api(email, refresh_token, client_id):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json"
    }
    payload = {
        "client_id": client_id,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/User.Read offline_access"
    }

    try:
        # ১ম ট্রাই: Graph Scope
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        
        # ২য় ট্রাই: Outlook Scope
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ৩য় ট্রাই: Fallback
        if res.status_code != 200:
            payload.pop("scope", None)
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        if res.status_code != 200:
            return f"Endpoint rejected token. Status: {res.status_code}"

        try:
            res_data = res.json()
        except Exception:
            return f"Invalid server response format. Status: {res.status_code}"

        access_token = res_data.get("access_token")
        if not access_token:
            return "Access Token missing in response."

        # ফেসবুক মেইল সার্চিং ব্লক
        messages_url = "https://graph.microsoft.com/v1.0/me/messages?$search=\"Facebook\"&$top=1"
        api_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
        }

        msg_res = requests.get(messages_url, headers=api_headers, timeout=15)
        if msg_res.status_code != 200:
            messages_url = "https://outlook.office.com/api/v2.0/me/messages?$search=\"Facebook\"&$top=1"
            msg_res = requests.get(messages_url, headers=api_headers, timeout=15)

        if msg_res.status_code != 200:
            return f"Connected, but failed to fetch inbox (Status: {msg_res.status_code})."

        try:
            msg_data = msg_res.json()
        except Exception:
            return f"Failed to parse inbox data. Status: {msg_res.status_code}"

        messages = msg_data.get("value", [])
        if not messages:
            return "No recent Facebook emails found."

        latest_message = messages[0]
        body_content = latest_message.get("body", {}).get("content", "") or latest_message.get("Body", {}).get("Content", "")
        subject = latest_message.get("subject", "") or latest_message.get("Subject", "")

        combined_text = f"{subject} {body_content}"
        code_match = re.search(r'\b(\d{5,6})\b', combined_text)

        if code_match:
            return code_match.group(1)
        else:
            return "Facebook email found, but couldn't parse code digits."

    except Exception as e:
        return f"System Connection Error: {str(e)}"

# 🔍 ইমেইল এক্সট্রাক্টর ফিল্টার
def extract_email_from_string(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    return match.group(0).strip() if match else None

# 🔮 মেইন এপিআই রাউট
@app.route('/get-code', methods=['POST', 'OPTIONS'])
def get_code():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'CORS_Preflight_OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        # ফ্রন্টএন্ড থেকে যেভাবে বা যে কি-তেই ডেটা আসুক, রিসিভ করার ব্যাকআপ লেয়ার
        data = request.get_json() or request.form or {}
        raw_input = data.get('raw_input', '')
        
        # যদি অন্য কোনো নামের কি (Key) ব্যবহার করা হয়ে থাকে ফ্রন্টএন্ডে
        if not raw_input and data:
            raw_input = list(data.values())[0] if isinstance(data, dict) and data.values() else ''
            
        raw_input = str(raw_input).strip()

        if not raw_input:
            response = jsonify({'status': 'error', 'message': 'Input is empty or null.'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200

        detected_email = extract_email_from_string(raw_input)
        
        # পাইপ (|) স্প্লিট মেথড
        parts = [p.strip() for p in raw_input.split('|') if p.strip()]
        
        if len(parts) < 3:
            response = jsonify({'status': 'error', 'message': 'Format incorrect. Must contain email|pass|token'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200

        email = detected_email if detected_email else parts[0]
        password = parts[1]
        refresh_token = parts[2]
        
        if len(parts) >= 4:
            client_id = parts[3]
        else:
            client_id = "f1e6c35b-1634-4bc0-b53d-24e526d140e6"

        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        if fb_code.isdigit():
            response = jsonify({'status': 'success', 'email': email, 'code': fb_code})
        else:
            response = jsonify({'status': 'error', 'message': fb_code})
            
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except Exception as e:
        response = jsonify({'status': 'error', 'message': f"Server Exception Safety Layer: {str(e)}"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

@app.route('/')
def home():
    return "OTP Extractor API is Running Live!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
