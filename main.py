import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# গ্লোবাল CORS অন করা হলো এবং সব রিকোয়েস্ট ওপেন করা হলো
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/get-code', methods=['POST', 'OPTIONS'])
def get_code():
    # 🌟 ব্রাউজারের প্রি-ফ্লাইট (OPTIONS) চেক ম্যানুয়ালি হ্যান্ডেল করা হলো (CORS Fix)
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
            return jsonify({"status": "error", "message": "Input field cannot be blank."}), 400

        # পাইপ (|) সিম্বল দিয়ে ডেটা আলাদা করা
        parts = raw_input.split('|')
        email = parts[0].strip() if len(parts) > 0 else ""
        password = parts[1].strip() if len(parts) > 1 else ""
        refresh_token = parts[2].strip() if len(parts) > 2 else ""

        # ----------------------------------------------------
        # 🛠️ আপনার আসল ইমেইল ও ওটিপি বের করার কোডটি এখানে বসবে
        # ----------------------------------------------------
        extracted_otp_code = "482015"  # উদাহরণ হিসেবে ডামি কোড পাঠানো হলো

        # রেসপন্সের সাথেও CORS হেডার যুক্ত করা হলো নিশ্চিত করার জন্য
        response = jsonify({
            "status": "success",
            "verification_code": extracted_otp_code,
            "email": email
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except Exception as e:
        response = jsonify({"status": "error", "message": f"Server error: {str(e)}"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
