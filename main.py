import os
import re
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# 🌐 ব্রাউজার ব্লকিং এবং ক্রস-অরিজিন (CORS) পলিসি শতভাগ পাস করার জন্য সিকিউরিটি লেয়ার
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

# 🔮 আপনার প্যানেলের আসল ফ্রন্টএন্ড ডিজাইন ইন্টারফেস (HTML/CSS/JS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Longisir VIP Portal - Free Tools</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;600;800&display=swap');

:root {
--primary: rgb(168, 85, 247);
--bg: rgb(10, 11, 18);
--card-bg: rgb(21, 23, 37);
--text-gray: rgb(156, 163, 175);
--btn-grad: linear-gradient(135deg, rgb(168, 85, 247), rgb(139, 92, 246));
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }

body {
background: var(--bg);
color: rgb(255, 255, 255);
min-height: 100vh;
display: flex;
flex-direction: column;
}

.section {
width: 100%;
max-width: 600px;
margin: 40px auto;
padding: 20px;
}

.card {
background: var(--card-bg);
border: 1px solid rgba(255, 255, 255, 0.05);
border-radius: 16px;
padding: 24px;
box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

h2 { font-size: 24px; font-weight: 800; margin-bottom: 8px; background: linear-gradient(to right, #fff, var(--text-gray)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { color: var(--text-gray); font-size: 14px; margin-bottom: 24px; }

.input-group { margin-bottom: 20px; }
.input-group label { display: block; font-size: 13px; font-weight: 600; color: var(--text-gray); margin-bottom: 8px; text-transform: uppercase; tracking-style: 1px; }

textarea {
width: 100%; height: 120px; background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; color: #fff; font-size: 14px; font-family: monospace; resize: none; transition: all 0.3s;
}
textarea:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15); }

.target-display { background: rgba(168, 85, 247, 0.06); border: 1px dashed rgba(168, 85, 247, 0.3); border-radius: 10px; padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 13px; }
.target-display span { font-weight: 600; color: var(--primary); }

.btn {
width: 100%; background: var(--btn-grad); border: none; border-radius: 12px; padding: 14px; color: #fff; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
}
.btn:hover { opacity: 0.95; transform: translateY(-1px); }
.btn:disabled { background: #374151; cursor: not-allowed; box-shadow: none; transform: none; }

.result-box { margin-top: 24px; padding: 16px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; display: none; }
.result-header { display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: 600; color: var(--text-gray); margin-bottom: 12px; }
.status-badge { padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; }
.status-processing { background: rgba(234, 179, 8, 0.15); color: rgb(234, 179, 8); }
.status-success { background: rgba(34, 197, 94, 0.15); color: rgb(34, 197, 94); }
.status-failed { background: rgba(239, 68, 68, 0.15); color: rgb(239, 68, 68); }

.otp-container { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; }
.otp-code { font-size: 28px; font-weight: 800; letter-spacing: 2px; font-family: monospace; color: rgb(34, 197, 94); }
.otp-error { font-size: 13px; color: rgb(239, 68, 68); font-family: sans-serif; }
.copy-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer; transition: 0.2s; }
.copy-btn:hover { background: rgba(255,255,255,0.1); }
</style>
</head>
<body>

<div class="section">
    <div class="card">
        <h2>Facebook Code Retriever</h2>
        <p class="subtitle">Enter Microsoft Refresh Token data line below to extract secure live verification codes.</p>
        
        <div class="input-group">
            <label>Account Data Line</label>
            <textarea id="rawData" placeholder="email|password|refresh_token|client_id"></textarea>
        </div>

        <div class="target-display">
            <div>Target Email: <span id="targetEmail">Waiting for data...</span></div>
        </div>

        <button onclick="getCode()" id="actionBtn" class="btn">Get Facebook Code</button>

        <div id="resultBox" class="result-box">
            <div class="result-header">
                <span>STATUS:</span>
                <span id="statusLabel" class="status-badge"></span>
            </div>
            <div class="otp-container">
                <div id="otpOutput" class="otp-code">XXXXXX</div>
                <button onclick="copyCode()" class="copy-btn">Copy</button>
            </div>
        </div>
    </div>
</div>

<script>
document.getElementById('rawData').addEventListener('input', function(e) {
    const val = e.target.value.trim();
    if(val.includes('|')) {
        document.getElementById('targetEmail').innerText = val.split('|')[0];
    } else {
        document.getElementById('targetEmail').innerText = "Waiting for data...";
    }
});

async function getCode() {
    const rawInput = document.getElementById('rawData').value.trim();
    const actionBtn = document.getElementById('actionBtn');
    const resultBox = document.getElementById('resultBox');
    const statusLabel = document.getElementById('statusLabel');
    const otpOutput = document.getElementById('otpOutput');

    if(!rawInput) return;

    actionBtn.disabled = true;
    actionBtn.innerText = 'Exchanging Mobile Session Token...';
    resultBox.style.display = 'block';
    statusLabel.className = "status-badge status-processing";
    statusLabel.innerText = "PROCESSING";
    otpOutput.innerHTML = '<span class="otp-code" style="color:var(--text-gray)">XXXXXX</span>';

    try {
        const response = await fetch('/get-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ raw_input: rawInput })
        });
        const data = await response.json();

        actionBtn.disabled = false;
        actionBtn.innerText = 'Get Facebook Code';

        if(data.status === 'success') {
            statusLabel.className = "status-badge status-success";
            statusLabel.innerText = "SUCCESS";
            otpOutput.innerHTML = `<span class="otp-code">${data.code}</span>`;
        } else {
            statusLabel.className = "status-badge status-failed";
            statusLabel.innerText = "FAILED";
            otpOutput.innerHTML = `<span class="otp-error">${data.message}</span>`;
        }
    } catch (err) {
        actionBtn.disabled = false;
        actionBtn.innerText = 'Get Facebook Code';
        statusLabel.className = "status-badge status-failed";
        statusLabel.innerText = "ERROR";
        otpOutput.innerHTML = '<span class="otp-error">Connection Error.</span>';
    }
}

function copyCode() {
    const otpText = document.getElementById('otpOutput').innerText;
    if(otpText && otpText !== 'XXXXXX' && !otpText.includes('rejected') && !otpText.includes('Error')) {
        navigator.clipboard.writeText(otpText);
        alert('Copied successfully!');
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

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

        # পাইপ (|) দিয়ে ডেটা নিখুঁতভাবে আলাদা করা হচ্ছে
        parts = [p.strip() for p in raw_input.split('|') if p.strip()]
        
        if len(parts) < 3:
            response = jsonify({'status': 'error', 'message': 'Format must be email|pass|token'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400

        email = detected_email
        password = parts[1]
        refresh_token = parts[2]
        
        # ৪ নম্বর অংশ (client_id) না থাকলে এই স্ট্যান্ডার্ড আইডিটি নিজে থেকে বসে যাবে
        if len(parts) >= 4:
            client_id = parts[3]
        else:
            client_id = "f1e6c35b-1634-4bc0-b53d-24e526d140e6"

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

if __name__ == '__main__':
    # ক্লাউড এনভায়রনমেন্টের জন্য পোর্ট ম্যানেজমেন্ট লজিক
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
