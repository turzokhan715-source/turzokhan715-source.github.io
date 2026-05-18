import os
import re
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# 🌐 Browser block validation layer config ruleset
CORS(app, resources={r"/*": {"origins": "*"}})

# 🎯 Facebook Lite Endpoint Logic Core API
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
        # ১ম চেষ্টা: Graph API Scope
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ২য় চেষ্টা: OWA Outlook Scope
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ৩য় চেষ্টা: Basic auth fallback
        if res.status_code != 200:
            payload.pop("scope", None)
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        if res.status_code != 200:
            return f"Endpoint rejected token. Status: {res.status_code}"

        res_data = res.json()
        access_token = res_data.get("access_token")
        if not access_token:
            return "Access Token missing in token response."

        # Facebook email parsing structure layers
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

        messages = msg_res.json().get("value", [])
        if not messages:
            return "No recent Facebook emails found in this inbox."

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

# 🔍 Email Regex Filter Extractor
def extract_email_from_string(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    return match.group(0).strip() if match else None

# 🔮 Flask Web Route with explicit manual OPTIONS and Header responses for Render Cloud
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

        parts = raw_input.split('|')
        if len(parts) < 4:
            response = jsonify({'status': 'error', 'message': 'Format must be email|pass|token|client_id'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        email = detected_email
        password = parts[1].strip()
        refresh_token = parts[2].strip()
        client_id = parts[3].strip()

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
    return "OTP Extractor API is Running Live!"

if __name__ == '__main__':
    # Cloud environments dynamic port assignments fallback
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
