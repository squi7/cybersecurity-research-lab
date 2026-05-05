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

    # SKENARIO: Developer memaksa user menginput .txt, 
    # lalu dia mencoba "menghapus" .txt tersebut untuk diproses.
    if not filename.endswith(".txt"):
        return "❌ Error: Harus berakhiran .txt!", 403

    # KESALAHAN: Dia hanya menghapus 4 karakter terakhir
    clean_name = filename[:-4] 
    
    filepath = os.path.join(DOCS_DIR, clean_name)
    
    print(f"[*] Mencari file di: {filepath}")
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        else:
            return f"Error: File {clean_name} tidak ditemukan!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500
    
if __name__ == '__main__':
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    app.run(port=5000)