from flask import Flask, request
import requests
import socket

app = Flask(__name__)

# Daftar hitam (blacklist) alamat yang dilarang
BLACKLIST = ["127.0.0.1", "localhost", "0.0.0.0"]

@app.route('/check-status')
def check_status(): 
    target_url = request.args.get('url')

    # FIX: Cek dulu apakah target_url ada isinya atau tidak
    if not target_url:
        return "⚠️ Silakan masukkan parameter URL! Contoh: /check-status?url=http://google.com", 400

    # Sekarang aman untuk mengecek BLACKLIST
    if any(blacklisted in target_url for blacklisted in BLACKLIST):
        return "❌ DETEKSI SERANGAN: Anda mencoba mengakses area terlarang!", 403

    try:
        response = requests.get(target_url, timeout=5)
        return f"<h3>Status Report:</h3><pre>{response.text}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"
# Area rahasia yang sama seperti kemarin
@app.route('/admin-secret-area')
def admin_area():
    if request.remote_addr != '127.0.0.1':
        return "❌ AKSES DITOLAK", 403
    return "✅ BYPASS BERHASIL! Flag: BYPASS_MASTER_2026"

if __name__ == '__main__':
    app.run(port=5000)