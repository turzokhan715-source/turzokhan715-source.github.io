<div id="page-mail" class="page">
    <div class="tool-panel">
        <textarea id="mailInputData" placeholder="Paste your Email accounts or tokens here..."></textarea>
        
        <div class="action-row">
            <button class="btn-start-engine" id="startMailBtn" onclick="startMailProcessor()">Start Mail Engine</button>
            <button class="btn-clear-engine" onclick="clearMailTool()">Clear</button>
        </div>

        <div class="console-box" id="mailConsoleScreen" style="background: #03050a; color: #38bdf8;">Console ready for Mail Server Engine...</div>

        <div class="mail-status-container">
            <div class="mail-stats-flex">
                <div class="mail-badge">
                    <span class="mail-num" id="countProcessed" style="color: #fff;">0</span>
                    <span class="mail-lbl">Processed</span>
                </div>
                <div class="mail-badge">
                    <span class="mail-num" id="countSuccess" style="color: #3b82f6;">0</span>
                    <span class="mail-lbl" style="color: #3b82f6;">Success</span>
                </div>
            </div>
            <button class="btn-download-mail" onclick="downloadMailCSV()">Download Extracted Data</button>
        </div>
    </div>
</div>
