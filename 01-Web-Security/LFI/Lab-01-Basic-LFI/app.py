from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Lokasi folder dokumentasi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")

@app.route('/')
def index():
    return '''
        <h2>Documentation Viewer</h2>
        <p>Pilih file untuk dibaca:</p>
        <ul>
            <li><a href="/view?file=intro.txt">Introduction</a></li>
            <li><a href="/view?file=setup.txt">Setup Guie</a></li>
        </ul>
    '''

@app.route('/view')
def view_file():
    filename = request.args.get('file')
    
    # 1. CEK: Jika parameter 'file' kosong, jangan lanjut
    if not filename:
        return "⚠️ Masukkan nama file! Contoh: /view?file=intro.txt", 400
    
    # 2. GABUNGKAN: Membuat path lengkap
    filepath = os.path.join(DOCS_DIR, filename)
    
    # DEBUG: Cetak di terminal lokasi file yang dicari
    print(f"[*] Mencari file di: {os.path.abspath(filepath)}")
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            return f"<h3>File: {filename}</h3><pre>{content}</pre>"
        else:
            # Beritahu user di mana file itu seharusnya berada (untuk debugging)
            return f"Error: File tidak ditemukan di {filepath}", 404
    except Exception as e:
        return f"Error: {str(e)}", 500
app.run(port=500)