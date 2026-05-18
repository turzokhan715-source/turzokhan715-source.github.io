import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Complete dynamic cross-origin rule mapping
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/get-code', methods=['POST', 'OPTIONS'])
def get_code():
    # Preflight routing configuration block
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'CORS_ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No input payload delivered."}), 400

        raw_input = data.get("raw_input", "").strip()
        if not raw_input:
            return jsonify({"status": "error", "message": "The account credential field cannot be blank."}), 400

        # Structural array string breakdown
        parts = raw_input.split('|')
        email = parts[0].strip() if len(parts) > 0 else ""
        password = parts[1].strip() if len(parts) > 1 else ""
        refresh_token = parts[2].strip() if len(parts) > 2 else ""

        # ----------------------------------------------------
        # 🛠️ APNAR API CALL / IMAP CODE EKHANE INTEGRATE KORUN
        # ----------------------------------------------------
        extracted_otp_code = "482015"  # Actual extracted code value assignment variable

        return jsonify({
            "status": "success",
            "verification_code": extracted_otp_code,
            "email": email
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server process fault: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
