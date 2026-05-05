# Lab 04: LFI Extension Bypass

## 🛡️ Deskripsi Kasus

Lab ini mensimulasikan kegagalan filter keamanan yang mencoba memvalidasi ekstensi file dengan cara memanipulasi string secara manual. Meskipun aplikasi mewajibkan akhiran file tertentu, logika pemrosesan yang dapat diprediksi memungkinkan penyerang untuk menyisipkan payload traversal.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi menggunakan metode `.endswith(".txt")` untuk validasi, namun kemudian melakukan *string slicing* untuk menghapus ekstensi tersebut sebelum memproses file.

### **Potongan Kode Bermasalah**

```python
if filename.endswith(".txt"):
    # VULNERABILITY: Memotong 4 karakter terakhir secara mentah
    clean_name = filename[:-4] 
    filepath = os.path.join(DOCS_DIR, clean_name)
```

### **Titik Lemah:**

- **Predictable Trimming:** Karena aplikasi pasti membuang 4 karakter terakhir, penyerang bisa memberikan file target yang diakhiri dengan ekstensi palsu (dummy extension).
- **Lack of Path Sanitization:** Aplikasi tidak membersihkan karakter `../` setelah proses pemotongan string dilakukan.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **The Extension Trimming Trick**

Untuk membaca file `app_secure.py`, kita harus mengakali filter `.txt` sekaligus memastikan hasil akhirnya merujuk pada file target.

**Payload Sukses:**
`http://127.0.0.1:5000/view?file=../app_secure.py.txt`

**Mekanisme Bypass:**

1. **Validation:** Input `../app_secure.py.txt` lolos karena berakhiran `.txt`.
2. **Manipulation:** Kode `filename[:-4]` membuang `.txt` dan menyisakan `../app_secure.py`.
3. **Execution:** Fungsi `os.path.join` menggabungkan path dan membuka source code asli aplikasi.

---

## ✅ Remediation (Saran Perbaikan)

1. **Gunakan Basename:** Selalu bungkus input user dengan `os.path.basename()` untuk membuang seluruh path traversal.
2. **Strict Validation:** Bandingkan input dengan daftar file yang diizinkan (*Allowlist*) daripada mencoba memanipulasi string secara manual.
3. **Use Pathlib:** Gunakan library `pathlib` yang lebih modern untuk menangani validasi path secara lebih aman di Python.

---
**Researcher:** Squi7 (Nur Alam)
