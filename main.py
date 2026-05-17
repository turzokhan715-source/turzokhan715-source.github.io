import re
from flask import Flask, request, jsonify, render_template_string
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ব্রাউজার ও পাইথনের সিকিউরিটি কানেকশন সচল রাখার জন্য

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


# =========================================================================
# VIP PORTAL DESIGN (Home, 2FA, UID Checker, and API Mail Integrated)
# =========================================================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Longisir VIP Portal</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        :root { 
            --primary: #a855f7; 
            --primary-glow: rgba(168, 85, 247, 0.3);
            --bg: #05060b; 
            --card-bg: #0f111a; 
            --input-bg: #111726;
            --text-gray: #94a3b8;
            --btn-grad: linear-gradient(135deg, #a855f7, #3b82f6);
            --border: rgba(255, 255, 255, 0.05);
        }

        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
            font-family: 'Plus Jakarta Sans', sans-serif; 
        }
        
        body { 
            background: var(--bg); 
            color: #fff; 
            padding: 20px 15px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
        }

        .container { 
            max-width: 1100px; 
            width: 100%;
            margin-top: 10px;
        }

        /* --- NAVIGATION BAR --- */
        .nav-bar {
            display: none; 
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            background: var(--card-bg);
            padding: 12px 24px;
            border-radius: 16px;
            border: 1px solid var(--border);
        }

        .nav-left .home-btn {
            background: var(--btn-grad);
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
            cursor: pointer;
            transition: 0.3s ease;
        }

        .nav-left .home-btn:hover {
            transform: translateY(-2px);
        }

        .nav-right {
            display: flex;
            gap: 12px;
        }

        .nav-link-btn {
            background: #111726;
            color: #f1f5f9;
            border: 1px solid var(--border);
            padding: 10px 18px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: 0.3s ease;
        }

        .nav-link-btn:hover {
            border-color: var(--primary);
            background: #161f33;
        }

        .nav-link-btn.active {
            background: var(--btn-grad);
            border: none;
        }

        /* --- PAGES --- */
        .page {
            display: none;
        }

        .page.active-page {
            display: block;
        }

        /* --- HOME PAGE --- */
        .hero {
            text-align: center;
            margin-bottom: 60px; 
            margin-top: 30px;
        }

        .hero h1 { font-size: clamp(32px, 7vw, 54px); font-weight: 800; margin-bottom: 8px; }
        .hero p { color: var(--text-gray); letter-spacing: 3px; font-size: 11px; font-weight: 600; text-transform: uppercase; }

        .home-grid { 
            display: grid;
            grid-template-columns: repeat(3, 1fr); 
            gap: 25px; 
            margin-bottom: 40px; 
        }
        
        .h-card { 
            background: var(--card-bg);
            border: 1px solid rgba(255,255,255,0.05); 
            padding: 50px 20px; 
            border-radius: 20px;
            text-align: center; 
            transition: 0.3s ease;
            cursor: pointer;
        }

        .h-card i { 
            font-size: 48px;
            color: var(--primary); 
            margin-bottom: 20px; 
            display: block;
            filter: drop-shadow(0 0 15px rgba(168, 85, 247, 0.5));
        }

        .h-card h3 { font-size: 20px; font-weight: 800; margin-bottom: 10px; }
        .h-card p { font-size: 13px; color: var(--text-gray); }
        .h-card:hover { transform: translateY(-6px); border-color: rgba(168, 85, 247, 0.3); background: #12141f; }

        .about-box { background: var(--card-bg); padding: 35px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.03); }
        .about-box h2 { color: var(--primary); margin-bottom: 15px; font-size: 24px; font-weight: 800; }
        .about-box p { color: var(--text-gray); font-size: 14px; line-height: 1.6; }

        /* --- TOOL PANELS --- */
        .tool-panel {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid var(--border);
        }

        .twofa-layout { max-width: 600px; margin: 0 auto; }
        .main-card { background: var(--card-bg); border-radius: 24px; padding: 40px; border: 1px solid var(--border); margin-bottom: 24px; }
        .tool-header { text-align: center; margin-bottom: 32px; }
        .tool-header h2 { font-size: 1.85rem; font-weight: 800; margin-bottom: 8px; }

        .input-group { margin-bottom: 24px; }
        label { display: block; font-weight: 600; margin-bottom: 10px; color: #e2e8f0; font-size: 0.875rem; }
        
        input[type="text"], textarea {
            width: 100%; padding: 16px; border: 2px solid #1e293b; border-radius: 14px;
            font-size: 1rem; color: #fff; background: var(--input-bg); transition: all 0.25s ease;
        }
        input[type="text"]:focus, textarea:focus { outline: none; border-color: var(--primary); background: #151c2e; }

        .btn-prime {
            width: 100%; padding: 16px; background: var(--btn-grad); color: #fff; border: none;
            border-radius: 14px; font-size: 1rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 8px 24px rgba(168, 85, 247, 0.3);
        }

        .code-display { background: linear-gradient(135deg, #111827 0%, #030712 100%); border: 2px solid #1e293b; border-radius: 14px; padding: 24px; text-align: center; margin-top: 15px; }
        .totp-code { font-size: 2.25rem; font-weight: 800; color: #34d399; font-family: 'Courier New', monospace; letter-spacing: 6px; }

        .history-card { background: var(--card-bg); border-radius: 24px; padding: 32px; border: 1px solid var(--border); max-height: 300px; display: flex; flex-direction: column; }
        .history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .history-list { overflow-y: auto; }
        .history-item { padding: 14px; background: #111726; border-radius: 14px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }

        textarea { height: 160px; font-family: 'Courier New', monospace; }
        .action-row { display: flex; gap: 12px; margin: 18px 0; }
        
        .btn-start { flex: 1; background: linear-gradient(135deg, #4f46e5, #3b82f6); color: white; border: none; padding: 16px; border-radius: 12px; font-size: 15px; font-weight: 700; cursor: pointer; text-transform: uppercase; }
        .btn-clear { background: #dc2626; color: white; border: none; padding: 0 25px; border-radius: 12px; font-size: 15px; font-weight: 700; cursor: pointer; text-transform: uppercase; }

        .console-box { width: 100%; height: 240px; background: #030712; border-radius: 12px; padding: 15px; font-family: 'Courier New', monospace; font-size: 13px; color: #34d399; overflow-y: auto; margin-bottom: 20px; border: 1px solid #1f2937; }
        .console-log { margin-bottom: 4px; word-break: break-all; }
        .log-live { color: #34d399; font-weight: 600; }
        .log-die { color: #f87171; }

        .footer-row { display: flex; flex-direction: column; gap: 15px; align-items: center; }
        @media (min-width: 600px) { .footer-row { flex-direction: row; justify-content: space-between; } }

        .stats-group { display: flex; gap: 10px; width: 100%; }
        @media (min-width: 600px) { .stats-group { width: auto; } }
        .stat-card { background: #111726; border: 1px solid #1e293b; border-radius: 10px; padding: 10px 15px; text-align: center; flex: 1; }
        .stat-num { font-size: 15px; font-weight: 700; display: block; }
        .stat-label { font-size: 10px; color: #9ca3af; font-weight: 700; text-transform: uppercase; }

        .btn-download { background: #059669; color: white; border: none; padding: 15px 28px; border-radius: 12px; font-size: 14px; font-weight: 700; cursor: pointer; text-transform: uppercase; width: 100%; }
        @media (min-width: 600px) { .btn-download { width: auto; } }

        /* PLATFORM SELECTOR FOR MAIL */
        .platform-select { display: flex; gap: 10px; margin-bottom: 15px; }
        .plat-btn { flex: 1; padding: 12px; border-radius: 10px; border: 1px solid #1e293b; background: #111726; color: #94a3b8; font-weight: 700; cursor: pointer; transition: 0.2s; }
        .plat-btn.active-plat { background: var(--btn-grad); color: white; border: none; }

        @media (max-width: 850px) { .home-grid { grid-template-columns: 1fr; gap: 15px; } }
    </style>
</head>
<body>

<div class="container">
    <nav class="nav-bar" id="globalNavBar">
        <div class="nav-left">
            <button class="home-btn" onclick="switchPage('home')"><i class="fa-solid fa-house"></i> HOME</button>
        </div>
        <div class="nav-right">
            <button class="nav-link-btn" id="nav-2fa" onclick="switchPage('2fa')"><i class="fa-solid fa-shield-halved"></i> 2FA AUTH</button>
            <button class="nav-link-btn" id="nav-uid" onclick="switchPage('uid')"><i class="fa-solid fa-bolt"></i> UID CHECKER</button>
            <button class="nav-link-btn" id="nav-mail" onclick="switchPage('mail')"><i class="fa-solid fa-envelope"></i> API MAIL</button>
        </div>
    </nav>

    <div id="page-home" class="page active-page">
        <header class="hero">
            <h1>Longisir VIP Portal</h1>
            <p>THE NEXT GEN AUTOMATION HUB</p>
        </header>
        
        <main class="home-grid">
            <div class="h-card" onclick="switchPage('2fa')">
                <i class="fa-solid fa-shield-halved"></i>
                <h3>2FA AUTH</h3>
                <p>Fast Code Gen</p>
            </div>
            <div class="h-card" onclick="switchPage('uid')">
                <i class="fa-solid fa-bolt"></i>
                <h3>UID CHECKER</h3>
                <p>Bulk Validator</p>
            </div>
            <div class="h-card" onclick="switchPage('mail')">
                <i class="fa-solid fa-envelope"></i>
                <h3>API MAIL</h3>
                <p>OTP Extractor</p>
            </div>
        </main>

        <footer class="about-box">
            <h2>About Portal</h2>
            <p>Welcome to Longisir VIP Portal. This premium ecosystem unifies elite automation routines into a seamless UI. Engine initialized and active.</p>
        </footer>
    </div>

    <div id="page-2fa" class="page">
        <div class="twofa-layout">
            <div class="main-card">
                <div class="tool-header">
                    <h2>🔐 2FA Authenticator Pro</h2>
                </div>
                <div class="input-group">
                    <label>Enter your 2FA Secret Key:</label>
                    <input type="text" id="secretKey" placeholder="JBSWY3DPEHPK3PXP">
                </div>
                <button class="btn-prime" onclick="generateCode()">🔑 Generate Code</button>
                <div id="codeDisplay" class="code-display" style="display: none;">
                    <div id="totpCode" class="totp-code">------</div>
                </div>
            </div>
        </div>
    </div>

    <div id="page-uid" class="page">
        <div class="tool-panel">
            <div class="tool-header"><h2>Bulk UID Checker Panel</h2></div>
            <div class="input-group">
                <textarea id="inputData" placeholder="Paste data here... (UID|PASS|2FA)"></textarea>
            </div>
            <div class="action-row">
                <button class="btn-start" id="startBtn" onclick="startScanner()">Start Scanner</button>
                <button class="btn-clear" onclick="clearTool()">Clear</button>
            </div>
            <div class="console-box" id="consoleScreen">Console ready...</div>
            <div class="footer-row">
                <div class="stats-group">
                    <div class="stat-card"><span class="stat-num total-color" id="totalCount">0</span><span class="stat-label">Total</span></div>
                    <div class="stat-card"><span class="stat-num live-color" id="livePercent">0% LIVE</span><span class="stat-label">Live</span></div>
                    <div class="stat-card"><span class="stat-num die-color" id="diePercent">0% DIE</span><span class="stat-label">Die</span></div>
                </div>
                <button class="btn-download" onclick="downloadLiveCSV()">Download Live Accounts</button>
            </div>
        </div>
    </div>

    <div id="page-mail" class="page">
        <div class="tool-panel">
            <div class="tool-header"><h2>Premium API MAIL Scraper Panel</h2></div>
            
            <label>Select Target Platform:</label>
            <div class="platform-select">
                <button id="mailFbBtn" class="plat-btn active-plat" onclick="setMailPlatform('fb')"><i class="fab fa-facebook"></i> Facebook</button>
                <button id="mailIgBtn" class="plat-btn" onclick="setMailPlatform('ig')"><i class="fab fa-instagram"></i> Instagram</button>
            </div>

            <div class="input-group">
                <label>Input Account Data (One account per line):</label>
                <textarea id="mailInputData" placeholder="email|password|refresh_token|client_id"></textarea>
            </div>
            
            <div class="action-row">
                <button class="btn-start" id="startMailBtn" onclick="startMailProcessor()">Start Mail Engine</button>
                <button class="btn-clear" onclick="clearMailTool()">Clear</button>
            </div>
            <div class="console-box" id="mailConsoleScreen" style="color: #38bdf8;">Console ready for Mail Server Engine...</div>
            <div class="footer-row">
                <div class="stats-group">
                    <div class="stat-card"><span class="stat-num total-color" id="mailTotalCount">0</span><span class="stat-label">Total Lines</span></div>
                    <div class="stat-card"><span class="stat-num live-color" id="mailSuccessCount" style="color: #34d399;">0 Success</span><span class="stat-label">OTP Extracted</span></div>
                </div>
                <button class="btn-download" onclick="downloadMailCSV()">Download Extracted Codes</button>
            </div>
        </div>
    </div>
</div>

<script>
    let mailPlatform = 'fb';
    let mailSuccessList = [];

    function switchPage(pageId) {
        const navBar = document.getElementById('globalNavBar');
        navBar.style.display = (pageId === 'home') ? 'none' : 'flex';
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
        document.querySelectorAll('.nav-link-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('page-' + pageId).classList.add('active-page');
        if(document.getElementById('nav-' + pageId)) document.getElementById('nav-' + pageId).classList.add('active');
    }

    function setMailPlatform(plat) {
        mailPlatform = plat;
        document.getElementById('mailFbBtn').classList.toggle('active-plat', plat === 'fb');
        document.getElementById('mailIgBtn').classList.toggle('active-plat', plat === 'ig');
    }

    // --- 2FA GENERATOR SIMULATION ---
    function generateCode() {
        const sk = document.getElementById('secretKey').value.trim();
        if(!sk) { alert('Enter secret!'); return; }
        document.getElementById('totpCode').textContent = Math.floor(100000 + Math.random() * 900000);
        document.getElementById('codeDisplay').style.display = 'block';
    }

    // --- UID CHECKER SIMULATION ---
    let liveAccounts = [];
    function startScanner() {
        const val = document.getElementById('inputData').value.trim();
        if(!val) return;
        const lines = val.split('\n');
        document.getElementById('totalCount').innerText = lines.length;
        const screen = document.getElementById('consoleScreen');
        screen.innerHTML = 'Scanning initialized...<br>';
        
        lines.forEach((line, index) => {
            setTimeout(() => {
                const parts = line.split('|');
                const uid = parts[0] || "Unknown";
                const isLive = Math.random() > 0.3;
                const div = document.createElement('div');
                if(isLive) {
                    div.className = 'console-log log-live';
                    div.innerText = `[LIVE] ${uid}`;
                    liveAccounts.push({uid, pass: parts[1]||'', twoFA: parts[2]||''});
                } else {
                    div.className = 'console-log log-die';
                    div.innerText = `[DEAD] ${uid}`;
                }
                screen.appendChild(div);
                screen.scrollTop = screen.scrollHeight;
            }, index * 400);
        });
    }

    function downloadLiveCSV() {
        if(liveAccounts.length === 0) return;
        let rows = ["UID,PASSWORD,2FA"];
        liveAccounts.forEach(a => rows.push(`"${a.uid}","${a.pass}","${a.twoFA}"`));
        const blob = new Blob([rows.join("\n")], {type: 'text/csv'});
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = "live_uids.csv";
        link.click();
    }

    function clearTool() { document.getElementById('inputData').value = ''; document.getElementById('consoleScreen').innerHTML = 'Console ready...'; }

    // --- API MAIL REAL ENGINE PROCESSING ---
    async function startMailProcessor() {
        const inputStr = document.getElementById('mailInputData').value.trim();
        const consoleScreen = document.getElementById('mailConsoleScreen');
        const startBtn = document.getElementById('startMailBtn');
        
        if (!inputStr) { alert("Please paste your email accounts first!"); return; }
        
        const lines = inputStr.split('\n').map(line => line.trim()).filter(line => line.length > 0);
        consoleScreen.innerHTML = "Starting Real Engine Connection to Flask Backend...<br>";
        
        startBtn.disabled = true;
        startBtn.innerText = "Processing Emails...";
        document.getElementById('mailTotalCount').innerText = lines.length;
        
        let successCount = 0;
        mailSuccessList = [];

        for (let i = 0; i < lines.length; i++) {
            const currentLine = lines[i];
            const logLine = document.createElement('div');
            logLine.className = 'console-log';
            
            try {
                // Flask-এর /get-code রাউটে লাইভ রিকোয়েস্ট পাঠানো হচ্ছে
                const response = await fetch('/get-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ raw_input: currentLine, mode: mailPlatform })
                });
                
                const result = await response.json();
                
                if (result.status === "success") {
                    logLine.style.color = "#34d399";
                    logLine.innerText = `[SUCCESS] Account: ${currentLine.split('|')[0]} -> OTP: ${result.code}`;
                    successCount++;
                    mailSuccessList.push({ email: currentLine.split('|')[0], code: result.code });
                } else {
                    logLine.style.color = "#f87171";
                    logLine.innerText = `[FAILED] ${currentLine.split('|')[0]} -> Error: ${result.message}`;
                }
            } catch (err) {
                logLine.style.color = "#ef4444";
                logLine.innerText = `[CRITICAL ERROR] Failed to talk with Python backend server.`;
            }
            
            consoleScreen.appendChild(logLine);
            document.getElementById('mailSuccessCount').innerText = `${successCount} Success`;
            consoleScreen.scrollTop = consoleScreen.scrollHeight;
        }
        
        const endLog = document.createElement('div');
        endLog.style.color = "#38bdf8";
        endLog.style.fontWeight = "bold";
        endLog.style.marginTop = "10px";
        endLog.innerText = "Mail Processing Tasks Completed!";
        consoleScreen.appendChild(endLog);
        
        startBtn.disabled = false;
        startBtn.innerText = "Start Mail Engine";
    }

    function downloadMailCSV() {
        if (mailSuccessList.length === 0) { alert("No extracted data available!"); return; }
        let csvRows = ["EMAIL,EXTRACTED_OTP_CODE"];
        mailSuccessList.forEach(item => { csvRows.push(`"${item.email}","${item.code}"`); });
        const blob = new Blob(["\ufeff" + csvRows.join("\n")], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "extracted_otp_data.csv";
        link.click();
    }

    function clearMailTool() {
        document.getElementById('mailInputData').value = '';
        document.getElementById('mailConsoleScreen').innerHTML = 'Console ready for Mail Server Engine...';
        document.getElementById('mailTotalCount').innerText = '0';
        document.getElementById('mailSuccessCount').innerText = '0 Success';
        mailSuccessList = [];
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
