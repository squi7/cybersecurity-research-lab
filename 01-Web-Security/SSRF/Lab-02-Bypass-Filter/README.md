# 🧪 Lab 11: SSRF Filter Bypass (Blacklist Evasion)

## 🛡️ Deskripsi Kasus

Lab ini mensimulasikan mekanisme pertahanan **Blacklist** yang sering diimplementasikan pengembang untuk mencegah *Server-Side Request Forgery* (SSRF). Fokus riset ini adalah membuktikan bahwa pengecekan berbasis teks (*string matching*) tidak cukup untuk menghentikan serangan, karena alamat IP memiliki berbagai representasi alias yang dapat dikenali oleh sistem operasi dan library jaringan.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi mencoba memfilter input pengguna dengan memeriksa keberadaan kata kunci sensitif di dalam URL sebelum melakukan permintaan HTTP.

### **Potongan Kode Filter (Python/Flask)**

```python
BLACKLIST = ["127.0.0.1", "localhost", "0.0.0.0"]

def check_vulnerability(target_url):
    # Filter berbasis teks mentah
    if any(blacklisted in target_url for blacklisted in BLACKLIST):
        return "❌ DETEKSI SERANGAN: Akses Dilarang", 403
    
    # Jika lolos, aplikasi melakukan request
    # response = requests.get(target_url)
```

### **Titik Lemah:**

1. **Incomplete Blacklist:** Daftar hitam tidak mencakup alias DNS lokal atau format encoding IP lainnya (seperti Decimal, Hexadecimal, atau Octal).
2. **Surface-Level Validation:** Filter hanya memeriksa teks mentah (*raw string*) dan tidak melakukan resolusi DNS terlebih dahulu untuk mengetahui IP asli di balik sebuah nama host sebelum validasi dilakukan.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **The "loopback" Alias Bypass**

Pada sistem operasi tertentu (khususnya Windows), terdapat nama alias internal yang merujuk pada mesin itu sendiri namun sering kali tidak terdaftar dalam blacklist umum.

* **Payload Sukses:**
    `[http://target-app.com/check-status?url=http://loopback:5000/admin-secret-area](http://target-app.com/check-status?url=http://loopback:5000/admin-secret-area)`

### **Mekanisme Bypass:**

1. **Filter Evasion:** Kata `loopback` tidak mengandung string `127.0.0.1` atau `localhost`, sehingga lolos dari pengecekan `if any(...)`.
2. **OS Resolution:** Saat fungsi `requests.get()` dipanggil, *resolver* sistem operasi menerjemahkan `loopback` menjadi alamat loopback standar (`127.0.0.1`).
3. **Execution:** Server akhirnya melakukan permintaan ke endpoint admin internalnya sendiri tanpa menyadari bahwa ia mengakses dirinya sendiri.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

Eksperimen ini menunjukkan bahwa validasi input URL sangat kompleks:

* **Environment Matters:** Teknik bypass seperti konversi **Desimal** (`2130706433`), **Hex** (`0x7f000001`), atau **Short-IP** (`127.1`) sangat bergantung pada bagaimana library bahasa pemrograman dan OS melakukan resolusi alamat.
* **DNS Aliases:** Selalu coba nama alias unik seperti `loopback`, `local`, atau `localhost.localdomain`.
* **IPv6 Evasion:** Jangan lupa mencoba format IPv6 seperti `[::1]` atau `[0:0:0:0:0:0:0:1]` yang sering kali luput dari filter regex sederhana.

---

## ✅ Remediation (Saran Perbaikan)

| Strategi | Deskripsi |
| :--- | :--- |
| **Whitelist Approach** | Hanya izinkan koneksi ke domain atau IP yang telah ditentukan secara eksplisit (*Positive Security Model*). |
| **DNS Resolution Check** | Resolusi DNS input pengguna ke IP address, lalu pastikan IP tersebut bukan bagian dari rentang IP privat (**RFC 1918**) sebelum mengirim request. |
| **Network Isolation** | Gunakan firewall atau *Security Groups* untuk mencegah server aplikasi mengakses port layanan sensitif di jaringan internal secara fisik. |

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | SSRF Filter Bypass |
| **Difficulty** | High (Context Dependent) |
| **Last Updated** | 01 Mei 2026 |
| **Researcher** | Squi7 |
