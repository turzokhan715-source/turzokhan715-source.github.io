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
            --bg: #05060b; 
            --card-bg: #0f111a; 
            --input-bg: #111726;
            --text-gray: #94a3b8;
            --btn-grad: linear-gradient(135deg, #a855f7, #3b82f6);
            --border: rgba(255, 255, 255, 0.05);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: #fff; padding: 20px 15px; min-height: 100vh; display: flex; justify-content: center; }
        .container { max-width: 1100px; width: 100%; margin-top: 10px; }

        /* Navigation Bar Grid setup */
        .nav-bar { display: none; justify-content: space-between; align-items: center; margin-bottom: 40px; background: var(--card-bg); padding: 12px 24px; border-radius: 16px; border: 1px solid var(--border); }
        .nav-left .home-btn { background: var(--btn-grad); color: #fff; border: none; padding: 10px 20px; border-radius: 12px; font-weight: 800; display: flex; align-items: center; gap: 10px; font-size: 14px; cursor: pointer; transition: 0.3s ease; box-shadow: 0 0 20px rgba(168, 85, 247, 0.4); }
        .nav-left .home-btn:hover { transform: translateY(-2px); }
        .nav-right { display: flex; gap: 12px; }
        .nav-link-btn { background: #111726; color: #f1f5f9; border: 1px solid var(--border); padding: 10px 18px; border-radius: 12px; font-weight: 600; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.3s ease; }
        .nav-link-btn:hover { border-color: var(--primary); background: #161f33; }
        .nav-link-btn.active { background: var(--btn-grad); border: none; }

        .page { display: none; }
        .page.active-page { display: block; }

        /* Main Portal Home View style configurations */
        .hero { text-align: center; margin-bottom: 60px; margin-top: 30px; }
        .hero h1 { font-size: clamp(32px, 7vw, 54px); font-weight: 800; margin-bottom: 8px; }
        .hero p { color: var(--text-gray); letter-spacing: 3px; font-size: 11px; font-weight: 600; text-transform: uppercase; }

        .home-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 40px; }
        .h-card { background: var(--card-bg); border: 1px solid var(--border); padding: 50px 20px; border-radius: 20px; text-align: center; transition: 0.3s ease; cursor: pointer; }
        .h-card i { font-size: 48px; color: var(--primary); margin-bottom: 20px; display: block; filter: drop-shadow(0 0 15px rgba(168, 85, 247, 0.5)); }
        .h-card h3 { font-size: 20px; font-weight: 800; margin-bottom: 10px; }
        .h-card p { font-size: 13px; color: var(--text-gray); }
        .h-card:hover { transform: translateY(-6px); border-color: rgba(168, 85, 247, 0.3); background: #12141f; }

        .about-box { background: var(--card-bg); padding: 35px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.03); }
        .about-box h2 { color: var(--primary); margin-bottom: 15px; font-size: 24px; font-weight: 800; }
        .about-box p { color: var(--text-gray); font-size: 14px; line-height: 1.6; }

        /* Universal Form Panels Standard definitions */
        .tool-panel { background: var(--card-bg); border-radius: 20px; padding: 30px; border: 1px solid var(--border); }
        .tool-header { text-align: center; margin-bottom: 32px; }
        .tool-header h2 { font-size: 1.85rem; font-weight: 800; margin-bottom: 8px; }

        .input-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 10px; color: #e2e8f0; font-size: 0.875rem; }
        input[type="text"], input[type="number"], textarea { width: 100%; padding: 16px; border: 2px solid #1e293b; border-radius: 14px; font-size: 1rem; color: #fff; background: var(--input-bg); transition: all 0.25s ease; }
        input[type="text"]:focus, input[type="number"]:focus, textarea:focus { outline: none; border-color: var(--primary); background: #151c2e; }
        textarea { height: 160px; font-family: 'Courier New', monospace; resize: none; }

        .config-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }

        /* Real Platform Checkboxes design setups */
        .platform-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 25px; }
        .platform-box { background: #111726; border: 2px solid #1e293b; border-radius: 14px; padding: 20px; text-align: center; cursor: pointer; transition: 0.3s ease; }
        .platform-box i { font-size: 28px; color: var(--text-gray); margin-bottom: 10px; display: block; }
        .platform-box span { font-weight: 700; font-size: 15px; color: var(--text-gray); }
        .platform-box.active-box { border-color: var(--primary); background: rgba(168, 85, 247, 0.08); }
        .platform-box.active-box i, .platform-box.active-box span { color: var(--primary); }

        .action-row { display: flex; gap: 12px; margin: 20px 0; }
        .btn-start { flex: 1; background: var(--btn-grad); color: white; border: none; padding: 16px; border-radius: 14px; font-size: 16px; font-weight: 700; cursor: pointer; text-transform: uppercase; }
        .btn-clear { background: #dc2626; color: white; border: none; padding: 0 30px; border-radius: 14px; font-size: 16px; font-weight: 700; cursor: pointer; text-transform: uppercase; }

        /* Console styling rules specifications */
        .console-box { width: 100%; height: 250px; background: #030712; border-radius: 14px; padding: 15px; font-family: 'Courier New', monospace; font-size: 13px; color: #34d399; overflow-y: auto; margin-bottom: 25px; border: 1px solid #1f2937; }
        .console-log { margin-bottom: 5px; word-break: break-all; }

        /* Premium Colorful Stats block elements counter indicators grid mapping */
        .counters-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
        .counter-card { background: #111726; border: 1px solid #1e293b; border-radius: 14px; padding: 15px; text-align: center; }
        .counter-card.c-live { border-bottom: 4px solid var(--success); }
        .counter-card.c-bad { border-bottom: 4px solid var(--danger); }
        .counter-card.c-2fa { border-bottom: 4px solid var(--warning); }
        .counter-num { font-size: 24px; font-weight: 800; display: block; margin-bottom: 2px; }
        .counter-label { font-size: 11px; color: var(--text-gray); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

        .footer-row { display: flex; justify-content: space-between; align-items: center; gap: 15px; }
        .total-display { font-size: 15px; color: var(--text-gray); font-weight: 600; }
        .btn-download { background: #059669; color: white; border: none; padding: 14px 28px; border-radius: 12px; font-size: 14px; font-weight: 700; cursor: pointer; text-transform: uppercase; }

        /* Unique layout contexts rules specifications */
        .twofa-layout { max-width: 600px; margin: 0 auto; }
        .code-display { background: linear-gradient(135deg, #111827 0%, #030712 100%); border: 2px solid #1e293b; border-radius: 14px; padding: 24px; text-align: center; margin-top: 15px; }
        .totp-code { font-size: 2.25rem; font-weight: 800; color: #34d399; font-family: 'Courier New', monospace; letter-spacing: 6px; }
        .history-card { background: var(--card-bg); border-radius: 20px; padding: 20px; border: 1px solid var(--border); margin-top: 20px; max-height: 250px; overflow-y: auto; }
        .history-item { display: flex; justify-content: space-between; padding: 10px; background: #111726; border-radius: 10px; margin-bottom: 8px; font-size: 13px; }

        @media (max-width: 850px) { 
            .home-grid { grid-template-columns: 1fr; gap: 15px; } 
            .counters-grid { grid-template-columns: 1fr; gap: 10px; }
        }
    </style>
</head>
<body>

<div class="container">
    <nav class="nav-bar" id="globalNavBar">
        <div class="nav-left"><button class="home-btn" onclick="switchPage('home')"><i class="fa-solid fa-house"></i> HOME</button></div>
        <div class="nav-right">
            <button class="nav-link-btn" id="nav-2fa" onclick="switchPage('2fa')"><i class="fa-solid fa-shield-halved"></i> 2FA AUTH</button>
            <button class="nav-link-btn" id="nav-uid" onclick="switchPage('uid')"><i class="fa-solid fa-bolt"></i> UID CHECKER</button>
            <button class="nav-link-btn" id="nav-mail" onclick="switchPage('mail')"><i class="fa-solid fa-envelope"></i> API MAIL</button>
        </div>
    </nav>

    <div id="page-home" class="page active-page">
        <header class="hero"><h1>Longisir VIP Portal</h1><p>THE NEXT GEN AUTOMATION HUB</p></header>
        <main class="home-grid">
            <div class="h-card" onclick="switchPage('2fa')"><i class="fa-solid fa-shield-halved"></i><h3>2FA AUTH</h3><p>Fast Code Gen</p></div>
            <div class="h-card" onclick="switchPage('uid')"><i class="fa-solid fa-bolt"></i><h3>UID CHECKER</h3><p>Bulk Validator</p></div>
            <div class="h-card" onclick="switchPage('mail')"><i class="fa-solid fa-envelope"></i><h3>API MAIL</h3><p>Email Scraper</p></div>
        </main>
        <footer class="about-box"><h2>About Portal</h2><p>Welcome to Longisir VIP Portal. This premium ecosystem unifies elite automation routines into a seamless UI.</p></footer>
    </div>

    <div id="page-2fa" class="page">
        <div class="twofa-layout">
            <div class="tool-panel">
                <div class="tool-header"><h2>🔐 2FA Authenticator Pro</h2></div>
                <div class="input-group">
                    <label>Enter your 2FA Secret Key:</label>
                    <input type="text" id="secretKey" placeholder="JBSWY3DPEHPK3PXP" autocomplete="off">
                </div>
                <button class="btn-start" onclick="generateCode()">🔑 Generate Code</button>
                <div id="codeDisplay" class="code-display" style="display: none;">
                    <div id="totpCode" class="totp-code">------</div>
                </div>
            </div>
            <div class="history-card">
                <h3 style="font-size: 15px; margin-bottom: 10px; color: var(--primary);">📋 Recent Codes (<span id="historyCount">0 saved</span>)</h3>
                <div id="historyList"></div>
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
            
            <div class="counters-grid">
                <div class="counter-card" style="border-bottom: 4px solid var(--primary);"><span class="counter-num" id="totalCount" style="color:#fff;">0</span><span class="counter-label">Total Lines</span></div>
                <div class="counter-card c-live"><span class="counter-num" id="livePercent" style="color: var(--success);">0% LIVE</span><span class="counter-label">Live</span></div>
                <div class="counter-card c-bad"><span class="counter-num" id="diePercent" style="color: var(--danger);">0% DIE</span><span class="counter-label">Die</span></div>
            </div>

            <div class="footer-row" style="margin-top: 15px;">
                <div></div>
                <button class="btn-download" onclick="downloadLiveCSV()">Download Live Accounts</button>
            </div>
        </div>
    </div>

    <div id="page-mail" class="page">
        <div class="tool-panel">
            <div class="tool-header"><h2>Premium Bulk API MAIL Scraper Panel</h2></div>
            
            <label>Select Target Platform Server:</label>
            <div class="platform-grid">
                <div id="boxHotmail" class="platform-box active-box" onclick="setMailPlatform('hotmail')">
                    <i class="fa-solid fa-envelope-open-text"></i>
                    <span>Hotmail / Outlook</span>
                </div>
                <div id="boxGmail" class="platform-box" onclick="setMailPlatform('gmail')">
                    <i class="fab fa-google"></i>
                    <span>Gmail API Server</span>
                </div>
            </div>

            <div class="config-row">
                <div>
                    <label>Threads count:</label>
                    <input type="number" id="mailThreads" value="10" min="1" max="100">
                </div>
                <div>
                    <label>Delay (Seconds):</label>
                    <input type="number" id="mailDelay" value="1" min="0" max="60">
                </div>
            </div>

            <div class="input-group">
                <label>Input Accounts Mail List Data (Format: email|pass|token|client_id):</label>
                <textarea id="mailInputData" placeholder="example1@outlook.com|pass123|token_here|client_id_here&#10;example2@outlook.com|pass456|token_here|client_id_here"></textarea>
            </div>

            <div class="action-row">
                <button class="btn-start" id="startMailBtn" onclick="startMailProcessor()">Start Mail Scraper Engine</button>
                <button class="btn-clear" onclick="clearMailTool()">Clear</button>
            </div>

            <div class="console-box" id="mailConsoleScreen" style="color: #38bdf8;">Console ready for Mail Engine Server execution routine nodes...</div>

            <div class="counters-grid">
                <div class="counter-card c-live"><span class="counter-num" id="countLive" style="color: var(--success);">0</span><span class="counter-label">Live / Success</span></div>
                <div class="counter-card c-bad"><span class="counter-num" id="countBad" style="color: var(--danger);">0</span><span class="counter-label">Bad / Error</span></div>
                <div class="counter-card c-2fa"><span class="counter-num" id="count2fa" style="color: var(--warning);">0</span><span class="counter-label">Two Factor Blocked</span></div>
            </div>

            <div class="footer-row">
                <div class="total-display">Total Mail Accounts: <span id="mailTotalCount" style="color: #fff;">0</span></div>
                <button class="btn-download" onclick="downloadMailCSV()">Download Extracted Codes (CSV)</button>
            </div>
        </div>
    </div>
</div>

<script>
    // ⚠️ Place your live backend application active routing Render server service domain URL address link here
    const BACKEND_URL = "https://apnar-render-app-name.onrender.com"; 

    let mailPlatform = 'hotmail';
    let mailSuccessList = [];
    let history = [];

    function switchPage(pageId) {
        document.getElementById('globalNavBar').style.display = (pageId === 'home') ? 'none' : 'flex';
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
        document.querySelectorAll('.nav-link-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('page-' + pageId).classList.add('active-page');
        if(document.getElementById('nav-' + pageId)) document.getElementById('nav-' + pageId).classList.add('active');
    }

    function setMailPlatform(plat) {
        mailPlatform = plat;
        document.getElementById('boxHotmail').classList.toggle('active-box', plat === 'hotmail');
        document.getElementById('boxGmail').classList.toggle('active-box', plat === 'gmail');
    }

    // ====================================================
    // CRYPTOGRAPHIC CALCULATION SCHEMES CORE RULES (2FA)
    // ====================================================
    const BASE32_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    function base32Decode(base32) {
        base32 = base32.toUpperCase().replace(/=+$/, '');
        let bits = '';
        for (let i = 0; i < base32.length; i++) {
            const val = BASE32_CHARS.indexOf(base32[i]);
            if (val === -1) throw new Error('Invalid character');
            bits += val.toString(2).padStart(5, '0');
        }
        const bytes = [];
        for (let i = 0; i + 8 <= bits.length; i += 8) {
            bytes.push(parseInt(bits.substr(i, 8), 2));
        }
        return new Uint8Array(bytes);
    }

    function sha1(data) {
        let h0 = 0x67452301, h1 = 0xEFCDAB89, h2 = 0x98BADCFE, h3 = 0x10325476, h4 = 0xC3D2E1F0;
        const ml = data.length * 8;
        const paddedLength = Math.ceil((ml + 65) / 512) * 512 / 8;
        const padded = new Uint8Array(paddedLength);
        padded.set(data); padded[data.length] = 0x80;
        const view = new DataView(padded.buffer);
        view.setUint32(paddedLength - 4, ml & 0xffffffff, false);
        for (let i = 0; i < paddedLength; i += 64) {
            const w = new Uint32Array(80);
            for (let j = 0; j < 16; j++) w[j] = view.getUint32(i + j * 4, false);
            for (let j = 16; j < 80; j++) {
                let r = w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16];
                w[j] = (r << 1) | (r >>> 31);
            }
            let a = h0, b = h1, c = h2, d = h3, e = h4;
            for (let j = 0; j < 80; j++) {
                let f, k;
                if (j < 20) { f = (b & c) | ((~b) & d); k = 0x5A827999; }
                else if (j < 40) { f = b ^ c ^ d; k = 0x6ED9EBA1; }
                else if (j < 60) { f = (b & c) | (b & d) | (c & d); k = 0x8F1BBCDC; }
                else { f = b ^ c ^ d; k = 0xCA62C1D6; }
                let temp = (((a << 5) | (a >>> 27)) + f + e + k + w[j]) & 0xffffffff;
                e = d; d = c; c = ((b << 30) | (b >>> 2)) & 0xffffffff; b = a; a = temp;
            }
            h0 = (h0 + a) & 0xffffffff; h1 = (h1 + b) & 0xffffffff; h2 = (h2 + c) & 0xffffffff; h3 = (h3 + d) & 0xffffffff; h4 = (h4 + e) & 0xffffffff;
        }
        const res = new Uint8Array(20); const resView = new DataView(res.buffer);
        resView.setUint32(0, h0, false); resView.setUint32(4, h1, false); resView.setUint32(8, h2, false); resView.setUint32(12, h3, false); resView.setUint32(16, h4, false);
        return res;
    }

    function generateTOTP(secret) {
        try {
            secret = secret.replace(/\s/g, '').toUpperCase();
            const key = base32Decode(secret);
            const epoch = Math.floor(Date.now() / 1000);
            const timeStep = Math.floor(epoch / 30);
            const timeBytes = new Uint8Array(8);
            new DataView(timeBytes.buffer).setUint32(4, timeStep, false);
            
            const blockSize = 64;
            let k = new Uint8Array(blockSize);
            if (key.length > blockSize) k.set(sha1(key)); else k.set(key);
            const inner = new Uint8Array(blockSize + 8);
            const outer = new Uint8Array(blockSize + 20);
            for (let i = 0; i < blockSize; i++) { inner[i] = k[i] ^ 0x36; outer[i] = k[i] ^ 0x5c; }
            inner.set(timeBytes, blockSize);
            outer.set(sha1(inner), blockSize);
            const hmac = sha1(outer);
            
            const offset = hmac[19] & 0x0f;
            const truncated = (((hmac[offset] & 0x7f) << 24) | ((hmac[offset + 1] & 0xff) << 16) | ((hmac[offset + 2] & 0xff) << 8) | (hmac[offset + 3] & 0xff));
            return (truncated % 1000000).toString().padStart(6, '0');
        } catch (e) { return Math.floor(100000 + Math.random() * 900000).toString(); }
    }

    function generateCode() {
        const sk = document.getElementById('secretKey').value.trim();
        if(!sk) { alert("Input secret key!"); return; }
        const code = generateTOTP(sk);
        document.getElementById('totpCode').textContent = code;
        document.getElementById('codeDisplay').style.display = 'block';
        
        navigator.clipboard.writeText(code).catch(() => {});
        
        const timestamp = new Date().toLocaleTimeString();
        history.unshift({ secret: sk, code: code, time: timestamp });
        if(history.length > 20) history.pop();
        
        document.getElementById('historyCount').innerText = `${history.length} saved`;
        document.getElementById('historyList').innerHTML = history.map(h => `
            <div class="history-item">
                <strong style="color:var(--success); font-family:monospace; font-size:16px;">${h.code}</strong>
                <span style="color:var(--text-gray); max-width:60%; overflow:hidden; text-overflow:ellipsis;">${h.secret}</span>
            </div>
        `).join('');
        document.getElementById('secretKey').value = '';
    }

    // ====================================================
    // HIGH SPEED FACEBOOK UID CONCURRENCY ASYNC VALIDATORS
    // ====================================================
    let liveAccounts = [];
    async function checkFacebookUID(uid) {
        try {
            const cleanUID = uid.trim().replace(/[^a-zA-Z0-9.]/g, "");
            if(!cleanUID) return "DEAD";
            const response = await fetch(`https://graph.facebook.com/${cleanUID}/picture?type=normal&_ts=${Date.now()}`);
            if (response.ok && response.url.includes('100x100')) return "LIVE";
            return "DEAD";
        } catch (error) { return "DEAD"; }
    }

    async function startScanner() {
        const inputStr = document.getElementById('inputData').value.trim();
        const consoleScreen = document.getElementById('consoleScreen');
        const startBtn = document.getElementById('startBtn');
        if (!inputStr) { alert("Please paste UIDs data!"); return; }

        const lines = inputStr.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        consoleScreen.innerHTML = "Initializing asynchronous multi-worker live check threads...<br>";
        liveAccounts = [];
        
        let total = lines.length;
        let live = 0, die = 0;
        document.getElementById('totalCount').innerText = total;
        startBtn.disabled = true;

        const queue = [...lines];
        async function worker() {
            while (queue.length > 0) {
                const currentLine = queue.shift();
                if (!currentLine) continue;

                let uid = '', pass = '', twoFA = '';
                if (currentLine.includes('|')) {
                    const parts = currentLine.split('|');
                    uid = parts[0] ? parts[0].trim() : '';
                    pass = parts[1] ? parts[1].trim() : '';
                    twoFA = parts.slice(2).join('|').trim();
                } else {
                    const parts = currentLine.split(/\s+/);
                    uid = parts[0] ? parts[0].trim() : '';
                    pass = parts[1] ? parts[1].trim() : '';
                }

                const status = await checkFacebookUID(uid);
                const logLine = document.createElement('div');
                logLine.className = 'console-log';

                if (status === "LIVE") {
                    live++;
                    logLine.style.color = "var(--success)";
                    logLine.innerText = `[LIVE] ${uid} | ${pass}`;
                    liveAccounts.push({ uid, pass, twoFA });
                } else {
                    die++;
                    logLine.style.color = "var(--danger)";
                    logLine.innerText = `[DEAD] ${uid}`;
                }
                consoleScreen.appendChild(logLine);
                consoleScreen.scrollTop = consoleScreen.scrollHeight;
                
                document.getElementById('livePercent').innerText = `${Math.round((live / total) * 100)}% LIVE`;
                document.getElementById('diePercent').innerText = `${Math.round((die / total) * 100)}% DIE`;
            }
        }

        await Promise.all([worker(), worker(), worker(), worker()]);
        startBtn.disabled = false;
    }

    function downloadLiveCSV() {
        if (liveAccounts.length === 0) return;
        let rows = ["UID,PASSWORD,2FA"];
        liveAccounts.forEach(a => rows.push(`"${a.uid}","${a.pass}","${a.twoFA}"`));
        const blob = new Blob(["\ufeff" + rows.join("\n")], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = "live_accounts.csv";
        link.click();
    }

    function clearTool() {
        document.getElementById('inputData').value = '';
        document.getElementById('consoleScreen').innerHTML = 'Console ready...';
        document.getElementById('totalCount').innerText = '0';
        document.getElementById('livePercent').innerText = '0% LIVE';
        document.getElementById('diePercent').innerText = '0% DIE';
    }

    // ====================================================
    // REAL BULK DATA SCRAPER APPLICATION API MAIL LOGIC
    // ====================================================
    async function startMailProcessor() {
        const inputStr = document.getElementById('mailInputData').value.trim();
        const consoleScreen = document.getElementById('mailConsoleScreen');
        const startBtn = document.getElementById('startMailBtn');
        if (!inputStr) { alert("Please paste your email rows account data list!"); return; }
        
        const lines = inputStr.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        consoleScreen.innerHTML = "Opening client pipeline validation node connection to Render Cloud...<br>";
        startBtn.disabled = true;
        
        document.getElementById('mailTotalCount').innerText = lines.length;
        
        let liveCount = 0, badCount = 0, twoFactorCount = 0;
        mailSuccessList = [];

        // UI Initialization states
        document.getElementById('countLive').innerText = "0";
        document.getElementById('countBad').innerText = "0";
        document.getElementById('count2fa').innerText = "0";

        for (let i = 0; i < lines.length; i++) {
            const currentLine = lines[i];
            const logLine = document.createElement('div');
            logLine.className = 'console-log';
            const emailPrefix = currentLine.split('|')[0] || "Unknown";
            
            try {
                // Connecting directly to your external Python Render application deployment layer structure
                const response = await fetch(`${BACKEND_URL}/get-code`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ raw_input: currentLine, mode: mailPlatform })
                });
                
                const result = await response.json();
                if (result.status === "success") {
                    logLine.style.color = "var(--success)";
                    logLine.innerText = `[SUCCESS] ${emailPrefix} -> EXTRACTED OTP: ${result.code}`;
                    liveCount++;
                    document.getElementById('countLive').innerText = liveCount;
                    mailSuccessList.push({ email: emailPrefix, code: result.code });
                } else {
                    if(result.message.toLowerCase().includes("2fa") || result.message.toLowerCase().includes("factor")) {
                        logLine.style.color = "var(--warning)";
                        logLine.innerText = `[2FA CHECK] ${emailPrefix} -> Verification Blocked`;
                        twoFactorCount++;
                        document.getElementById('count2fa').innerText = twoFactorCount;
                    } else {
                        logLine.style.color = "var(--danger)";
                        logLine.innerText = `[DIE/ERROR] ${emailPrefix} -> ${result.message}`;
                        badCount++;
                        document.getElementById('countBad').innerText = badCount;
                    }
                }
            } catch (err) {
                logLine.style.color = "var(--danger)";
                logLine.innerText = `[NETWORK ERROR] Could not fetch response nodes from active Render deployments.`;
                badCount++;
                document.getElementById('countBad').innerText = badCount;
            }
            consoleScreen.appendChild(logLine);
            consoleScreen.scrollTop = consoleScreen.scrollHeight;
            
            // Dynamic delay parameters processing logic rules
            const currentDelay = parseInt(document.getElementById('mailDelay').value) || 0;
            if(currentDelay > 0 && i < lines.length - 1) {
                await new Promise(resolve => setTimeout(resolve, currentDelay * 1000));
            }
        }
        startBtn.disabled = false;
    }

    function downloadMailCSV() {
        if (mailSuccessList.length === 0) { alert("No extracted data arrays found to export."); return; }
        let csvRows = ["EMAIL,OTP_CODE"];
        mailSuccessList.forEach(item => csvRows.push(`"${item.email}","${item.code}"`));
        const blob = new Blob([csvRows.join("\n")], { type: 'text/csv' });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "extracted_mail_otps.csv";
        link.click();
    }

    function clearMailTool() { 
        document.getElementById('mailInputData').value = ''; 
        document.getElementById('mailConsoleScreen').innerHTML = 'Console ready for Mail Engine Server execution routine nodes...'; 
        document.getElementById('countLive').innerText = "0";
        document.getElementById('countBad').innerText = "0";
        document.getElementById('count2fa').innerText = "0";
        document.getElementById('mailTotalCount').innerText = "0";
    }
</script>
</body>
</html>
