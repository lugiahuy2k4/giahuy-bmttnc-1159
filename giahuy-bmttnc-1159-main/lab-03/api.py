from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
from cipher.ecc import ECCipher

app = Flask(__name__)

# RSA CIPHER ALGORITHM
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'RSA keys generated successfully!'})

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    message = data.get('message')
    key_type = data.get('key_type')
    private_key, public_key = rsa_cipher.load_keys()
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type!'}), 400
    try:
        encrypted_message = rsa_cipher.encrypt(message, key)
        encrypted_hex = encrypted_message.hex()
        return jsonify({'encrypted_message': encrypted_hex})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data.get('ciphertext')
    key_type = data.get('key_type')
    private_key, public_key = rsa_cipher.load_keys()
    if key_type == 'public':
        key = public_key
    elif key_type == 'private':
        key = private_key
    else:
        return jsonify({'error': 'Invalid key type!'}), 400
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
        decrypted_message = rsa_cipher.decrypt(ciphertext, key)
        if decrypted_message is False:
            return jsonify({'error': 'Decryption failed!'}), 400
        return jsonify({'decrypted_message': decrypted_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data.get('message')
    private_key, _ = rsa_cipher.load_keys()
    try:
        signature = rsa_cipher.sign(message, private_key)
        signature_hex = signature.hex()
        return jsonify({'signature': signature_hex})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data.get('message')
    signature_hex = data.get('signature')
    _, public_key = rsa_cipher.load_keys()
    try:
        signature = bytes.fromhex(signature_hex)
        is_verified = rsa_cipher.verify(message, signature, public_key)
        return jsonify({'is_verified': is_verified})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ECC CIPHER ALGORITHM
ecc_cipher = ECCipher()

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'ECC keys generated successfully!'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data.get('message')
    private_key, _ = ecc_cipher.load_keys()
    try:
        signature = ecc_cipher.sign(message, private_key)
        signature_hex = signature.hex()
        return jsonify({'signature': signature_hex})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data.get('message')
    signature_hex = data.get('signature')
    _, public_key = ecc_cipher.load_keys()
    try:
        signature = bytes.fromhex(signature_hex)
        is_verified = ecc_cipher.verify(message, signature, public_key)
        return jsonify({'is_verified': is_verified})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)