
# 🧪 Lab 10: Basic Server-Side Request Forgery (SSRF)

## 🛡️ Deskripsi Kasus

Lab ini mensimulasikan kerentanan **SSRF** pada aplikasi Python (Flask) yang memiliki fitur pengecekan status URL eksternal. Karena aplikasi tidak melakukan validasi atau pembatasan (*sandboxing*) terhadap URL yang diminta, penyerang dapat memaksa server untuk melakukan permintaan ke layanan internal yang seharusnya tidak dapat diakses dari luar.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi menggunakan pustaka `requests` untuk mengambil data dari input pengguna tanpa adanya pengecekan terhadap alamat IP atau skema protokol.

### **Potongan Kode Bermasalah**

```python
@app.route('/check-status')
def check_status():
    target_url = request.args.get('url')
    # KERENTANAN: Server melakukan request ke URL apa pun yang diberikan user
    response = requests.get(target_url, timeout=5)
    return f"<pre>{response.text}</pre>"
```

### **Titik Lemah**

* **Lack of URL Filtering:** Aplikasi tidak memeriksa apakah URL mengarah ke alamat *localhost* (`127.0.0.1`) atau rentang IP privat (misal: `192.168.x.x`).
* **Implicit Trust:** Endpoint `/admin-secret-area` hanya mengandalkan pengecekan `request.remote_addr`, yang sangat mudah dikelabui jika permintaan datang dari server itu sendiri melalui SSRF.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **Internal Service Discovery**

Meskipun penyerang tidak bisa mengakses area admin secara langsung, penyerang bisa memerintahkan server aplikasi untuk menjadi "proxy" atau perantara.

**Payload yang Digunakan:**
`[http://127.0.0.1:5000/check-status?url=http://127.0.0.1:5000/admin-secret-area](http://127.0.0.1:5000/check-status?url=http://127.0.0.1:5000/admin-secret-area)`

### **Mekanisme Serangan**

1. **Request:** Penyerang mengirim permintaan ke endpoint publik `/check-status`.
2. **Processing:** Server aplikasi menerima URL internal sebagai parameter.
3. **Redirection:** Server mengeksekusi permintaan HTTP ke dirinya sendiri (`127.0.0.1`).
4. **Bypass:** Endpoint admin mendeteksi IP pengirim adalah *loopback* (internal) dan memberikan akses penuh.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Cloud Metadata Attack:** Pada infrastruktur cloud seperti AWS, SSRF sering digunakan untuk mengakses `[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)` untuk mencuri *IAM Credentials*.
* **Port Scanning:** SSRF dapat digunakan untuk memetakan port yang terbuka di jaringan internal (misal: menebak port database `3306` atau `5432`).
* **Protocol Smuggling:** Selain `http://`, terkadang SSRF mendukung skema lain seperti `file:///etc/passwd` (untuk membaca file lokal) atau `gopher://`.

---

## ✅ Remediation (Saran Perbaikan)

1. **Allowlist-based Filtering:** Hanya izinkan permintaan ke domain atau IP yang sudah terdaftar secara resmi.
2. **Disable Non-HTTP Protocols:** Pastikan aplikasi hanya mendukung skema `http` dan `https`.
3. **Internal Network Isolation:** Letakkan layanan sensitif di jaringan yang benar-benar terpisah atau gunakan autentikasi tambahan yang kuat (jangan hanya mengandalkan pengecekan IP).

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | Basic SSRF |
| **Difficulty** | Medium |
| **Last Updated** | 30 April 2026 |
| **Researcher** | Squi7 |

---
