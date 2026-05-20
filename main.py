<div id="tool-mail" class="section">
<div class="tool-wrapper">
<iframe id="iframe-mail" class="responsive-iframe" srcdoc="
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>FB & IG OTP Extractor - Responsive Pro</title>
    <script src='https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4'></script>
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'>
    <style>
        .neon-card {
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(51, 65, 85, 0.5);
            box-shadow: 0 25px 70px -10px rgba(0, 0, 0, 0.8), 0 0 30px rgba(99, 102, 241, 0.05);
            border-radius: 28px;
        }
        .neon-bracket {
            border-left: 3px solid #6366f1;
            border-right: 3px solid #6366f1;
            border-radius: 14px;
            box-shadow: inset 10px 0 15px -10px rgba(99, 102, 241, 0.1), inset -10px 0 15px -10px rgba(99, 102, 241, 0.1);
        }
        textarea::-webkit-scrollbar { width: 6px; }
        textarea::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
        textarea::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class='bg-[#030712] text-slate-200 min-h-screen flex flex-col justify-center items-center p-4 sm:p-6 font-sans select-none'>
    <div class='w-full max-w-4xl neon-card p-6 sm:p-8 min-h-[auto] md:min-h-[500px] flex flex-col justify-between transition-all duration-300'>
        <div>
            <div class='flex flex-col items-center mb-6 border-b border-slate-800 pb-5'>
                <div class='flex items-center space-x-3 text-2xl sm:text-3xl font-black tracking-tight'>
                    <i class='fas fa-cube text-indigo-500 animate-pulse'></i>
                    <h1 class='bg-gradient-to-r from-white via-slate-200 to-indigo-400 bg-clip-text text-transparent'>FB & IG OTP Extractor</h1>
                </div>
                <p class='text-[10px] text-indigo-400/70 font-bold uppercase tracking-widest mt-1'>Cloud Automation Hub</p>
                <div id='modeBadge' class='mt-3 inline-flex items-center space-x-1.5 bg-amber-500/10 border border-amber-500/30 px-5 py-1 rounded-full shadow-sm'>
                    <i class='fas fa-shield-alt text-amber-400 text-[10px]'></i>
                    <span id='badgeText' class='text-[10px] font-black text-amber-400 tracking-wider uppercase'>Facebook Priority Mode</span>
                </div>
            </div>
            <div class='grid grid-cols-1 md:grid-cols-2 gap-6 items-start'>
                <div class='space-y-5'>
                    <div class='bg-slate-950 p-1.5 rounded-2xl flex space-x-1.5 border border-slate-800/80'>
                        <button onclick='setPlatform(&quot;fb&quot;)' id='fbBtn' class='flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-[11px] sm:text-xs font-black py-3 px-3 rounded-xl flex justify-center items-center transition-all duration-300 shadow-lg cursor-pointer'>
                            <i class='fab fa-facebook mr-1.5 text-xs'></i> Facebook <span class='ml-1 bg-amber-400 text-slate-950 text-[9px] font-black px-1.5 py-0.5 rounded-md'>1st</span>
                        </button>
                        <button onclick='setPlatform(&quot;ig&quot;)' id='igBtn' class='flex-1 bg-transparent text-slate-500 hover:text-slate-300 text-[11px] sm:text-xs font-bold py-3 px-3 rounded-xl flex justify-center items-center transition-all duration-300 cursor-pointer'>
                            <i class='fab fa-instagram mr-1.5 text-xs'></i> Instagram <span class='ml-1 bg-slate-800 text-slate-400 text-[9px] font-bold px-1.5 py-0.5 rounded-md'>2nd</span>
                        </button>
                    </div>
                    <div class='flex space-x-2'>
                        <button onclick='loadAccount(1)' class='flex-1 bg-slate-900/60 hover:bg-slate-800/80 text-slate-400 hover:text-white text-xs font-bold py-2.5 px-3 rounded-xl border border-slate-800 transition cursor-pointer flex justify-center items-center'>
                            <i class='fas fa-user-shield mr-1.5 text-blue-400'></i> Account 1
                        </button>
                        <button onclick='loadAccount(2)' class='flex-1 bg-slate-900/60 hover:bg-slate-800/80 text-slate-400 hover:text-white text-xs font-bold py-2.5 px-3 rounded-xl border border-slate-800 transition cursor-pointer flex justify-center items-center'>
                            <i class='fas fa-user-shield mr-1.5 text-purple-400'></i> Account 2
                        </button>
                    </div>
                    <div id='inputBracket' class='relative px-4 neon-bracket'>
                        <label class='block text-[11px] font-black text-indigo-300 tracking-wider mb-2 uppercase flex items-center'>
                            <i class='fas fa-terminal mr-1.5 text-indigo-400'></i> Input Account Data Line:
                        </label>
                        <textarea id='rawData' class='w-full h-32 bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-xs font-mono text-cyan-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-inner transition resize-none' placeholder='email|password|refresh_token|client_id'></textarea>
                    </div>
                    <div class='flex space-x-2'>
                        <button onclick='getOtpCode()' id='actionBtn' class='flex-[2] bg-indigo-600 hover:bg-indigo-500 text-white font-black py-3.5 px-4 rounded-xl border border-indigo-500/30 transition-all duration-200 flex justify-center items-center text-xs tracking-wider uppercase shadow-md cursor-pointer'>
                            <span id='btnText'><i class='fas fa-bolt mr-2 text-white'></i> Extract OTP Code</span>
                        </button>
                        <button onclick='clearAll()' class='flex-1 bg-slate-900/40 hover:bg-slate-900 text-slate-500 hover:text-red-400 font-bold py-3.5 px-4 rounded-xl border border-slate-800/60 transition flex justify-center items-center text-xs uppercase cursor-pointer'>
                            <i class='fas fa-eraser mr-1.5'></i> Clear
                        </button>
                    </div>
                </div>
                <div class='space-y-5 h-full flex flex-col justify-between'>
                    <div id='detectInfo' class='px-4 border-l-3 border-r-3 border-indigo-500 flex justify-between items-center bg-slate-950/60 py-4 rounded-xl border border-slate-800/50 min-h-[96px]'>
                        <div class='max-w-[200px] sm:max-w-[240px]'>
                            <div class='flex items-center text-xs font-black text-indigo-300 tracking-wide'>
                                <i id='statusDot' class='fas fa-circle-notch text-indigo-400 mr-1.5 text-xs'></i>
                                <span id='successMsg'>System Standing By</span>
                            </div>
                            <div class='text-[11px] text-slate-500 mt-2 font-mono break-all leading-tight'>
                                Target: <span id='displayEmail' class='text-slate-400 font-bold'>No Account Loaded</span>
                            </div>
                        </div>
                        <button onclick='copyEmail()' id='copyEmailBtn' class='bg-indigo-950/80 text-indigo-400 hover:bg-indigo-900 hover:text-indigo-200 border border-indigo-800/50 px-3 py-2.5 rounded-xl text-[11px] font-black transition flex items-center shadow-md shrink-0 cursor-pointer'>
                            <i class='fas fa-copy mr-1 text-xs'></i> Copy Email
                        </button>
                    </div>
                    <div class='bg-slate-950 p-5 rounded-xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-inner'>
                        <div class='text-center sm:text-left'>
                            <span id='codeTitle' class='text-[9px] font-black text-slate-500 block mb-1 uppercase tracking-widest'>Verification Code:</span>
                            <span id='otpOutput' class='text-4xl sm:text-5xl font-black tracking-widest text-slate-700 font-mono transition-all'>XXXXXX</span>
                        </div>
                        <button onclick='copyCode()' class='w-full sm:w-auto bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-3 rounded-xl text-xs font-black transition shadow-lg flex justify-center items-center border border-indigo-500/30 cursor-pointer'>
                            <i class='fas fa-clone mr-1.5'></i> Copy Code
                        </button>
                    </div>
                    <div class='text-[10px] text-slate-600 font-mono text-center md:text-right pt-2'>
                        <span>● Live Server Connection: Secured</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        let currentPlatform = 'fb';
        const account1_data = 'email1@outlook.com|pass1|refresh_token_1|client_id_1';
        const account2_data = 'email2@outlook.com|pass2|refresh_token_2|client_id_2';
        const API_URL = 'https://toll-376d.onrender.com/get-code';

        document.getElementById('rawData').addEventListener('input', function(e) {
            const val = e.target.value.trim();
            document.getElementById('displayEmail').innerText = val.includes('|') ? val.split('|')[0] : 'No Account Loaded';
        });

        function setPlatform(platform) {
            currentPlatform = platform;
            const fbBtn = document.getElementById('fbBtn');
            const igBtn = document.getElementById('igBtn');
            const modeBadge = document.getElementById('modeBadge');
            const badgeText = document.getElementById('badgeText');
            if (platform === 'fb') {
                fbBtn.className = 'flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-[11px] sm:text-xs font-black py-3 px-3 rounded-xl flex justify-center items-center transition-all duration-300 shadow-lg cursor-pointer';
                igBtn.className = 'flex-1 bg-transparent text-slate-500 hover:text-slate-300 text-[11px] sm:text-xs font-bold py-3 px-3 rounded-xl flex justify-center items-center transition-all duration-300 cursor-pointer';
                modeBadge.className = 'mt-3 inline-flex items-center space-x-1.5 bg-amber-500/10 border border-amber-500/30 px-5 py-1 rounded-full shadow-sm';
                badgeText.innerText = 'Facebook Priority Mode';
            } else {
                igBtn.className = 'flex-1 bg-gradient-to-r from-pink-600 to-rose-600 text-white text-[11px] sm:text-xs font-black py-3 px-3 rounded-xl flex justify-center items-center transition-all duration-300 shadow-lg cursor-pointer';
                fbBtn.className = 'flex-1 bg-transparent text-slate-500 hover:text-slate-300 text-[11px] sm:text-xs font-bold py-3 px-3 rounded-xl flex justify-center items-center transition-all duration-300 cursor-pointer';
                modeBadge.className = 'mt-3 inline-flex items-center space-x-1.5 bg-pink-500/10 border border-pink-500/30 px-5 py-1 rounded-full shadow-sm';
                badgeText.innerText = 'Instagram Priority Mode';
            }
        }

        function loadAccount(num) {
            const field = document.getElementById('rawData');
            if(num === 1) field.value = account1_data;
            if(num === 2) field.value = account2_data;
            document.getElementById('displayEmail').innerText = field.value.split('|')[0];
            document.getElementById('successMsg').innerText = 'Account ' + num + ' Loaded';
        }

        function clearAll() {
            document.getElementById('rawData').value = '';
            document.getElementById('displayEmail').innerText = 'No Account Loaded';
            document.getElementById('otpOutput').innerText = 'XXXXXX';
            document.getElementById('otpOutput').className = 'text-4xl sm:text-5xl font-black tracking-widest text-slate-700 font-mono transition-all';
            document.getElementById('successMsg').innerText = 'System Standing By';
            resetButton();
        }

        function getOtpCode() {
            const rawData = document.getElementById('rawData').value.trim();
            const actionBtn = document.getElementById('actionBtn');
            const btnText = document.getElementById('btnText');
            const otpOutput = document.getElementById('otpOutput');
            const successMsg = document.getElementById('successMsg');
            const statusDot = document.getElementById('statusDot');

            if (!rawData) {
                successMsg.innerText = 'Please input credentials first!';
                return;
            }

            actionBtn.disabled = true;
            actionBtn.className = 'flex-[2] bg-slate-950 text-slate-600 font-black py-3.5 px-4 rounded-xl border border-slate-900/40 flex justify-center items-center cursor-not-allowed text-xs tracking-wider uppercase';
            btnText.innerHTML = '<i class="fas fa-circle-notch animate-spin mr-2 text-indigo-500"></i> Connecting Mail Box...';
            statusDot.className = 'fas fa-circle-notch animate-spin text-indigo-500 mr-1.5 text-xs';
            successMsg.innerText = 'Extracting OTP Engine Core...';
            otpOutput.innerText = 'SEARCHING';
            otpOutput.className = 'text-xl sm:text-2xl font-black text-indigo-400 font-mono tracking-normal animate-pulse';

            // 🎯 JSON POST ফিক্সড রিকোয়েস্ট ব্লক
            fetch(API_URL, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({ 'raw_input': rawData })
            })
            .then(res => {
                if (!res.ok) throw new Error('Server Error Connection Failed');
                return res.json();
            })
            .then(data => {
                resetButton();
                if (data.status === 'success') {
                    otpOutput.innerText = data.code;
                    otpOutput.className = 'text-4xl sm:text-5xl font-black tracking-widest text-emerald-400 font-mono transition-all animate-bounce';
                    successMsg.innerText = 'Code Extracted Successfully';
                    statusDot.className = 'fas fa-check-circle text-emerald-400 mr-1.5 text-xs';
                } else {
                    otpOutput.innerText = 'ERROR';
                    otpOutput.className = 'text-2xl font-black text-rose-500 font-mono tracking-normal';
                    successMsg.innerText = data.message || 'Failed to Parse Stream';
                    statusDot.className = 'fas fa-times-circle text-rose-500 mr-1.5 text-xs';
                }
            })
            .catch(err => {
                resetButton();
                otpOutput.innerText = 'CORS ERR';
                otpOutput.className = 'text-xl font-black text-amber-500 font-mono tracking-normal';
                successMsg.innerText = 'CORS Blocked or Endpoint Offline.';
                statusDot.className = 'fas fa-exclamation-triangle text-amber-500 mr-1.5 text-xs';
            });
        }

        function resetButton() {
            const actionBtn = document.getElementById('actionBtn');
            const btnText = document.getElementById('btnText');
            actionBtn.disabled = false;
            actionBtn.className = 'flex-[2] bg-indigo-600 hover:bg-indigo-500 text-white font-black py-3.5 px-4 rounded-xl border border-indigo-500/30 transition-all duration-200 flex justify-center items-center text-xs tracking-wider uppercase shadow-md cursor-pointer';
            btnText.innerHTML = '<i class="fas fa-bolt mr-2 text-white"></i> Extract OTP Code';
        }

        function copyEmail() {
            const text = document.getElementById('rawData').value.split('|')[0];
            if(text) { navigator.clipboard.writeText(text); alert('Email Copied: ' + text); }
        }

        function copyCode() {
            const code = document.getElementById('otpOutput').innerText;
            if(code && code !== 'XXXXXX' && code !== 'ERROR' && code !== 'CORS ERR') { 
                navigator.clipboard.writeText(code);
                alert('OTP Code Copied: ' + code); 
            }
        }
    </script>
</body>
</html>
"></iframe>
</div>
</div>

<div id="tool-2fa" class="section">
<div class="tool-wrapper">
<iframe id="iframe-2fa" class="responsive-iframe" srcdoc="
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');
        :root {
            --bg: rgb(10, 11, 18);
            --card-bg: rgb(21, 23, 37);
            --input-bg: rgb(15, 17, 26);
            --primary: rgb(168, 85, 247);
            --primary-glow: rgba(168, 85, 247, 0.3);
            --btn-grad: linear-gradient(135deg, rgb(168, 85, 247), rgb(59, 130, 246));
            --text-gray: rgb(148, 163, 184);
            --border: rgba(255, 255, 255, 0.05);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: #fff; min-height: 100vh; padding: 20px 12px; display: flex; justify-content: center; align-items: flex-start; }
        .container { max-width: 520px; width: 100%; margin: 0 auto; }
        .main-card { background: var(--card-bg); border-radius: 24px; padding: 30px 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); border: 1px solid var(--border); margin-bottom: 24px; }
        .card-header { text-align: center; margin-bottom: 24px; }
        .card-header h1 { font-size: clamp(1.3rem, 4vw, 1.7rem); font-weight: 800; background: linear-gradient(135deg, #fff 40%, var(--text-gray)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; line-height: 1.3; }
        .card-header p { font-size: 0.8rem; color: var(--text-gray); }
        .input-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 10px; color: #e2e8f0; font-size: 0.875rem; }
        input[type='text'] { width: 100%; padding: 14px; border: 2px solid rgb(30, 41, 59); border-radius: 14px; font-size: 0.95rem; color: #fff; background: var(--input-bg); font-family: 'Courier New', monospace; font-weight: 600; }
        input[type='text']:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 20px var(--primary-glow); }
        button { width: 100%; padding: 14px; background: var(--btn-grad); color: #fff; border: none; border-radius: 14px; font-size: 0.95rem; font-weight: 700; cursor: pointer; transition: all 0.25s ease; display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 16px; box-shadow: 0 8px 24px rgba(168, 85, 247, 0.3); }
        button:hover { transform: translateY(-2px); opacity: 0.95; }
        .code-display { background: linear-gradient(135deg, rgb(17, 24, 39) 0%, rgb(3, 7, 18) 100%); border: 2px solid rgb(30, 41, 59); border-radius: 14px; padding: 20px; text-align: center; margin-bottom: 12px; }
        .code-label { font-size: 0.8rem; color: var(--primary); font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
        .totp-code { font-size: clamp(1.5rem, 5vw, 2rem); font-weight: 800; color: rgb(52, 211, 153); font-family: 'Courier New', monospace; letter-spacing: 4px; }
        .copy-hint { text-align: center; color: rgb(52, 211, 153); font-weight: 700; font-size: 0.85rem; opacity: 0; transition: opacity 0.3s; }
        .copy-hint.show { opacity: 1; }
        .history-card { background: var(--card-bg); border-radius: 24px; padding: 24px 20px; border: 1px solid var(--border); max-height: 350px; display: flex; flex-direction: column; width: 100%; }
        .history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .history-header h2 { font-size: 1.05rem; color: #f1f5f9; font-weight: 800; }
        #historyCount { font-size: 0.7rem; color: rgb(192, 132, 252); background: rgba(168, 85, 247, 0.15); padding: 4px 10px; border-radius: 20px; }
        .history-list { overflow-y: auto; padding-right: 4px; }
        .history-list::-webkit-scrollbar { width: 6px; }
        .history-list::-webkit-scrollbar-thumb { background: rgb(30, 41, 59); border-radius: 10px; }
        .empty-state { text-align: center; color: var(--text-gray); padding: 30px 10px; font-style: italic; font-size: 0.85rem; }
        .history-item { padding: 12px; background: rgb(17, 23, 38); border-radius: 14px; margin-bottom: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: center; border: 1px solid rgba(255, 255, 255, 0.03); }
        .history-info { display: flex; flex-direction: column; gap: 4px; }
        .history-secret { font-size: 0.75rem; color: #cbd5e1; font-family: monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 600; }
        .history-time { font-size: 0.65rem; color: var(--text-gray); }
        .history-actions { display: flex; justify-content: flex-end; gap: 8px; }
        .btn-action { width: auto; padding: 8px 12px; font-size: 0.75rem; border-radius: 8px; margin-bottom: 0; box-shadow: none; }
        .btn-copy { background: rgba(168, 85, 247, 0.1); color: var(--primary); border: 1px solid rgba(168, 85, 247, 0.2); }
        .btn-copy:hover { background: rgba(168, 85, 247, 0.2); }
        .btn-delete { background: rgba(239, 68, 68, 0.1); color: rgb(239, 68, 68); border: 1px solid rgba(239, 68, 68, 0.2); }
        .btn-delete:hover { background: rgba(239, 68, 68, 0.2); }
    </style>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/jsqrcode/1.0.2/qr_packed.js'></script>
</head>
<body>
    <div class='container'>
        <div class='main-card'>
            <div class='card-header'>
                <h1>2FA Authentication Portal</h1>
                <p>Generate secure high-speed TOTP arrays instantly</p>
            </div>
            <div class='input-group'>
                <label for='secretInput'>Enter 2FA Secret Key:</label>
                <input type='text' id='secretInput' placeholder='Paste your secret 2FA code here...' autocomplete='off'>
            </div>
            <button onclick='generate2FA()'><i class='fas fa-sync-alt'></i> Generate 2FA Code</button>
            <div class='code-display' onclick='copyGeneratedCode()' style='cursor: pointer;'>
                <div class='code-label'>Current Active Token</div>
                <div class='totp-code' id='totpOutput'>------</div>
            </div>
            <div class='copy-hint' id='copyHint'>✓ Token copied to clipboard successfully!</div>
        </div>
        <div class='history-card'>
            <div class='history-header'>
                <h2>Active Session Log</h2>
                <span id='historyCount'>0 Keys</span>
            </div>
            <div class='history-list' id='historyList'>
                <div class='empty-state' id='emptyState'>No keys processed in this active pool sequence.</div>
            </div>
        </div>
    </div>
    <script>
        let sessionLog = [];
        function dec2hex(s) { return (s < 15.5 ? '0' : '') + Math.round(s).toString(16); }
        function hex2dec(s) { return parseInt(s, 16); }
        function base32tohex(base32) {
            let b32chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
            let bits = '';
            let hex = '';
            base32 = base32.replace(/ /g, '').toUpperCase();
            for (let i = 0; i < base32.length; i++) {
                let val = b32chars.indexOf(base32.charAt(i));
                if (val === -1) continue;
                bits += leftpad(val.toString(2), 5, '0');
            }
            for (let i = 0; i + 4 <= bits.length; i += 4) {
                let chunk = bits.substr(i, 4);
                hex = hex + parseInt(chunk, 2).toString(16);
            }
            return hex;
        }
        function leftpad(str, len, pad) {
            if (len + 1 >= str.length) { str = Array(len + 1 - str.length).join(pad) + str; }
            return str;
        }
        function getTOTP(secret) {
            try {
                secret = secret.replace(/\s/g, '');
                if(!secret) return 'INVALID';
                let hexSecret = base32tohex(secret);
                if (!hexSecret) return 'ERROR';
                let epoch = Math.round(new Date().getTime() / 1000.0);
                let time = leftpad(dec2hex(Math.floor(epoch / 30)), 16, '0');
                let hmacObj = new HMAC();
                let hmac = hmacObj.hex_hmac_sha1(time, hexSecret);
                let offset = hex2dec(hmac.substr(hmac.length - 1));
                let otp = (hex2dec(hmac.substr(offset * 2, 8)) & hex2dec('7fffffff')) + '';
                otp = (otp).substr(otp.length - 6, 6);
                return leftpad(otp, 6, '0');
            } catch (err) { return 'ERROR'; }
        }
        function generate2FA() {
            let input = document.getElementById('secretInput').value.trim();
            if(!input) return alert('Please enter a valid 2FA Secret Key');
            let cleanKey = input;
            if(input.includes('secret=')) {
                let urlParams = new URLSearchParams(input.split('?')[1]);
                cleanKey = urlParams.get('secret') || input;
            }
            let code = getTOTP(cleanKey);
            if(code === 'ERROR' || code === 'INVALID') return alert('Failed to parse Secret. Check base32 configuration format.');
            document.getElementById('totpOutput').innerText = code;
            addLogItem(cleanKey, code);
        }
        function addLogItem(secret, code) {
            document.getElementById('emptyState').style.display = 'none';
            let timestamp = new Date().toLocaleTimeString();
            sessionLog.unshift({ secret: secret, code: code, time: timestamp });
            renderLog();
        }
        function renderLog() {
            let list = document.getElementById('historyList');
            let items = sessionLog.map((item, index) => `
                <div class='history-item'>
                    <div class='history-info'>
                        <span class='history-secret'>${item.secret}</span>
                        <span class='history-time'>Generated at: ${item.time} [Token: <b>${item.code}</b>]</span>
                    </div>
                    <div class='history-actions'>
                        <button class='btn-action btn-copy' onclick='copyText(&quot;${item.code}&quot;)'><i class='fas fa-copy'></i> Code</button>
                        <button class='btn-action btn-delete' onclick='deleteLog(${index})'><i class='fas fa-trash'></i></button>
                    </div>
                </div>
            `).join('');
            list.innerHTML = sessionLog.length ? items : `<div class='empty-state' id='emptyState'>No keys processed in this active pool sequence.</div>`;
            document.getElementById('historyCount').innerText = sessionLog.length + ' Keys';
        }
        function deleteLog(index) {
            sessionLog.splice(index, 1);
            renderLog();
        }
        function copyText(str) {
            navigator.clipboard.writeText(str);
            let hint = document.getElementById('copyHint');
            hint.className = 'copy-hint show';
            setTimeout(() => { hint.className = 'copy-hint'; }, 2000);
        }
        function copyGeneratedCode() {
            let code = document.getElementById('totpOutput').innerText;
            if(code && code !== '------') copyText(code);
        }
        // Minimal SHA-1 implementation block for inline compatibility frameworks
        function HMAC() {
            this.hex_hmac_sha1 = function(key, data) { return core_hmac_sha1(key, data); };
            function core_hmac_sha1(key, data) {
                let bkey = hash2bin(key);
                let bdata = hash2bin(data);
                let ipad = Array(16), opad = Array(16);
                for(let i=0; i<16; i++) { ipad[i] = bkey[i] ^ 0x36363636; opad[i] = bkey[i] ^ 0x5C5C5C5C; }
                let hash = core_sha1(ipad.concat(bdata), 512 + bdata.length * 32);
                return bin2hex(core_sha1(opad.concat(hash), 512 + 160));
            }
            function core_sha1(x, len) {
                x[len >> 5] |= 0x80 << (24 - len % 32); x[((len + 64 >> 9) << 4) + 15] = len;
                let w = Array(80), a =  1732584193, b = -271733879, c = -1732584194, d =  271733878, e = -1009454052;
                for(let i = 0; i < x.length; i += 16) {
                    let olda = a, oldb = b, oldc = c, oldd = d, olde = e;
                    for(let j = 0; j < 80; j++) {
                        if(j < 16) w[j] = x[i + j];
                        else w[j] = rol(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1);
                        let t = safe_add(safe_add(rol(a, 5), sha1_ft(j, b, c, d)), safe_add(safe_add(e, w[j]), sha1_kt(j)));
                        e = d; d = c; c = rol(b, 30); b = a; a = t;
                    }
                    a = safe_add(a, olda); b = safe_add(b, oldb); c = safe_add(c, oldc); d = safe_add(d, oldd); e = safe_add(e, olde);
                }
                return Array(a, b, c, d, e);
            }
            function sha1_ft(t, b, c, d) { if(t < 20) return (b & c) | ((~b) & d); if(t < 40) return b ^ c ^ d; if(t < 60) return (b & c) | (b & d) | (c & d); return b ^ c ^ d; }
            function sha1_kt(t) { return (t < 20) ?  1518500249 : (t < 40) ?  1859775393 : (t < 60) ? -1894007588 : -899497514; }
            function safe_add(x, y) { let lsw = (x & 0xFFFF) + (y & 0xFFFF), msw = (x >> 16) + (y >> 16) + (lsw >> 16); return (msw << 16) | (lsw & 0xFFFF); }
            function rol(num, cnt) { return (num << cnt) | (num >>> (32 - cnt)); }
            function bin2hex(binarray) { let hex_tab = '0123456789abcdef', str = ''; for(let i = 0; i < binarray.length * 4; i++) { str += hex_tab.charAt((binarray[i] >> ((3-i%4)*8+4)) & 0xF) + hex_tab.charAt((binarray[i] >> ((3-i%4)*8)) & 0xF); } return str; }
            function hash2bin(hexStr) { let words = [], i = 0; while (i < hexStr.length) { words.push(parseInt(hexStr.substr(i, 8), 16)); i += 8; } return words; }
        }
    </script>
</body>
</html>
"></iframe>
</div>
</div>

<script>
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => { section.classList.remove('active'); });
    const targetSection = document.getElementById(sectionId);
    if(targetSection) {
        targetSection.classList.add('active');
    }

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === sectionId) {
            link.classList.add('active');
        }
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
</script>
</body>
</html>
