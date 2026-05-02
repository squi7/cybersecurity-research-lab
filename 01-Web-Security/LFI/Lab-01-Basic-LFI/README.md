
# 🧪 Lab 12: Basic Local File Inclusion (LFI)

## 🛡️ Deskripsi Kasus

Lab ini mendemonstrasikan kerentanan **Local File Inclusion (LFI)** pada aplikasi Python (Flask). Kerentanan ini terjadi ketika aplikasi menerima input nama file dari pengguna untuk ditampilkan, namun tidak melakukan validasi atau sanitasi terhadap karakter navigasi direktori.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi menggunakan fungsi `os.path.join()` untuk menggabungkan folder tujuan dengan input dari user tanpa membatasi ruang lingkup folder tersebut.

### **Potongan Kode Bermasalah**

```python
filepath = os.path.join(DOCS_DIR, filename)
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
```

### **Titik Lemah:**

- **Path Traversal:** Penggunaan karakter `../` (dot-dot-slash) memungkinkan penyerang keluar dari folder `DOCS_DIR` yang ditentukan.
- **No Input Validation:** Aplikasi tidak memeriksa apakah `filename` mengandung karakter berbahaya atau mencoba mengakses file di luar folder dokumentasi.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **1. Directory Traversal (Windows System File)**

Penyerang dapat membaca file sensitif sistem operasi dengan melakukan navigasi ke atas hingga mencapai *root directory* (C:\).

**Payload Sukses:**
`?url=/../../../../../../../../../../../Windows/System32/drivers/etc/hosts`

### **2. Source Code Disclosure**

Penyerang dapat membaca logika aplikasi itu sendiri untuk mencari kerentanan lain atau kredensial yang tersembunyi.

**Payload Sukses:**
`?url=../app.py`

---

## 💡 Pelajaran Teknis untuk Bug Hunter

- **Information Disclosure:** LFI sering digunakan untuk mencuri file konfigurasi (seperti `.env`, `settings.py`, atau `config.php`).
- **Escalation to RCE:** Jika penyerang bisa membaca file log (Log Poisoning), mereka bisa menyuntikkan kode berbahaya dan mendapatkan kendali penuh atas server.

---

## ✅ Remediation (Saran Perbaikan)

1. **Basename Validation:** Gunakan `os.path.basename(filename)` untuk mengambil hanya nama filenya saja, sehingga karakter `../` akan terbuang.
2. **Allowlist:** Hanya izinkan daftar file tertentu yang boleh dibaca oleh aplikasi.
3. **Filesystem Permissions:** Jalankan aplikasi dengan hak akses terbatas (Least Privilege) agar tidak bisa membaca file sistem sensitif.

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | Local File Inclusion (LFI) |
| **Difficulty** | Medium |
| **Last Updated** | 03 Mei 2026 |
| **Researcher** | Squi7 |
