# 🧪 Lab 04: URL Protocol Injection (Dangerous Href)

## 🛡️ Deskripsi Kasus

Lab ini mensimulasikan kerentanan pada fitur navigasi dinamis. Aplikasi mengambil input dari parameter URL dan menggunakannya sebagai nilai untuk atribut `href` pada tag anchor (`<a>`). Masalah muncul karena aplikasi **tidak memvalidasi skema protokol URL** yang diizinkan.

---

## 🧱 Analisis Kode (Vulnerability)

Input dari user dikontrol sepenuhnya untuk mengisi tujuan navigasi link tanpa adanya sanitasi.

### Potongan Kode Bermasalah

```javascript
const targetUrl = urlParams.get('return_to');

// Sink: setAttribute digunakan untuk mengisi atribut href
backBtn.setAttribute('href', targetUrl);
```

### Titik Lemah

Developer mengira pengguna hanya akan memasukkan URL valid seperti `https://google.com`. Namun, atribut `href` juga mendukung **Pseudo-protocol JavaScript**, yang memungkinkan eksekusi kode langsung saat link diklik oleh pengguna.

---

## 🚀 Teknik Eksploitasi (Payloads)

### 1. JavaScript Protocol Injection

Menyuntikkan instruksi JavaScript langsung ke dalam skema URL.

* **Payload:** `?return_to=javascript:alert(document.domain)`
* **Mekanisme:** Saat tombol diklik, browser tidak berpindah halaman, melainkan mengeksekusi string setelah `javascript:`.

### 2. Cookie Stealing (Impact Simulation)

Menunjukkan dampak yang lebih serius daripada sekadar alert sederhana.

* **Payload:** `?return_to=javascript:console.log(%22Mencuri_Session:%20%22%20%2B%20document.cookie)`
* **Analisis:** Penyerang dapat mengirimkan data sensitif ini ke server luar (Out-of-band) menggunakan fungsi `fetch()`.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Sink setAttribute:** Memberikan perhatian khusus pada `setAttribute('href', ...)` atau `setAttribute('src', ...)`.
* **Protocol Whitelisting:** Selalu cek apakah aplikasi membolehkan protokol selain `http:` dan `https:`.
* **Click-based Execution:** XSS jenis ini memerlukan interaksi user (klik). Meskipun demikian, dampaknya tetap tinggi jika diletakkan pada tombol yang krusial seperti "Login" atau "Logout".

---

## ✅ Remediasi (Saran Perbaikan)

Gunakan validasi ketat (**Whitelist**) untuk memastikan hanya protokol yang aman yang diizinkan.

### Contoh Perbaikan

```javascript
// Validasi protokol secara eksplisit
if (targetUrl.startsWith('http://') || targetUrl.startsWith('https://')) {
    backBtn.setAttribute('href', targetUrl);
} else {
    backBtn.setAttribute('href', '#'); // Default ke safe link (mencegah injeksi)
}
```

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS (URL Injection) |
| **Difficulty** | Easy - Medium |
| **Last Updated** | 24 April 2026 |
| **Researcher** | Squi7 |
