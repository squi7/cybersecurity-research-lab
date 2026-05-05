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
    
    # PERTAHANAN: Developer memaksa ekstensi file harus .txt
    # jika user input 'app.py', maka akan berubah menjadi 'app.py.txt'
    target_file = filename + ".txt"
    filepath = os.path.join(DOCS_DIR, target_file)

    print (f"[*] Mencari file di: {filepath}")

    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"<pre>{content}</pre>"
        else:
            return f"Error: File {target_file} tidak ditemukan!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500
    
if __name__ == '__main__':
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    app.run(port=5000)