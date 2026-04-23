# 🧪 Lab 03: Attribute Injection (Breaking the Quotes)

## 🛡️ Deskripsi Kasus

Lab ini mensimulasikan skenario di mana input pengguna dimasukkan ke dalam **atribut** elemen HTML—dalam hal ini, atribut `value` pada tag `<input>`.

Kerentanan ini terjadi karena aplikasi tidak melakukan *escaping* pada karakter tanda kutip (`"`). Hal ini memungkinkan penyerang untuk "keluar" dari konteks atribut asli dan menyuntikkan atribut baru yang berbahaya (seperti *event handlers*).

---

## 🧱 Analisis Kode (Vulnerability)

Data diambil dari parameter URL `nick` dan dimasukkan ke dalam string HTML melalui properti `innerHTML`.

### **Potongan Kode Bermasalah:**

```javascript
const nick = urlParams.get('nick');

// Sink: Data digabungkan langsung ke dalam string atribut HTML
container.innerHTML = '<input type="text" value="' + nick + '">';
```

> [!CAUTION]
> **Titik Lemah:**
> Developer berasumsi pengguna hanya akan memasukkan teks biasa. Namun, karena karakter `"` tidak difilter, penyerang bisa mengirimkan karakter tersebut untuk menutup atribut `value` secara prematur.

---

## 🚀 Teknik Eksploitasi (Payloads)

### 1. Event Handler Injection (`onmouseover`)

Teknik ini menyuntikkan atribut *event* baru ke dalam tag yang sudah ada.

* **Payload:** `?nick=" onmouseover="alert('XSS_Attribute_Injection')`
* **Hasil di DOM:**

    ```html
    <input type="text" value="" onmouseover="alert('XSS_Attribute_Injection')">

    ```

* **Mekanisme:** Alert akan terpicu saat kursor mouse melewati (hover) kotak input tersebut.

### 2. Breaking Out of Tag (Tag Injection)

Teknik ini menutup tag `<input>` sepenuhnya dan membuat tag baru secara mandiri.

* **Payload:** `?nick="><img src=x onerror=alert(1)>`
* **Hasil di DOM:**

    ```html

    <input type="text" value=""><img src=x onerror=alert(1)>">

    ```

* **Mekanisme:** Alert terpicu secara otomatis saat halaman dimuat karena tag `<img>` baru memicu *error* saat mencoba memuat sumber (`src`) yang tidak valid.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Context is King:** XSS tidak selalu berarti membuat tag `<script>`. Perhatikan di mana input Anda mendarat. Jika mendarat di dalam kutipan, misi pertama Anda adalah **menutup kutipan** tersebut.
* **Hidden Sinks:** Atribut seperti `value`, `src`, `href`, dan `title` sering kali menjadi target empuk untuk *Attribute Injection*.
* **Interaction vs Non-Interaction:** Atribut seperti `onmouseover` membutuhkan interaksi user, sedangkan `onerror` atau `onload` tidak. Dalam laporan Bug Bounty, payload **tanpa interaksi** biasanya memiliki *severity* (tingkat bahaya) yang lebih tinggi.

---

## ✅ Remediasi (Saran Perbaikan)

Untuk mencegah serangan ini, karakter khusus HTML harus diubah menjadi **HTML Entities** atau menggunakan metode manipulasi DOM yang lebih aman.

### **Cara Aman (Menggunakan Properti Objek):**

Jika tujuannya hanya mengisi nilai input, jangan gunakan `innerHTML` untuk membangun seluruh tag. Gunakan manipulasi properti secara langsung:

```javascript
const inputField = document.createElement('input');
inputField.type = 'text';

// AMAN: Browser menangani 'nick' sebagai teks murni (literal), bukan kode HTML
inputField.value = nick; 

container.appendChild(inputField);
```

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS (Attribute Injection) |
| **Difficulty** | Easy - Medium |
| **Last Updated** | 23 April 2026 |
| **Researcher** | Squi7 |
