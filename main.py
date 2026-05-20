@app.route('/get-code', methods=['POST'])
def get_code():
    try:
        data = request.get_json() or {}
        raw_input = data.get('raw_input', '').strip()

        if not raw_input:
            return jsonify({'status': 'error', 'message': 'Input empty.'}), 400

        detected_email = extract_email_from_string(raw_input)
        if not detected_email:
            return jsonify({'status': 'error', 'message': 'No valid email found in data.'}), 400

        # পাইপ (|) দিয়ে ডেটা নিখুঁতভাবে আলাদা করা হচ্ছে
        parts = [p.strip() for p in raw_input.split('|') if p.strip()]
        
        # কমপক্ষে ৩টি অংশ (ইমেইল, পাসওয়ার্ড, টোকেন) থাকতে হবে
        if len(parts) < 3:
            return jsonify({'status': 'error', 'message': 'Format must be email|pass|token'}), 400

        email = detected_email
        password = parts[1]
        refresh_token = parts[2]
        
        # যদি ইনপুটে ৪ নম্বর অংশ (client_id) না থাকে, তবে এই আইডিটি নিজে থেকে বসে যাবে
        if len(parts) >= 4:
            client_id = parts[3]
        else:
            client_id = "f1e6c35b-1634-4bc0-b53d-24e526d140e6" 

        # ওটিপি ইঞ্জিনে ডেটা পাঠানো হচ্ছে
        fb_code = extract_fb_code_via_api(email, refresh_token, client_id)

        if fb_code.isdigit():
            return jsonify({
                'status': 'success', 
                'email': email, 
                'code': fb_code
            }), 200
        else:
            return jsonify({
                'status': 'error', 
                'message': fb_code
            }), 200

    except Exception as e:
        # ইনপুট কম হলেও কোড যেন ক্র্যাশ না করে, তাই এই সেফটি লেয়ার
        return jsonify({'status': 'error', 'message': f"Server error: {str(e)}"}), 500
