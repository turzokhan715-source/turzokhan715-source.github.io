import os
import re
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# 🌐 ব্রাউজারের সিকিউরিটি ব্লক সমস্যা দূর করার জন্য CORS সচল করা হলো
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


# 🔍 ইমেইল ছেঁকে বের করার ফাংশন
def extract_email_from_string(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    return match.group(0).strip() if match else None


# 🔮 ULTRA-PREMIUM INTERFACE (HTML/Tailwind/JavaScript UI)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB & IG OTP Extractor Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="bg-[#0b0f19] text-gray-100 min-h-screen flex flex-col justify-center items-center p-4 font-sans selection:bg-blue-500 selection:text-white">

    <div class="w-full max-w-md bg-gradient-to-b from-[#111827] to-[#1f2937] border border-white/5 rounded-3xl shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5),0_0_40px_rgba(59,130,246,0.1)] p-6 relative overflow-hidden">
        
        <div class="absolute -top-[50px] left-1/2 -translate-x-1/2 w-[180px] h-[180px] bg-gradient-to-b from-blue-500/10 to-transparent rounded-full pointer-events-none"></div>

        <div class="text-center mb-6 relative z-10">
            <div class="text-4xl mb-2 drop-shadow-[0_0_12px_rgba(147,51,234,0.6)]">🔮</div>
            <h2 class="text-2xl font-black text-white tracking-tight bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">FB & IG OTP Extractor</h2>
            <p class="text-xs text-gray-400 font-medium mt-1 tracking-wide">Next-Gen Verification Code Hub</p>
        </div>

        <div class="flex justify-center mb-6">
            <div id="modeBadge" class="bg-amber-500/10 border border-amber-500/30 text-amber-400 px-4 py-1.5 rounded-full text-[11px] font-extrabold tracking-wider shadow-[0_0_15px_rgba(217,119,6,0.1)]">
                ⚡ FACEBOOK PRIORITY MODE
            </div>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
            <button id="tab-fb" onclick="setMailMode('facebook')" class="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-3 rounded-xl font-bold text-xs cursor-pointer shadow-[0_4px_15px_rgba(37,99,235,0.25)] transition duration-200 focus:outline-none">
                Facebook <span class="bg-amber-500 text-white text-[9px] px-1.5 py-0.5 rounded ml-1 font-black">1st</span>
            </button>
            <button id="tab-ig" onclick="setMailMode('instagram')" class="bg-[#1f2937] text-gray-400 border border-white/5 p-3 rounded-xl font-semibold text-xs cursor-pointer transition duration-200 focus:outline-none">
                📷 Instagram <span id="igBadgeLabel" class="bg-gray-700 text-gray-400 text-[9px] px-1.5 py-0.5 rounded ml-1 font-bold">2nd</span>
            </button>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-6">
            <div class="bg-blue-500/5 border border-blue-500/10 p-2.5 rounded-xl text-center text-xs font-bold text-blue-400 flex items-center justify-center gap-1.5">
                👤 Account 1
            </div>
            <div class="bg-purple-500/5 border border-purple-500/10 p-2.5 rounded-xl text-center text-xs font-bold text-purple-400 flex items-center justify-center gap-1.5">
                🔮 Account 2
            </div>
        </div>

        <div class="border-l-2 border-blue-500 pl-1 mb-6">
            <div class="text-[11px] font-bold text-gray-400 mb-2 pl-1 tracking-wider uppercase">📋 Paste your account data line:</div>
            <textarea id="mailInputData" oninput="liveUpdateEmailDisplay()" placeholder="এখানে ডাটা পেস্ট করুন... মেইল সাথে সাথে শো করবে" class="w-full h-24 bg-[#111827] border border-white/5 rounded-xl p-3 text-xs font-mono text-blue-400 focus:outline-none focus:border-blue-500 transition duration-200 resize-none shadow-inner leading-relaxed"></textarea>
        </div>

        <div class="grid grid-cols-3 gap-3 mb-6">
            <button id="startMailBtn" onclick="startMailProcessor()" class="col-span-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white p-3.5 rounded-xl text-xs font-extrabold uppercase tracking-wider cursor-pointer shadow-[0_4px_20px_rgba(37,99,235,0.25)] transition duration-200 focus:outline-none">
                🔍 Extract Code
            </button>
            <button onclick="clearMailTool()" class="bg-[#374151] hover:bg-gray-600 border border-white/5 text-gray-200 p-3.5 rounded-xl text-xs font-bold uppercase cursor-pointer transition duration-200 focus:outline-none">
                🗑️ Clear
            </button>
        </div>

        <div id="mailStatusAlertBox" class="bg-[#111827] border border-white/5 border-l-4 border-gray-600 rounded-2xl p-4 mb-5 flex justify-between items-center gap-3 transition-all duration-300">
            <div class="min-w-0 flex-1">
                <div id="mailStatusTitle" class="text-[11px] font-black text-gray-400 mb-1 tracking-wider uppercase">💤 Engine Idle</div>
                <div id="currentProcessingMail" class="text-xs font-mono text-gray-200 break-all font-semibold leading-relaxed">Mail: Waiting for data...</div>
            </div>
            <button onclick="copyTextToClipboard('currentProcessingMail', 'Email Copied!')" class="bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/20 px-3 py-2 rounded-xl text-[11px] font-bold cursor-pointer transition whitespace-nowrap focus:outline-none">
                ✉️ Copy
            </button>
        </div>

        <div class="bg-gradient-to-b from-[#111827] to-[#0f172a] border border-white/5 rounded-2xl p-4 shadow-inner flex justify-between items-center gap-3">
            <div class="min-w-0">
                <span class="text-[10px] font-extrabold text-gray-500 tracking-wider uppercase block mb-1">Verification Code:</span>
                <div id="extractedOtpValue" class="text-2xl font-black font-mono text-gray-500 tracking-widest break-all">EMPTY</div>
            </div>
            <button id="copyCodeBtn" onclick="copyTextToClipboard('extractedOtpValue', 'OTP Code Copied!')" class="bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white px-4 py-2.5 rounded-xl text-xs font-extrabold cursor-pointer shadow-[0_4px_15px_rgba(16,185,129,0.25)] transition whitespace-nowrap focus:outline-none">
                🔷 Copy Code
            </button>
        </div>

    </div>

    <script>
        let currentMailMode = 'facebook';

        function liveUpdateEmailDisplay() {
            const inputData = document.getElementById('mailInputData').value.trim();
            const mailDisplay = document.getElementById('currentProcessingMail');
            
            if (!inputData) {
                mailDisplay.innerText = "Mail: Waiting for data...";
                return;
            }

            const firstLine = inputData.split('\\n')[0].trim();
            const detectedEmail = extractEmailFromString(firstLine);
            
            if (detectedEmail) {
                mailDisplay.innerText = "Mail: " + detectedEmail;
            } else {
                mailDisplay.innerText = "Mail: No Email Detected";
            }
        }

        function extractEmailFromString(text) {
            const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/;
            const match = text.match(emailRegex);
            return match ? match[0].trim() : null;
        }

        function setMailMode(mode) {
            currentMailMode = mode;
            const fbTab = document.getElementById('tab-fb');
            const igTab = document.getElementById('tab-ig');
            const modeBadge = document.getElementById('modeBadge');
            const igLabel = document.getElementById('igBadgeLabel');

            if (mode === 'facebook') {
                fbTab.className = "bg-gradient-to-r from-blue-600 to-blue-700 text-white p-3 rounded-xl font-bold text-xs cursor-pointer shadow-[0_4px_15px_rgba(37,99,235,0.25)] transition duration-200 focus:outline-none";
                igTab.className = "bg-[#1f2937] text-gray-400 border border-white/5 p-3 rounded-xl font-semibold text-xs cursor-pointer transition duration-200 focus:outline-none";
                igLabel.className = "bg-gray-700 text-gray-400 text-[9px] px-1.5 py-0.5 rounded ml-1 font-bold";
                modeBadge.innerText = "⚡ FACEBOOK PRIORITY MODE";
                modeBadge.className = "bg-amber-500/10 border border-amber-500/30 text-amber-400 px-4 py-1.5 rounded-full text-[11px] font-extrabold tracking-wider";
            } else {
                igTab.className = "bg-gradient-to-r from-purple-500 to-purple-600 text-white p-3 rounded-xl font-bold text-xs cursor-pointer shadow-[0_4px_15px_rgba(168,85,247,0.25)] transition duration-200 focus:outline-none";
                fbTab.className = "bg-[#1f2937] text-gray-400 border border-white/5 p-3 rounded-xl font-semibold text-xs cursor-pointer transition duration-200 focus:outline-none";
                igLabel.className = "bg-amber-500 text-white text-[9px] px-1.5 py-0.5 rounded ml-1 font-black";
                modeBadge.innerText = "📷 INSTAGRAM PRIORITY MODE";
                modeBadge.className = "bg-pink-500/10 border border-pink-500/30 text-pink-400 px-4 py-1.5 rounded-full text-[11px] font-extrabold tracking-wider";
            }
        }

        async function startMailProcessor() {
            const inputData = document.getElementById('mailInputData').value.trim();
            const startBtn = document.getElementById('startMailBtn');
            const alertBox = document.getElementById('mailStatusAlertBox');
            const statusTitle = document.getElementById('mailStatusTitle');
            const mailDisplay = document.getElementById('currentProcessingMail');
            const otpDisplay = document.getElementById('extractedOtpValue');

            if (!inputData) { 
                alert("Please input credential string sets!"); 
                return; 
            }

            const firstLine = inputData.split('\\n')[0].trim();
            const detectedEmail = extractEmailFromString(firstLine);

            startBtn.disabled = true;
            startBtn.innerText = "⏳ Processing...";
            alertBox.style.borderLeftColor = "#3b82f6"; 
            statusTitle.innerText = "⚡ Fetching OTP...";
            statusTitle.style.color = "#3b82f6";
            
            otpDisplay.innerText = "WAITING";
            otpDisplay.className = "text-2xl font-black font-mono text-blue-400 animate-pulse tracking-widest break-all";

            try {
                // 🛠️ ফিক্স: হার্ডকোডেড স্লাশ তুলে সরাসরি রিলেটিভ পাথ ব্যবহার করা হয়েছে
                const response = await fetch('get-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ raw_input: firstLine, mode: currentMailMode })
                });
                const result = await response.json();

                startBtn.disabled = false;
                startBtn.innerText = "🔍 Extract Code";

                if (result.status === "success") {
                    alertBox.style.borderLeftColor = "#10b981"; 
                    statusTitle.innerText = "✅ OTP Extracted Successfully";
                    statusTitle.style.color = "#10b981";
                    mailDisplay.innerText = "Mail: " + result.email;
                    otpDisplay.className = "text-2xl font-black font-mono text-emerald-400 tracking-widest break-all";
                    otpDisplay.innerText = result.code; 
                } else {
                    alertBox.style.borderLeftColor = "#ef4444"; 
                    statusTitle.innerText = "❌ Failed";
                    statusTitle.style.color = "#ef4444";
                    otpDisplay.innerText = result.message;
                    otpDisplay.className = "text-xs font-sans font-bold text-red-400 break-all";
                }
            } catch (err) {
                startBtn.disabled = false;
                startBtn.innerText = "🔍 Extract Code";
                alertBox.style.borderLeftColor = "#ef4444";
                statusTitle.innerText = "⚠️ Server Connection Failed";
                statusTitle.style.color = "#ef4444";
                otpDisplay.innerText = "RETRY";
                otpDisplay.className = "text-2xl font-black font-mono text-red-500";
            }
        }

        function copyTextToClipboard(elementId, successMessage) {
            let textToCopy = document.getElementById(elementId).innerText.replace("Mail: ", "").trim();
            if (textToCopy === "EMPTY" || textToCopy === "WAITING" || textToCopy.includes("Waiting for data")) {
                alert("No valid data to copy!");
                return;
            }
            navigator.clipboard.writeText(textToCopy).then(() => alert(successMessage));
        }

        function clearMailTool() { 
            document.getElementById('mailInputData').value = ''; 
            document.getElementById('extractedOtpValue').innerText = 'EMPTY';
            document.getElementById('extractedOtpValue').className = "text-2xl font-black font-mono text-gray-500 tracking-widest break-all";
            
            const alertBox = document.getElementById('mailStatusAlertBox');
            const statusTitle = document.getElementById('mailStatusTitle');
            
            alertBox.style.borderLeftColor = "#4b5563";
            statusTitle.innerText = "💤 Engine Idle";
            statusTitle.style.color = "#94a3b8";
            document.getElementById('currentProcessingMail').innerText = 'Mail: Waiting for data...';
        }
    </script>
</body>
</html>
"""


# রেন্ডার এবং লোকাল হোস্টে ইন্টারফেস রেন্ডার করার রুট
@app.route('/', methods=['GET', 'HEAD'])
def home():
    return render_template_string(HTML_TEMPLATE)


# ওটিপি রিকোয়েস্ট হ্যান্ডলার এপিআই এন্ডপয়েন্ট
@app.route('/get-code', methods=['POST'])
def get_code():
    try:
        data = request.get_json() or {}
        raw_input = data.get('raw_input', '').strip()

        if not raw_input:
            return jsonify({'status': 'error', 'message': 'Input empty.'})

        detected_email = extract_email_from_string(raw_input)
        if not detected_email:
            return jsonify({'status': 'error', 'message': 'No valid email found in data.'})

        parts = raw_input.split('|')
        if len(parts) < 4:
            return jsonify({'status': 'error', 'message': 'Format must be email|pass|token|client_id'})

        email = detected_email
        password = parts[1].strip()
        refresh_token = parts[2].strip()
        client_id = parts[3].strip()

        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        if fb_code.isdigit():
            return jsonify({
                'status': 'success', 
                'email': email, 
                'code': fb_code
            })
        else:
            return jsonify({
                'status': 'error', 
                'message': fb_code
            })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
