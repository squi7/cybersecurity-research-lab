# 🧪 Lab 02: Bypassing Filters & Modern Sanitization

## 🛡️ Deskripsi Kasus

Lab ini mendemonstrasikan kegagalan strategi keamanan berbasis **Blacklisting** (melarang kata kunci tertentu). Developer mencoba memblokir kata kunci berbahaya, namun penyerang dapat menemukan cara untuk mem-*bypass* filter tersebut menggunakan variasi teknik *encoding* atau manipulasi struktur tag.

---

## ❌ Masalah: Blacklist Filter (Insecure)

Banyak developer menggunakan metode `.replace()` untuk menghapus tag secara manual. Ini adalah pendekatan yang sangat rentan.

### Contoh Filter yang Lemah

```javascript
// 1. Sangat Lemah: Case-sensitive dan hanya menghapus satu kata spesifik.
let filteredInput = input.replace("<script>", "");

// 2. Tetap Lemah: Masih bisa ditembus dengan teknik Recursive atau Nesting.
let regexFilter = input.replace(/script|alert|img|onload/gi, "");
```

### Teknik Bypass yang Berhasil

* **Recursive Bypass:** `<scrscriptipt>` → Setelah filter menghapus kata "script" di tengah, sisa karakter akan menyatu kembali menjadi `<script>`.
* **Event Handler Bypass:** Menggunakan tag yang tidak ada dalam daftar blokir, seperti `<svg onload=...>` atau `<details ontoggle=...>`.

---

## ✅ Solusi Modern: Sanitasi vs Encoding

Untuk mencegah **DOM XSS** secara total, terdapat dua pendekatan standar industri yang direkomendasikan:

### 1. HTML Entity Encoding (Mencegah Eksekusi)

Metode ini mengubah karakter berbahaya menjadi simbol teks murni sehingga browser tidak akan mengeksekusinya sebagai kode HTML.

* `<` menjadi `&lt;`
* `>` menjadi `&gt;`

**Implementasi Kode Aman:**

```javascript
// Menggunakan browser API untuk encoding otomatis
function escapeHTML(str) {
    const p = document.createElement('p');
    p.textContent = str; // Browser secara otomatis melakukan encoding
    return p.innerHTML;
}

// Penggunaan langsung pada elemen
document.getElementById('search-result').textContent = input; 
```

### 2. DOMPurify (Library Standar Industri)

Jika aplikasi **harus** mengizinkan beberapa tag HTML (misal: `<b>` atau `<i>`), gunakan library sanitasi berbasis *whitelist* seperti **DOMPurify**. Library ini menghapus atribut berbahaya (seperti `onerror`) namun mempertahankan tag yang aman.

**Cara Kerja Sanitasi Modern:**

```javascript
// Menghapus semua yang berbahaya, menyisakan yang aman
const clean = DOMPurify.sanitize(input);
document.getElementById('search-result').innerHTML = clean;
```

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Blacklist is Fail:** Jangan pernah percaya pada filter yang hanya menghapus kata kunci tertentu. Penyerang selalu lebih kreatif daripada daftar kata terlarang.
* **Context Matters:** Selalu periksa di mana input ditampilkan. Jika masuk ke `.innerHTML`, sanitasi adalah **wajib**. Jika masuk ke `.textContent`, aplikasi secara otomatis aman dari XSS.
* **Modern Defense:** Saat melakukan pentest, periksa apakah aplikasi menggunakan library seperti DOMPurify. Jika ya, carilah celah pada konfigurasi khusus library tersebut atau cari *namespace* yang tidak ter-cover.

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS (Filter Bypass) |
| **Difficulty** | Easy - Medium |
| **Last Updated** | 22 April 2026 |
| **Researcher** | Squi7 |

---
