import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 🌐 ব্রাউজারের CORS কানেকশন ব্লক সমস্যা দূর করার জন্য
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/get-code',彻 methods=['POST'])
def get_code():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received!"}), 400
            
        raw_input = data.get("raw_input", "").strip()
        mode = data.get("mode", "facebook").strip()

        if not raw_input:
            return jsonify({"status": "error", "message": "Input data is empty!"}), 400

        # 📋 পাইপ (|) সিম্বল দিয়ে ডেটা আলাদা করা
        parts = raw_input.split('|')
        email = parts[0].strip() if len(parts) > 0 else ""
        password = parts[1].strip() if len(parts) > 1 else ""
        token = parts[2].strip() if len(parts) > 2 else ""
        uid = parts[3].strip() if len(parts) > 3 else ""

        # 🔍 মোড অনুযায়ী আপনার ওটিপি এক্সট্রাকশন লজিক এখানে কাজ করবে
        extracted_otp = ""
        
        if mode == "facebook":
            # 🔵 এখানে আপনার ফেসবুক ওটিপি বের করার আসল স্ক্রিপ্ট/লজিক বসাবেন
            extracted_otp = "FB-123456"  # টেস্ট ডামি ওটিপি
            
        elif mode == "instagram":
            # 🔮 এখানে আপনার ইনস্টাগ্রাম ওটিপি বের করার আসল স্ক্রিপ্ট/লজিক বসাবেন
            extracted_otp = "IG-654321"  # টেস্ট ডামি ওটিপি
        else:
            return jsonify({"status": "error", "message": "Invalid platform mode!"}), 400

        # সবকিছু সফল হলে ফ্রন্টএন্ডে পাঠানো
        return jsonify({
            "status": "success",
            "code": extracted_otp,
            "email": email,
            "uid": uid
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    # রেন্ডার পোর্টের সাথে ম্যাচ করানোর জন্য
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
