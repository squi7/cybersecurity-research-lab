from flask import Flask, request
import os

app =Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")

@app.route('/view')
def view_file():
    filename = request.args.get('file')
    
    if not filename:
        return "⚠️ Masukkan nama file!", 400

    # CELAH LOGIKA: Developer hanya mengecek apakah kata ".txt" ADA di dalam nama file.
    # Ini kesalahan fatal yang sering terjadi karena malas pakai regex atau basename.
    if ".txt" not in filename:
        return "❌ Error: Hanya boleh membaca file .txt!", 403

    # Karena pengecekan di atas lolos, file langsung digabung
    filepath = os.path.join(DOCS_DIR, filename)
    
    print(f"[*] Mencari file di: {filepath}")
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        else:
            return f"Error: File {filename} tidak ditemukan!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    app.run(port=5000)