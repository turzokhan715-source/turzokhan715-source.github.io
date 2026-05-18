import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 🌐 ব্রাউজারের CORS কানেকশন ব্লক সমস্যা দূর করার জন্য
CORS(app, resources={r"/*": {"origins": "*"}})

# 🎯 রেন্ডারের ডেপ্লয়মেন্ট এরর (404) ঠিক করার জন্য মেইন রুট
@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({
        "status": "online",
        "message": "OTP Extractor Backend is Running Successfully!"
    }), 200

# 🎯 স্ট্রিংয়ের ভেতর থেকে নিখুঁতভাবে ইমেইল খুঁজে বের করার রেজেক্স ফাংশন
def extract_email(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    return match.group(0).strip() if match else None

@app.route('/get-code', methods=['POST'])
def get_code():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received!"}), 400

        raw_input = data.get("raw_input", "").strip()
        mode = data.get("mode", "facebook").strip()

        if not raw_input:
            return jsonify({"status": "error", "message": "Input data is empty!"}), 400

        # 🔍 স্মার্টলি আসল ইমেইল বের করা হচ্ছে
        detected_email = extract_email(raw_input)
        
        if not detected_email:
            return jsonify({"status": "error", "message": "No valid email found in data!"}), 400

        # 📋 পাইপ (|) দিয়ে বাকি ডাটা আলাদা করা (যদি পাসওয়ার্ড বা অন্য কিছু লাগে)
        parts = raw_input.split('|')
        password = parts[1].strip() if len(parts) > 1 else ""
        token = parts[2].strip() if len(parts) > 2 else ""

        # =========================================================
        # 🔥 এখানে আপনার OTP বা কোড বের করার আসল লজিকটি কাজ করবে
        # =========================================================
        
        # আপনার স্ক্রিপ্টের আসল ওটিপি বের করার পর এই '123456' এর জায়গায় পাস করে দিবেন:
        extracted_otp = "123456" 

        return jsonify({
            "status": "success",
            "email": detected_email,
            "code": extracted_otp,
            "message": "OTP fetched successfully!"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 🚀 রেন্ডারের ডায়নামিক পোর্ট ডিটেক্ট করার জন্য
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
