from flask import Flask, request, render_template_string
import requests # type: ignore

app = Flask(__name__)

# Simulasi "Innternal Server" yang hanya bisa di akses oleh server ini sendiri
# Di dunia nyata, ini bida berupa metada server (AWS/GCP) atau database internal.

INTERNAL_ADMIN_PANEL = "http://127.0.0.1:5000/admin-secret-area"

@app.route('/')
def index():
    return '''
        <h2>Service Checker</h2>
        <p>Masukkan URL API untuk mengecek status layanan:</p>
    <form action="/check-status" method="get">
        <input type="text" name="url" placeholder="http://api.external.com/status">
        <input type="submit" value"Check">
    </form>

'''

@app.route('/check-status')
def check_status():
    target_url = request.args.get('url')
    try:
        # KERENTANAN: Sever langsung langsung melakukan request ke URL dari user tanpa validasi
        response = requests.get(target_url, timeout=5)
        return f"<h3>Status Report for {target_url}:</h3><pre>{response.text}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin-secret-area')
def admin_area():
    # Hanya boleh diakses dari localhost (172.0.0.1)
    if request.remote_addr != '127.0.0.1':
        return "❌ AKSES DITOLAK: Hanya untuk admin internal!", 403
    return "✅ SELAMAT! Anda masuk ke panel Admin Internal. Rahasia: SSRF_IS_POWERFUL_2026"
if __name__ == '__main__':
    app.run(port=5000)