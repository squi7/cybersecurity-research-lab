# 🧪 Lab 05: Hash-Based DOM XSS (The Client-Side Shadow)

## 🛡️ Deskripsi Kasus

Lab ini mendemonstrasikan kerentanan **DOM XSS** yang menggunakan `window.location.hash` (data setelah tanda `#` di URL) sebagai sumber serangan (*source*). Vektor ini unik karena data *hash* tidak pernah dikirim ke server melalui permintaan HTTP, sehingga seringkali luput dari deteksi **Web Application Firewall (WAF)**.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi memantau perubahan pada fragmen URL dan merender kontennya langsung ke dalam DOM tanpa sanitasi.

### Potongan Kode Bermasalah

```javascript
// Source: Mengambil data dari hash URL
const hashData = decodeURIComponent(window.location.hash.substring(1));

// Sink: Merender data mentah langsung ke innerHTML
const display = document.getElementById('message-box'); 
display.innerHTML = "Selamat datang, " + hashData;
```

### Titik Lemah

1. **Source:** `window.location.hash` sering dianggap sebagai data "internal" oleh developer, padahal dapat dikontrol penuh oleh penyerang melalui URL.
2. **Event Listener:** Penggunaan `hashchange` memungkinkan eksekusi script berkali-kali secara dinamis tanpa perlu memuat ulang (*reload*) halaman.
3. **Dangerous Sink:** Penggunaan `.innerHTML` akan mengeksekusi tag HTML atau script yang disisipkan di dalam string.

---

## 🚀 Teknik Eksploitasi (Payloads)

### 1. Self-Executing Image Payload

Teknik paling umum untuk memicu XSS secara instan saat halaman dibuka atau saat *hash* berubah.

* **Payload:** `#<img src=x onerror=alert('Hash_XSS_Success')>`
* **Mekanisme:** Browser mencoba merender tag `<img>`, gagal menemukan sumber `x`, lalu memicu fungsi `onerror` yang berisi JavaScript.

### 2. Iframe Injection

Menyuntikkan frame eksternal atau menjalankan script dalam konteks iframe.

* **Payload:** `#<iframe src="javascript:alert(document.domain)"></iframe>`

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Invisible to Server:** Selalu periksa *Single Page Application* (SPA) yang menggunakan *hash* untuk navigasi. Karena data setelah `#` tidak sampai ke server, log server tidak akan menunjukkan adanya upaya serangan.
* **WAF Bypass:** Karena payload berada di sisi klien (setelah tanda `#`), filter keamanan di sisi server biasanya akan melewatkannya begitu saja.
* **Sink Monitoring:** Selain `innerHTML`, periksa juga penggunaan data hash pada sink berbahaya lain seperti `eval()`, `setTimeout()`, atau `document.write()`.

---

## ✅ Remediasi (Saran Perbaikan)

Jangan pernah merender data yang berasal dari input pengguna (termasuk URL) sebagai HTML. Gunakan `.textContent` agar data hanya dianggap sebagai teks murni.

### Contoh Perbaikan Kode

```javascript
// Cara Aman: Menggunakan textContent bukan innerHTML
const display = document.getElementById('message-box');
display.textContent = "Selamat datang, " + hashData; 
```

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS (Hash-Based Injection) |
| **Difficulty** | Medium |
| **Last Updated** | 25 April 2026 |
| **Researcher** | Squi7 |
