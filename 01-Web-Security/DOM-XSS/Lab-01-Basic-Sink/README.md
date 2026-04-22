# 🧪 Vulnerability Lab 01: DOM XSS Playground

Selamat datang di Lab Kerentanan DOM XSS. File ini dirancang untuk mensimulasikan bagaimana data yang tidak difilter dapat mengalir dari input pengguna ke fungsi eksekusi berbahaya di sisi klien.

## 📁 Struktur Lab

- **File Utama:** `vulnerable-lab-01.html`
- **Tujuan:** Memahami alur kerja *Cross-Site Scripting* (XSS) berbasis DOM (Document Object Model).

---

## 🔍 Materi Pembelajaran Utama

### 1. Analisis "Source to Sink"

Ini adalah keahlian teknis paling fundamental bagi seorang *bug hunter*. Anda belajar untuk melacak perjalanan data.

- **Source (Pintu Masuk):** Di mana data masuk ke aplikasi.
  - Dalam lab ini: `URLSearchParams` (mengambil dari URL) dan `.value` dari form input.
- **Sink (Pintu Eksekusi):** Fungsi atau properti JavaScript yang dapat mengeksekusi kode jika tidak divalidasi.
  - Dalam lab ini: Properti `.innerHTML`.

**💡 Skill Tip:** Biasakan membaca file `.js` pada target asli. Cari kata kunci (Sink) seperti `innerHTML`, `document.write()`, atau `eval()`, lalu lakukan *trace back* (tarik mundur) untuk menemukan dari mana variabel tersebut berasal.

---

### 2. Browser Storage sebagai Vektor Serangan

Banyak pemula hanya fokus pada URL. Lab ini menunjukkan bahwa penyimpanan lokal (LocalStorage) bisa menjadi tempat persembunyian *payload* yang mematikan.

- **Skenario:** Data dimasukkan hari ini, disimpan di browser, dan dieksekusi besok saat pengguna membuka kembali halaman tersebut. Ini disebut **Stored DOM XSS**.
- **💡 Skill Tip:** Selalu periksa tab **Inspect Element > Application > Local Storage**. Jika Anda bisa memasukkan data ke sana dan data tersebut ditampilkan kembali melalui sink berbahaya, Anda menemukan *bug* bernilai tinggi.

---

### 3. Manipulasi DOM & Client-Side Logic

Kerentanan tidak selalu di *backend*. JavaScript yang ceroboh di sisi klien bisa merusak seluruh keamanan aplikasi.

- **💡 Skill Tip:** Pelajari fungsi manipulasi teks seperti `.replace()`, `.split()`, atau `.substring()`. Developer sering membuat filter sendiri (misal menghapus kata `<script>`). Tugas Anda adalah mencari *bypass* (misal menggunakan huruf besar-kecil: `<sCrIpT>`).

---

### 4. Eksplorasi Payload (Cheat Sheet)

Karena `.innerHTML` secara bawaan memblokir tag `<script>`, Anda belajar menggunakan *Event Handlers*.

| Jenis Payload | Kode Payload | Kegunaan |
| :--- | :--- | :--- |
| **Basic Error** | `<img src=x onerror=alert(1)>` | Mengetes celah dasar. |
| **Stealing Cookie** | `<img src=x onerror=console.log(document.cookie)>` | Mencuri sesi pengguna. |
| **Modern Tag** | `<details open ontoggle=alert(1)>` | Sering lolos dari filter kata kunci gambar. |
| **Iframe** | `<iframe src="javascript:alert(1)">` | Eksekusi di dalam frame. |

---

## 🛠️ Cara Praktik (Eksploitasi)

### Kasus 1: Reflected DOM XSS

1. Buka file melalui Live Server.
2. Tambahkan parameter di URL: `?name=<img src=x onerror=alert('Reflected_XSS')>`
3. Tekan Enter.

### Kasus 2: Stored DOM XSS

1. Masukkan payload `<svg onload=alert('Stored_XSS')>` ke dalam kotak input status.
2. Klik tombol **Update**.
3. **Refresh Halaman (F5).** Alert akan tetap muncul karena data tersimpan di LocalStorage.

---

## ✅ Remediasi (Saran Perbaikan)

Sebagai *bug hunter* profesional, Anda harus tahu cara memperbaikinya:

- **Salah (Vulnerable):** `element.innerHTML = userInput;`
- **Benar (Aman):** `element.textContent = userInput;` atau `element.innerText = userInput;`

Menggunakan `.textContent` akan membuat browser menganggap semua input sebagai teks murni, bukan kode HTML yang harus dijalankan.

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS |
| **Difficulty** | Easy - Medium |
| **Last Updated** | 21 April 2026 |
| **Researcher** | Squi7 |

---
