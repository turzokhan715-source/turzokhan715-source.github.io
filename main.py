import re
from flask import Flask, request, jsonify, render_template_string
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def extract_fb_code_via_api(email, refresh_token, client_id, mode='fb'):
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
        res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        if res.status_code != 200:
            payload["scope"] = "https://outlook.office.com/IMAP.AccessAsUser.All offline_access"
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        if res.status_code != 200:
            payload.pop("scope", None)
            res = requests.post(token_url, headers=headers, data=payload, timeout=15)
        if res.status_code != 200:
            return f"Endpoint rejected token. Server Response: {res.text[:100]}"

        res_data = res.json()
        access_token = res_data.get("access_token")
        if not access_token:
            return "Access Token missing in token response."

        search_keyword = "Instagram" if mode == "ig" else "Facebook"
        messages_url = "https://graph.microsoft.com/v1.0/me/messages?$search=\"" + search_keyword + "\"&$top=1"
        
        api_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
        }

        msg_res = requests.get(messages_url, headers=api_headers, timeout=15)
        if msg_res.status_code != 200:
            messages_url = "https://outlook.office.com/api/v2.0/me/messages?$search=\"" + search_keyword + "\"&$top=1"
            msg_res = requests.get(messages_url, headers=api_headers, timeout=15)

        if msg_res.status_code != 200:
            return f"Connected, but failed to fetch inbox (Status: {msg_res.status_code})."

        messages = msg_res.json().get("value", [])
        if not messages:
            return f"No recent {search_keyword} emails found in this inbox."

        latest_message = messages[0]
        body_content = latest_message.get("body", {}).get("content", "") or latest_message.get("Body", {}).get("Content", "")
        subject = latest_message.get("subject", "") or latest_message.get("Subject", "")

        combined_text = f"{subject} {body_content}"
        code_match = re.search(r'\b(\d{5,6})\b', combined_text)

        if code_match:
            return code_match.group(1)
        else:
            return f"{search_keyword} email found, but couldn't parse the numeric code digits."
    except Exception as e:
        return f"System Connection Error: {str(e)}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB & IG OTP Extractor - Full Wide Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .neon-card {
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(51, 65, 85, 0.5);
            box-shadow: 0 25px 70px -10px rgba(0, 0, 0, 0.8), 0 0 40px rgba(99, 102, 241, 0.08);
            border-radius: 24px;
        }
        .neon-bracket {
            border-left: 3px solid #6366f1;
            border-right: 3px solid #6366f1;
            border-radius: 12px;
        }
        textarea::-webkit-scrollbar {
            width: 6px;
        }
        textarea::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
        }
        textarea::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 10px;
        }
    </style>
</head>
<body class="bg-[#030712] text-slate-200 min-h-screen flex flex-col justify-center items-center p-4 md:p-10 font-sans select-none">

    <div class="w-full max-w-7xl neon-card p-6 md:p-10 transition-all duration-300">
        
        <div class="flex flex-col items-center mb-8 border-b border-slate-800 pb-6">
            <div class="flex items-center space-x-3 text-2xl md:text-4xl font-black tracking-tight">
                <i class="fas fa-cube text-indigo-500 animate-pulse"></i>
                <h1 class="bg-gradient-to-r from-white via-slate-200 to-indigo-400 bg-clip-text text-transparent">FB & IG OTP Extractor</h1>
            </div>
            <p class="text-[10px] md:text-xs text-indigo-400/70 font-bold uppercase tracking-widest mt-1.5">Cloud Automation Hub</p>
            
            <div id="modeBadge" class="mt-3 inline-flex items-center space-x-1.5 bg-amber-500/10 border border-amber-500/30 px-6 py-1 rounded-full shadow-sm">
                <i class="fas fa-shield-alt text-amber-400 text-[10px]"></i>
                <span id="badgeText" class="text-[10px] font-black text-amber-400 tracking-wider uppercase">Facebook Priority Mode</span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
            
            <div class="flex flex-col justify-between space-y-6">
                <div class="space-y-5">
                    <div class="bg-slate-950 p-2 rounded-2xl flex space-x-2 border border-slate-800/80">
                        <button onclick="setPlatform('fb')" id="fbBtn" class="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-xs md:text-sm font-black py-3.5 px-4 rounded-xl flex justify-center items-center transition-all duration-300 shadow-lg cursor-pointer">
                            <i class="fab fa-facebook mr-2 text-sm"></i> Facebook
                            <span class="ml-1.5 bg-amber-400 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded-md">1st</span>
                        </button>
                        <button onclick="setPlatform('ig')" id="igBtn" class="flex-1 bg-transparent text-slate-500 hover:text-slate-300 text-xs md:text-sm font-bold py-3.5 px-4 rounded-xl flex justify-center items-center transition-all duration-300 cursor-pointer">
                            <i class="fab fa-instagram mr-2 text-sm"></i> Instagram
                            <span class="ml-1.5 bg-slate-800 text-slate-400 text-[10px] font-bold px-1.5 py-0.5 rounded-md">2nd</span>
                        </button>
                    </div>

                    <div class="flex space-x-3">
                        <button onclick="loadAccount(1)" class="flex-1 bg-slate-900/60 hover:bg-slate-800/80 text-slate-400 hover:text-white text-xs font-bold py-3 px-4 rounded-xl border border-slate-800 transition cursor-pointer flex justify-center items-center shadow-xs">
                            <i class="fas fa-user-shield mr-2 text-blue-400"></i> Account 1
                        </button>
                        <button onclick="loadAccount(2)" class="flex-1 bg-slate-900/60 hover:bg-slate-800/80 text-slate-400 hover:text-white text-xs font-bold py-3 px-4 rounded-xl border border-slate-800 transition cursor-pointer flex justify-center items-center shadow-xs">
                            <i class="fas fa-user-shield mr-2 text-purple-400"></i> Account 2
                        </button>
                    </div>

                    <div id="inputBracket" class="relative px-4 neon-bracket">
                        <label class="block text-[11px] md:text-xs font-black text-indigo-300 tracking-wider mb-2 uppercase flex items-center">
                            <i class="fas fa-terminal mr-2 text-indigo-400"></i> Input Account Data Line:
                        </label>
                        <textarea 
                            id="rawData" 
                            class="w-full h-36 bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-xs font-mono text-cyan-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-inner transition resize-none"
                            placeholder="email|password|refresh_token|client_id"
                        ></textarea>
                    </div>
                </div>

                <div class="flex space-x-3 pt-2">
                    <button onclick="getOtpCode()" id="actionBtn" class="flex-[3] bg-slate-900 hover:bg-slate-800 text-slate-300 font-black py-4 px-5 rounded-xl border border-slate-800 transition-all duration-200 flex justify-center items-center cursor-pointer text-xs md:text-sm tracking-wider uppercase shadow-md">
                        <span id="btnText"><i class="fas fa-bolt mr-2 text-indigo-400"></i> Extract OTP Code</span>
                    </button>
                    <button onclick="clearAll()" class="flex-1 bg-slate-900/40 hover:bg-slate-900 text-slate-500 hover:text-red-400 font-bold py-4 px-4 rounded-xl border border-slate-800/60 transition flex justify-center items-center cursor-pointer text-xs uppercase">
                        <i class="fas fa-eraser mr-1.5"></i> Clear
                    </button>
                </div>
            </div>

            <div class="flex flex-col justify-between space-y-6 lg:space-y-0 lg:pl-6 border-t lg:border-t-0 lg:border-l border-slate-800/60 pt-6 lg:pt-0">
                
                <div id="detectInfo" class="px-5 border-l-4 border-r-4 border-indigo-500 flex justify-between items-center bg-slate-950/60 py-5 rounded-xl border border-slate-800/50 shadow-xs min-h-[110px]">
                    <div class="max-w-[70%]">
                        <div class="flex items-center text-xs md:text-sm font-black text-indigo-300 tracking-wide">
                            <i id="statusDot" class="fas fa-circle-notch text-indigo-400 mr-2 text-xs"></i>
                            <span id="successMsg">System Standing By</span>
                        </div>
                        <div class="text-[11px] md:text-xs text-slate-500 mt-2.5 font-mono break-all leading-relaxed">
                            Target: <span id="displayEmail" class="text-slate-400 font-bold">No Account Loaded</span>
                        </div>
                    </div>
                    <button onclick="copyEmail()" id="copyEmailBtn" class="bg-indigo-950/80 text-indigo-400 hover:bg-indigo-900 hover:text-indigo-200 border border-indigo-800/50 px-4 py-3 rounded-xl text-xs font-black transition cursor-pointer flex items-center shadow-md shrink-0">
                        <i class="fas fa-copy mr-1.5 text-xs"></i> Copy
                    </button>
                </div>

                <div class="bg-slate-950 p-6 md:p-8 rounded-xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-6 shadow-inner my-auto">
                    <div class="text-center sm:text-left">
                        <span id="codeTitle" class="text-[10px] font-black text-slate-500 block mb-1.5 uppercase tracking-widest">Verification Code:</span>
                        <span id="otpOutput" class="text-5xl md:text-6xl font-black tracking-widest text-slate-700 font-mono transition-all">XXXXXX</span>
                    </div>
                    <button onclick="copyCode()" class="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-4 rounded-xl text-xs md:text-sm font-black transition-all cursor-pointer shadow-lg flex justify-center items-center border border-indigo-500/30 shrink-0">
                        <i class="fas fa-clone mr-2"></i> Copy Code
                    </button>
                </div>

                <div class="text-[10px] font-mono text-center lg:text-right text-slate-600 pt-4">
                    <span>● Live Server Connection: Secured</span>
                </div>
            </div>

        </div>
    </div>

    <script>
        let currentPlatform = 'fb';
        const account1_data = "email1@outlook.com|pass1|refresh_token_1|client_id_1";
        const account2_data = "email2@outlook.com|pass2|refresh_token_2|client_id_2";

        document.getElementById('rawData').addEventListener('input', function(e) {
            const val = e.target.value.trim();
            document.getElementById('displayEmail').innerText = val.includes('|') ? val.split('|')[0] : "No Account Loaded";
        });

        function setPlatform(platform) {
            currentPlatform = platform;
            const fbBtn = document.getElementById('fbBtn');
            const igBtn = document.getElementById('igBtn');
            const modeBadge = document.getElementById('modeBadge');
            const badgeText = document.getElementById('badgeText');
            const inputBracket = document.getElementById('inputBracket');

            if(platform === 'fb') {
                fbBtn.className = "flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-xs md:text-sm font-black py-3.5 px-4 rounded-xl flex justify-center items-center transition-all duration-300 shadow-lg cursor-pointer";
                igBtn.className = "flex-1 bg-transparent text-slate-500 hover:text-slate-300 text-xs md:text-sm font-bold py-3.5 px-4 rounded-xl flex justify-center items-center transition-all duration-300 cursor-pointer";
                modeBadge.className = "mt-3 inline-flex items-center space-x-1.5 bg-amber-500/10 border border-amber-500/30 px-6 py-1 rounded-full shadow-sm";
                badgeText.innerText = "Facebook Priority Mode";
                inputBracket.style.borderColor = "#6366f1";
            } else {
                igBtn.className = "flex-1 bg-gradient-to-r from-purple-600 via-pink-500 to-orange-500 text-white text-xs md:text-sm font-black py-3.5 px-4 rounded-xl flex justify-center items-center transition-all duration-300 shadow-lg cursor-pointer";
                fbBtn.className = "flex-1 bg-transparent text-slate-500 hover:text-slate-300 text-xs md:text-sm font-bold py-3.5 px-4 rounded-xl flex justify-center items-center transition-all duration-300 cursor-pointer";
                modeBadge.className = "mt-3 inline-flex items-center space-x-1.5 bg-pink-500/10 border border-pink-500/30 px-6 py-1 rounded-full shadow-sm";
                badgeText.innerText = "Instagram Priority Mode";
                inputBracket.style.borderColor = "#ec4899";
            }
        }

        function loadAccount(num) {
            const data = num === 1 ? account1_data : account2_data;
            document.getElementById('rawData').value = data;
            document.getElementById('displayEmail').innerText = data.includes('|') ? data.split('|')[0] : "No Account Loaded";
        }

        function clearAll() {
            document.getElementById('rawData').value = "";
            document.getElementById('displayEmail').innerText = "No Account Loaded";
            document.getElementById('otpOutput').innerText = "XXXXXX";
            document.getElementById('otpOutput').className = "text-5xl md:text-6xl font-black tracking-widest text-slate-700 font-mono";
            document.getElementById('successMsg').innerText = "System Standing By";
            document.getElementById('statusDot').className = "fas fa-circle-notch text-indigo-400 mr-2 text-xs";
            document.getElementById('detectInfo').style.borderColor = "#6366f1";
        }

        async function getOtpCode() {
            const rawInput = document.getElementById('rawData').value.trim();
            const actionBtn = document.getElementById('actionBtn');
            const btnText = document.getElementById('btnText');
            const otpOutput = document.getElementById('otpOutput');
            const successMsg = document.getElementById('successMsg');
            const statusDot = document.getElementById('statusDot');
            const detectInfo = document.getElementById('detectInfo');

            if(!rawInput) {
                alert('Please enter or select account data line!');
                return;
            }

            actionBtn.disabled = true;
            actionBtn.className = "flex-[3] bg-indigo-600 text-white font-black py-4 px-5 rounded-xl transition-all duration-200 flex justify-center items-center text-xs md:text-sm tracking-wider uppercase shadow-lg";
            btnText.innerHTML = '<i class="fas fa-circle-notch fa-spin mr-2"></i> Fetching...';
            
            successMsg.innerText = "Connecting Mail API Cloud...";
            statusDot.className = "fas fa-circle-notch fa-spin mr-2 text-amber-400 text-xs";
            detectInfo.style.borderColor = "#f59e0b";
            otpOutput.innerText = "XXXXXX";
            otpOutput.className = "text-5xl md:text-6xl font-black tracking-widest text-slate-800 font-mono";

            try {
                const response = await fetch('/get-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ raw_input: rawInput, mode: currentPlatform })
                });
                const data = await response.json();
                resetButton();

                if(data.status === 'success') {
                    successMsg.innerText = (currentPlatform === 'fb' ? 'Facebook' : 'Instagram') + " OTP Extracted";
                    statusDot.className = "fas fa-check-circle mr-2 text-emerald-400 text-xs";
                    detectInfo.style.borderColor = "#10b981";
                    otpOutput.innerText = data.code;
                    otpOutput.className = "text-5xl md:text-6xl font-black tracking-widest text-emerald-400 font-mono drop-shadow-[0_0_15px_rgba(52,211,153,0.6)]";
                } else {
                    successMsg.innerText = "Session Rejected / No Code";
                    statusDot.className = "fas fa-times-circle mr-2 text-red-400 text-xs";
                    detectInfo.style.borderColor = "#ef4444";
                    otpOutput.innerText = data.message;
                    otpOutput.className = "text-sm md:text-base font-sans font-semibold text-red-400 px-2 text-center";
                }
            } catch (err) {
                resetButton();
                successMsg.innerText = "System Connection Error";
                statusDot.className = "fas fa-exclamation-triangle mr-2 text-red-400 text-xs";
                detectInfo.style.borderColor = "#ef4444";
                otpOutput.innerText = "ERROR";
                otpOutput.className = "text-2xl font-black text-red-500 font-sans";
            }
        }

        function resetButton() {
            const actionBtn = document.getElementById('actionBtn');
            const btnText = document.getElementById('btnText');
            actionBtn.disabled = false;
            actionBtn.className = "flex-[3] bg-slate-900 hover:bg-slate-800 text-slate-300 font-black py-4 px-5 rounded-xl border border-slate-800 transition-all duration-200 flex justify-center items-center cursor-pointer text-xs md:text-sm tracking-wider uppercase shadow-md";
            btnText.innerHTML = '<i class="fas fa-bolt mr-2 text-indigo-400"></i> Extract OTP Code';
        }

        function copyCode() {
            const text = document.getElementById('otpOutput').innerText;
            if(text && text !== 'XXXXXX' && text !== 'ERROR') {
                navigator.clipboard.writeText(text);
                alert('Verification Code Copied!');
            }
        }

        function copyEmail() {
            const emailText = document.getElementById('displayEmail').innerText;
            if(emailText && emailText !== 'No Account Loaded') {
                navigator.clipboard.writeText(emailText);
                alert('Email Copied successfully!');
            } else {
                alert('No Email loaded to copy!');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get-code', methods=['POST'])
def get_code():
    data = request.json or {}
    raw_input = data.get('raw_input', '').strip()
    mode = data.get('mode', 'fb')

    if '|' not in raw_input:
        return jsonify({'status': 'error', 'message': 'Invalid Format.'})

    parts = raw_input.split('|')
    if len(parts) < 4:
        return jsonify({'status': 'error', 'message': 'Format must be email|pass|token|client_id'})

    email = parts[0].strip()
    password = parts[1].strip()
    refresh_token = parts[2].strip()
    client_id = parts[3].strip()

    fb_code = extract_fb_code_via_api(email, refresh_token, client_id, mode)

    if fb_code.isdigit():
        return jsonify({'status': 'success', 'code': fb_code})
    else:
        return jsonify({'status': 'error', 'message': fb_code})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
