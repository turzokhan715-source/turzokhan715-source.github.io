@app.route('/get-code', methods=['POST', 'OPTIONS'])
def get_code():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'CORS_Preflight_OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")
        return response, 200

    try:
        # ফ্রন্টএন্ড থেকে যেভাবে ডেটা পাঠানো হোক না কেন তা ক্যাচ করার ট্রাই করা হচ্ছে
        data = request.get_json() or request.form or {}
        
        # যদি 'raw_input' নামে ডেটা না পাওয়া যায়, তবে ব্যাকআপ হিসেবে সরাসরি ডাটা ভ্যালু বা প্রথম কী চেক করবে
        raw_input = data.get('raw_input', '')
        if not raw_input and data:
            # ফ্রন্টএন্ড যদি শুধু অবজেক্ট বা অন্য নামে ডেটা পাঠায়
            raw_input = list(data.values())[0] if isinstance(data, dict) and data.values() else ''

        raw_input = str(raw_input).strip()

        if not raw_input or '|' not in raw_input:
            response = jsonify({'status': 'error', 'message': 'Invalid input format or empty data.'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200  # ৫০০ এরর এড়াতে সাকসেস কোডে এরর মেসেজ পাঠানো হচ্ছে

        # পাইপ (|) দিয়ে ডেটা নিখুঁতভাবে আলাদা করা হচ্ছে
        parts = [p.strip() for p in raw_input.split('|') if p.strip()]
        
        if len(parts) < 3:
            response = jsonify({'status': 'error', 'message': 'Format must contain email|pass|token'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200

        email = parts[0]
        password = parts[1]
        refresh_token = parts[2]
        
        # ৪ নম্বর অংশ (client_id) না থাকলে এই স্ট্যান্ডার্ড আইডিটি নিজে থেকে বসে যাবে
        if len(parts) >= 4:
            client_id = parts[3]
        else:
            client_id = "f1e6c35b-1634-4bc0-b53d-24e526d140e6"

        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        if fb_code.isdigit():
            response = jsonify({
                'status': 'success', 
                'email': email, 
                'code': fb_code
            })
        else:
            response = jsonify({
                'status': 'error', 
                'message': fb_code
            })
            
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200

    except Exception as e:
        # কোনো অবস্থাতেই যেন রেন্ডার সার্ভার ৫০০ এরর না দেখায়, তাই নিরাপদ ক্যাচ লেয়ার
        response = jsonify({'status': 'error', 'message': f"API Safe Layer: {str(e)}"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200
