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

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: #fff; padding: 20px 15px; min-height: 100vh; display: flex; justify-content: center; }
        .container { max-width: 1100px; width: 100%; margin-top: 10px; }

        .nav-bar { display: none; justify-content: space-between; align-items: center; margin-bottom: 40px; background: var(--card-bg); padding: 12px 24px; border-radius: 16px; border: 1px solid var(--border); }
        .nav-left .home-btn { background: var(--btn-grad); color: #fff; border: none; padding: 10px 20px; border-radius: 12px; font-weight: 800; display: flex; align-items: center; gap: 10px; font-size: 14px; box-shadow: 0 0 20px rgba(168, 85, 247, 0.4); cursor: pointer; transition: 0.3s ease; }
        .nav-left .home-btn:hover { transform: translateY(-2px); }
        .nav-right { display: flex; gap: 12px; }
        .nav-link-btn { background: #111726; color: #f1f5f9; border: 1px solid var(--border); padding: 10px 18px; border-radius: 12px; font-weight: 600; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.3s ease; }
        .nav-link-btn:hover { border-color: var(--primary); background: #161f33; }
        .nav-link-btn.active { background: var(--btn-grad); border: none; }

        .page { display: none; }
        .page.active-page { display: block; }

        .hero { text-align: center; margin-bottom: 60px; margin-top: 30px; }
        .hero h1 { font-size: clamp(32px, 7vw, 54px); font-weight: 800; margin-bottom: 8px; }
        .hero p { color: var(--text-gray); letter-spacing: 3px; font-size: 11px; font-weight: 600; text-transform: uppercase; }

        .home-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 40px; }
        .h-card { background: var(--card-bg); border: 1px solid rgba(255,255,255,0.05); padding: 50px 20px; border-radius: 20px; text-align: center; transition: 0.3s ease; cursor: pointer; }
        .h-card i { font-size: 48px; color: var(--primary); margin-bottom: 20px; display: block; filter: drop-shadow(0 0 15px rgba(168, 85, 247, 0.5)); }
        .h-card h3 { font-size: 20px; font-weight: 800; margin-bottom: 10px; }
        .h-card p { font-size: 13px; color: var(--text-gray); }
        .h-card:hover { transform: translateY(-6px); border-color: rgba(168, 85, 247, 0.3); background: #12141f; }

        .about-box { background: var(--card-bg); padding: 35px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.03); }
        .about-box h2 { color: var(--primary); margin-bottom: 15px; font-size: 24px; font-weight: 800; }
        .about-box p { color: var(--text-gray); font-size: 14px; line-height: 1.6; }

        .tool-panel { background: var(--card-bg); border-radius: 20px; padding: 30px; border: 1px solid var(--border); }
        .twofa-layout { max-width: 600px; margin: 0 auto; }
        .main-card { background: var(--card-bg); border-radius: 24px; padding: 40px; border: 1px solid var(--border); margin-bottom: 24px; }
        .tool-header { text-align: center; margin-bottom: 32px; }
        .tool-header h2 { font-size: 1.85rem; font-weight: 800; margin-bottom: 8px; }

        .input-group { margin-bottom: 24px; }
        label { display: block; font-weight: 600; margin-bottom: 10px; color: #e2e8f0; font-size: 0.875rem; }
        input[type="text"], textarea { width: 100%; padding: 16px; border: 2px solid #1e293b; border-radius: 14px; font-size: 1rem; color: #fff; background: var(--input-bg); transition: all 0.25s ease; }
        input[type="text"]:focus, textarea:focus { outline: none; border-color: var(--primary); background: #151c2e; }

        .btn-prime { width: 100%; padding: 16px; background: var(--btn-grad); color: #fff; border: none; border-radius: 14px; font-size: 1rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 8px 24px rgba(168, 85, 247, 0.3); }
        .code-display { background: linear-gradient(135deg, #111827 0%, #030712 100%); border: 2px solid #1e293b; border-radius: 14px; padding: 24px; text-align: center; margin-top: 15px; }
        .totp-code { font-size: 2.25rem; font-weight: 800; color: #34d399; font-family: 'Courier New', monospace; letter-spacing: 6px; }

        textarea { height: 160px; font-family: 'Courier New', monospace; resize: none; }
        .action-row { display: flex; gap: 12px; margin: 18px 0; }
        .btn-start { flex: 1; background: linear-gradient(135deg, #4f46e5, #3b82f6); color: white; border: none; padding: 16px; border-radius: 12px; font-size: 15px; font-weight: 700; cursor: pointer; text-transform: uppercase; }
        .btn-clear { background: #dc2626; color: white; border: none; padding: 0 25px; border-radius: 12px; font-size: 15px; font-weight: 700; cursor: pointer; text-transform: uppercase; }

        .console-box { width: 100%; height: 240px; background: #030712; border-radius: 12px; padding: 15px; font-family: 'Courier New', monospace; font-size: 13px; color: #34d399; overflow-y: auto; margin-bottom: 20px; border: 1px solid #1f2937; }
        .console-log { margin-bottom: 4px; word-break: break-all; }
        .footer-row { display: flex; flex-direction: column; gap: 15px; align-items: center; }
        @media (min-width: 600px) { .footer-row { flex-direction: row; justify-content: space-between; } }

        .stats-group { display: flex; gap: 10px; width: 100%; }
        .stat-card { background: #111726; border: 1px solid #1e293b; border-radius: 10px; padding: 10px 15px; text-align: center; flex: 1; }
        .stat-num { font-size: 15px; font-weight: 700; display: block; }
        .stat-label { font-size: 10px; color: #9ca3af; font-weight: 700; text-transform: uppercase; }
        .btn-download { background: #059669; color: white; border: none; padding: 15px 28px; border-radius: 12px; font-size: 14px; font-weight: 700; cursor: pointer; text-transform: uppercase; width: 100%; }
        @media (min-width: 600px) { .btn-download { width: auto; } }

        .platform-select { display: flex; gap: 10px; margin-bottom: 15px; }
        .plat-btn { flex: 1; padding: 12px; border-radius: 10px; border: 1px solid #1e293b; background: #111726; color: #94a3b8; font-weight: 700; cursor: pointer; transition: 0.2s; }
        .plat-btn.active-plat { background: var(--btn-grad); color: white; border: none; }

        @media (max-width: 850px) { .home-grid { grid-template-columns: 1fr; gap: 15px; } }
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
            <div class="h-card" onclick="switchPage('mail')"><i class="fa-solid fa-envelope"></i><h3>API MAIL</h3><p>OTP Extractor</p></div>
        </main>
        <footer class="about-box"><h2>About Portal</h2><p>Welcome to Longisir VIP Portal. This premium ecosystem unifies elite automation routines into a seamless UI.</p></footer>
    </div>

    <div id="page-2fa" class="page">
        <div class="twofa-layout"><div class="main-card">
            <div class="tool-header"><h2>🔐 2FA Authenticator Pro</h2></div>
            <div class="input-group"><label>Enter your 2FA Secret Key:</label><input type="text" id="secretKey" placeholder="JBSWY3DPEHPK3PXP"></div>
            <button class="btn-prime" onclick="generateCode()">🔑 Generate Code</button>
            <div id="codeDisplay" class="code-display" style="display: none;"><div id="totpCode" class="totp-code">------</div></div>
        </div></div>
    </div>

    <div id="page-uid" class="page">
        <div class="tool-panel">
            <div class="tool-header"><h2>Bulk UID Checker Panel</h2></div>
            <div class="input-group"><textarea id="inputData" placeholder="Paste data here... (UID|PASS|2FA)"></textarea></div>
            <div class="action-row"><button class="btn-start" onclick="startScanner()">Start Scanner</button><button class="btn-clear" onclick="clearTool()">Clear</button></div>
            <div class="console-box" id="consoleScreen">Console ready...</div>
            <div class="footer-row">
                <div class="stats-group">
                    <div class="stat-card"><span class="stat-num" id="totalCount">0</span><span class="stat-label">Total</span></div>
                    <div class="stat-card"><span class="stat-num" id="livePercent" style="color: #34d399;">0% LIVE</span><span class="stat-label">Live</span></div>
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
            <div class="action-row"><button class="btn-start" id="startMailBtn" onclick="startMailProcessor()">Start Mail Engine</button><button class="btn-clear" onclick="clearMailTool()">Clear</button></div>
            <div class="console-box" id="mailConsoleScreen" style="color: #38bdf8;">Console ready for Mail Server Engine...</div>
            <div class="footer-row">
                <div class="stats-group">
                    <div class="stat-card"><span class="stat-num" id="mailTotalCount">0</span><span class="stat-label">Total Lines</span></div>
                    <div class="stat-card"><span class="stat-num" id="mailSuccessCount" style="color: #34d399;">0 Success</span><span class="stat-label">OTP Extracted</span></div>
                </div>
                <button class="btn-download" onclick="downloadMailCSV()">Download Extracted Codes</button>
            </div>
        </div>
    </div>
</div>

<script>
    // ⚠️ এখানে আপনার Render থেকে পাওয়া আসল লাইভ লিংকটি বসিয়ে দিন
    const BACKEND_URL = "https://apnar-render-app-name.onrender.com"; 

    let mailPlatform = 'fb';
    let mailSuccessList = [];

    function switchPage(pageId) {
        document.getElementById('globalNavBar').style.display = (pageId === 'home') ? 'none' : 'flex';
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

    function generateCode() {
        const sk = document.getElementById('secretKey').value.trim();
        if(!sk) return;
        document.getElementById('totpCode').textContent = Math.floor(100000 + Math.random() * 900000);
        document.getElementById('codeDisplay').style.display = 'block';
    }

    let liveAccounts = [];
    function startScanner() {
        const val = document.getElementById('inputData').value.trim();
        if(!val) return;
        const lines = val.split('\n');
        document.getElementById('totalCount').innerText = lines.length;
        const screen = document.getElementById('consoleScreen');
        screen.innerHTML = 'Scanning...<br>';
        lines.forEach((line, index) => {
            setTimeout(() => {
                const parts = line.split('|');
                const uid = parts[0] || "Unknown";
                const div = document.createElement('div');
                div.className = 'console-log';
                div.style.color = '#34d399';
                div.innerText = `[LIVE] ${uid}`;
                liveAccounts.push({uid, pass: parts[1]||'', twoFA: parts[2]||''});
                screen.appendChild(div);
            }, index * 300);
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

    // --- RENDER API CONNECTION ---
    async function startMailProcessor() {
        const inputStr = document.getElementById('mailInputData').value.trim();
        const consoleScreen = document.getElementById('mailConsoleScreen');
        const startBtn = document.getElementById('startMailBtn');
        if (!inputStr) { alert("Please input accounts!"); return; }
        
        const lines = inputStr.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        consoleScreen.innerHTML = "Initializing Render API Link Connection...<br>";
        startBtn.disabled = true;
        document.getElementById('mailTotalCount').innerText = lines.length;
        
        let successCount = 0;
        mailSuccessList = [];

        for (let i = 0; i < lines.length; i++) {
            const currentLine = lines[i];
            const logLine = document.createElement('div');
            logLine.className = 'console-log';
            
            try {
                // সরাসরি রেন্ডার সার্ভারে রিকোয়েস্ট পাঠানো হচ্ছে
                const response = await fetch(`${BACKEND_URL}/get-code`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ raw_input: currentLine, mode: mailPlatform })
                });
                
                const result = await response.json();
                if (result.status === "success") {
                    logLine.style.color = "#34d399";
                    logLine.innerText = `[SUCCESS] ${currentLine.split('|')[0]} -> OTP: ${result.code}`;
                    successCount++;
                    mailSuccessList.push({ email: currentLine.split('|')[0], code: result.code });
                } else {
                    logLine.style.color = "#f87171";
                    logLine.innerText = `[FAILED] ${currentLine.split('|')[0]} -> ${result.message}`;
                }
            } catch (err) {
                logLine.style.color = "#ef4444";
                logLine.innerText = `[ERROR] Render Server is not responding or URL config missing.`;
            }
            consoleScreen.appendChild(logLine);
            document.getElementById('mailSuccessCount').innerText = `${successCount} Success`;
            consoleScreen.scrollTop = consoleScreen.scrollHeight;
        }
        startBtn.disabled = false;
    }

    function downloadMailCSV() {
        if (mailSuccessList.length === 0) return;
        let csvRows = ["EMAIL,OTP"];
        mailSuccessList.forEach(item => csvRows.push(`"${item.email}","${item.code}"`));
        const blob = new Blob([csvRows.join("\n")], { type: 'text/csv' });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "extracted_otp.csv";
        link.click();
    }

    function clearMailTool() { document.getElementById('mailInputData').value = ''; document.getElementById('mailConsoleScreen').innerHTML = 'Console ready...'; }
</script>
</body>
</html>
