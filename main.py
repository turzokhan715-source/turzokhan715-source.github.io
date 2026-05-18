import os
import re
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# ব্রাউজারের CORS সিকিউরিটি ইস্যু হ্যান্ডেল করার জন্য
CORS(app, resources={r"/*": {"origins": "*"}})


# 🎯 ফেসবুক লাইটের অফিশিয়াল মাইক্রোসফট অথেন্টিকেশন এবং ওটিপি রিডার মেথড
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
        # ১ম চেষ্টা: মডার্ন গ্রাফ এপিআই স্কোপ
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ২য় চেষ্টা: ওডব্লিউএ (OWA) স্কোপ
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)

        # ৩য় চেষ্টা: বেসিক এক্সচেঞ্জ
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


# 📋 আপনার নিজস্ব অরিজিনাল ইন্টারফেস (HTML)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Hotmail/Outlook Verification Code</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: rgb(240, 242, 245);
            padding: 40px 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .card {
            background: rgb(255, 255, 255);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgb(228, 230, 235);
        }
        
        .header-icon {
            font-size: 24px;
        }
        
        .header h1 {
            font-size: 18px;
            color: rgb(24, 119, 242);
            font-weight: 600;
        }
        
        .section-title {
            font-size: 14px;
            font-weight: 600;
            color: rgb(75, 79, 86);
            margin-bottom: 12px;
        }
        
        .input-box {
            width: 100%;
            padding: 12px;
            border: 2px solid rgb(228, 230, 235);
            border-radius: 8px;
            font-size: 12px;
            font-family: 'Courier New', monospace;
            background: rgb(248, 249, 250);
            resize: vertical;
            min-height: 100px;
            transition: all 0.3s;
        }
        
        .input-box:focus {
            outline: none;
            border-color: rgb(24, 119, 242);
            background: rgb(255, 255, 255);
        }
        
        .hint {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-top: 12px;
            padding: 10px;
            background: rgb(240, 242, 245);
            border-radius: 6px;
            font-size: 12px;
            color: rgb(101, 103, 107);
            line-height: 1.5;
        }
        
        .hint-icon {
            font-size: 14px;
            margin-top: 2px;
        }
        
        .email-display {
            margin-top: 20px;
            padding: 15px;
            background: rgb(248, 249, 250);
            border-radius: 8px;
            border: 1px solid rgb(228, 230, 235);
        }
        
        .email-label {
            font-size: 12px;
            font-weight: 600;
            color: rgb(75, 79, 86);
            margin-bottom: 8px;
        }
        
        .email-value {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }
        
        .email-text {
            font-size: 14px;
            color: rgb(33, 37, 41);
            font-weight: 600;
            word-break: break-all;
        }
        
        .email-text.placeholder {
            color: rgb(136, 136, 136);
            font-style: italic;
        }
        
        .btn-copy-small {
            padding: 8px 16px;
            background: rgb(24, 119, 242);
            color: rgb(255, 255, 255);
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.3s;
        }
        
        .btn-copy-small:hover {
            background: rgb(21, 101, 192);
        }
        
        .btn-copy-small:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .button-row {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .btn-primary {
            flex: 1;
            padding: 14px;
            background: rgb(24, 119, 242);
            color: rgb(255, 255, 255);
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary:hover:not(:disabled) {
            background: rgb(21, 101, 192);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .btn-clear {
            padding: 14px 24px;
            background: rgb(239, 68, 68);
            color: rgb(255, 255, 255);
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-clear:hover {
            background: rgb(220, 38, 38);
        }
        
        .result-header {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 15px;
            background: rgb(209, 250, 229);
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .result-header.error {
            background: rgb(254, 226, 226);
        }
        
        .result-header.waiting {
            background: rgb(243, 244, 246);
        }
        
        .result-icon {
            font-size: 20px;
            margin-top: 2px;
        }
        
        .result-content {
            flex: 1;
        }
        
        .result-title {
            font-size: 14px;
            font-weight: 700;
            color: rgb(6, 95, 70);
            margin-bottom: 6px;
        }
        
        .result-header.error .result-title {
            color: rgb(153, 27, 27);
        }
        
        .result-header.waiting .result-title {
            color: rgb(55, 65, 81);
        }
        
        .result-detail {
            font-size: 13px;
            color: rgb(4, 120, 87);
            margin: 4px 0;
        }
        
        .result-header.error .result-detail {
            color: rgb(185, 28, 28);
        }
        
        .result-header.waiting .result-detail {
            color: rgb(107, 114, 128);
        }
        
        .code-box {
            padding: 20px;
            border: 2px solid rgb(228, 230, 235);
            border-radius: 10px;
            background: rgb(255, 255, 255);
        }
        
        .code-label {
            font-size: 12px;
            font-weight: 600;
            color: rgb(75, 79, 86);
            margin-bottom: 12px;
        }
        
        .code-display {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
        }
        
        .code-value {
            font-size: 32px;
            font-weight: 900;
            color: rgb(16, 185, 129);
            letter-spacing: 6px;
            font-family: 'Courier New', monospace;
            user-select: all;
        }
        
        .code-value.placeholder {
            color: rgb(156, 163, 175);
        }
        
        .btn-copy-large {
            padding: 10px 20px;
            background: rgb(16, 185, 129);
            color: rgb(255, 255, 255);
            border: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.3s;
        }
        
        .btn-copy-large:hover:not(:disabled) {
            background: rgb(5, 150, 105);
        }
        
        .btn-copy-large:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .how-to-use {
            padding: 15px;
            background: rgb(243, 244, 246);
            border-radius: 8px;
            border-left: 4px solid rgb(156, 163, 175);
        }
        
        .how-to-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            font-weight: 700;
            color: rgb(55, 65, 81);
            margin-bottom: 10px;
        }
        
        .how-to-content {
            font-size: 13px;
            color: rgb(75, 85, 99);
            line-height: 1.6;
        }
        
        .how-to-content ol {
            margin-left: 20px;
            margin-top: 8px;
        }
        
        .how-to-content li {
            margin: 6px 0;
        }
        
        .loader {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: rgb(255, 255, 255);
            animation: spin 0.8s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <span class="header-icon">📧</span>
                <h1>Get Hotmail/Outlook Verification Code</h1>
            </div>

            <div class="section-title">Account Details</div>
            
            <textarea 
                class="input-box" 
                id="accountInput" 
                placeholder="email@outlook.com|password|refresh_token|client_id"></textarea>

            <div class="hint">
                <span class="hint-icon">ℹ️</span>
                <div>
                    <strong>Format:</strong> email|password|refresh_token|client_id<br>
                    <strong>Supports:</strong> @hotmail.com, @outlook.com, @live.com addresses
                </div>
            </div>

            <div class="email-display">
                <div class="email-label">Extracted Email:</div>
                <div class="email-value">
                    <span class="email-text placeholder" id="extractedEmail">No email entered yet</span>
                    <button class="btn-copy-small" id="copyEmailBtn" onclick="copyEmail()" disabled>📋 Copy Email</button>
                </div>
            </div>

            <div class="button-row">
                <button class="btn-primary" id="getCodeBtn" onclick="getVerificationCode()">
                    Get Verification Code
                </button>
                <button class="btn-clear" onclick="clearAll()">
                    🗑️ Clear
                </button>
            </div>
        </div>

        <div class="card">
            <div class="result-header waiting" id="resultHeader">
                <span class="result-icon" id="resultIcon">⏳</span>
                <div class="result-content">
                    <div class="result-title" id="resultTitle">Waiting for request...</div>
                    <div class="result-detail" id="resultDetail">Enter your account details and click "Get Verification Code"</div>
                </div>
            </div>

            <div class="code-box">
                <div class="code-label">Verification Code:</div>
                <div class="code-display">
                    <div class="code-value placeholder" id="codeValue">------</div>
                    <button class="btn-copy-large" id="copyCodeBtn" onclick="copyCode()" disabled>📋 Copy Code</button>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="how-to-use">
                <div class="how-to-title">
                    <span>ℹ️</span>
                    <span>How to Use</span>
                </div>
                <div class="how-to-content">
                    <ol>
                        <li>Enter your account details in the format: <code>email|password|token|client_id</code></li>
                        <li>Click "Get Verification Code" button</li>
                        <li>Wait for the system to fetch your latest verification email</li>
                        <li>The code will be automatically extracted and displayed</li>
                        <li>Click "Copy Code" to copy it to clipboard</li>
                        <li>Use "Clear" button to reset and start over</li>
                    </ol>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Input পরিবর্তনের সাথে সাথে ইমেইল ডিটেক্ট করার লজিক
        document.getElementById('accountInput').addEventListener('input', function() {
            const input = this.value.trim();
            const emailText = document.getElementById('extractedEmail');
            const copyEmailBtn = document.getElementById('copyEmailBtn');
            
            if (input) {
                const email = input.split('|')[0].trim();
                if (email && email.includes('@')) {
                    emailText.textContent = email;
                    emailText.classList.remove('placeholder');
                    copyEmailBtn.disabled = false;
                } else {
                    emailText.textContent = 'Invalid email format';
                    emailText.classList.add('placeholder');
                    copyEmailBtn.disabled = true;
                }
            } else {
                emailText.textContent = 'No email entered yet';
                emailText.classList.add('placeholder');
                copyEmailBtn.disabled = true;
            }
        });

        async function getVerificationCode() {
            const input = document.getElementById('accountInput').value.trim();
            
            if (!input) {
                alert('⚠️ Please enter account details!');
                return;
            }

            const parts = input.split('|');
            if (parts.length < 3) {
                alert('⚠️ Invalid format! Use: email|password|token|client_id');
                return;
            }

            const email = parts[0] ? parts[0].trim() : '';
            const password = parts[1] ? parts[1].trim() : '';
            const token = parts[2] ? parts[2].trim() : '';
            const clientId = parts[3] ? parts[3].trim() : '';

            const btn = document.getElementById('getCodeBtn');
            const resultHeader = document.getElementById('resultHeader');
            const resultIcon = document.getElementById('resultIcon');
            const resultTitle = document.getElementById('resultTitle');
            const resultDetail = document.getElementById('resultDetail');
            const codeValue = document.getElementById('codeValue');
            const copyCodeBtn = document.getElementById('copyCodeBtn');
            
            btn.disabled = true;
            btn.innerHTML = '<span class="loader"></span> Fetching verification code...';

            try {
                // পাইথন এন্ডপয়েন্ট এপিআই কল করা হচ্ছে
                const response = await fetch('/api/get-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, token, clientId })
                });

                const data = await response.json();

                if (data.success) {
                    resultHeader.classList.remove('error', 'waiting');
                    resultIcon.textContent = '✅';
                    resultTitle.textContent = 'Email Retrieved Successfully';
                    resultDetail.textContent = `For: ${data.email}`;
                    codeValue.textContent = data.code;
                    codeValue.classList.remove('placeholder');
                    copyCodeBtn.disabled = false;

                    // অটো ক্লিপবোর্ড কপি অপশন
                    try {
                        await navigator.clipboard.writeText(data.code);
                        console.log('✅ Code auto-copied');
                    } catch(e) {}
                } else {
                    resultHeader.classList.add('error');
                    resultHeader.classList.remove('waiting');
                    resultIcon.textContent = '❌';
                    resultTitle.textContent = 'Error';
                    resultDetail.textContent = data.error;
                    codeValue.textContent = '------';
                    codeValue.classList.add('placeholder');
                    copyCodeBtn.disabled = true;
                }

            } catch (error) {
                resultHeader.classList.add('error');
                resultHeader.classList.remove('waiting');
                resultIcon.textContent = '❌';
                resultTitle.textContent = 'Network Error';
                resultDetail.textContent = error.message;
                codeValue.textContent = '------';
                codeValue.classList.add('placeholder');
                copyCodeBtn.disabled = true;
            }

            btn.disabled = false;
            btn.innerHTML = 'Get Verification Code';
        }

        function clearAll() {
            document.getElementById('accountInput').value = '';
            const emailText = document.getElementById('extractedEmail');
            emailText.textContent = 'No email entered yet';
            emailText.classList.add('placeholder');
            document.getElementById('copyEmailBtn').disabled = true;
            
            const resultHeader = document.getElementById('resultHeader');
            resultHeader.classList.remove('error');
            resultHeader.classList.add('waiting');
            document.getElementById('resultIcon').textContent = '⏳';
            document.getElementById('resultTitle').textContent = 'Waiting for request...';
            document.getElementById('resultDetail').textContent = 'Enter your account details and click "Get Verification Code"';
            
            const codeValue = document.getElementById('codeValue');
            codeValue.textContent = '------';
            codeValue.classList.add('placeholder');
            document.getElementById('copyCodeBtn').disabled = true;
        }

        async function copyCode() {
            const code = document.getElementById('codeValue').textContent;
            if (code === '------') return;
            
            try {
                await navigator.clipboard.writeText(code);
                alert('✅ Code copied: ' + code);
            } catch(e) {
                alert('⚠️ Failed to copy');
            }
        }

        async function copyEmail() {
            const email = document.getElementById('extractedEmail').textContent;
            if (email === 'No email entered yet' || email === 'Invalid email format') return;
            
            try {
                await navigator.clipboard.writeText(email);
                alert('✅ Email copied: ' + email);
            } catch(e) {
                alert('⚠️ Failed to copy');
            }
        }
    </script>
</body>
</html>"""


# রুট ডোমেইনে আপনার অরিজিনাল ইন্টারফেস রেন্ডার করার ফাংশন
@app.route('/', methods=['GET', 'HEAD'])
def home():
    return render_template_string(HTML_TEMPLATE)


# আপনার জাভাস্ক্রিপ্ট রিকোয়েস্টের সাথে সামঞ্জস্যপূর্ণ API এন্ডপয়েন্ট
@app.route('/api/get-code', methods=['POST'])
def get_code():
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        refresh_token = data.get('token', '').strip()  # JS থেকে 'token' হিসেবে আসছে
        client_id = data.get('clientId', '').strip()    # JS থেকে 'clientId' হিসেবে আসছে

        if not email or not refresh_token or not client_id:
            return jsonify({
                'success': False, 
                'error': 'Missing email, refresh_token, or client_id from input.'
            })

        # মাইক্রোসফট এপিআই এর মাধ্যমে ওটিপি রিড করা হচ্ছে
        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        # প্রাপ্ত রেজাল্ট যদি ডিজিট (সংখ্যা) হয় তাহলে সাকসেস রেসপন্স পাঠানো হচ্ছে
        if fb_code.isdigit():
            return jsonify({
                'success': True, 
                'email': email, 
                'code': fb_code
            })
        else:
            return jsonify({
                'success': False, 
                'error': fb_code
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
