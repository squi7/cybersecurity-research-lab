# 🧪 Lab 07: DOM Clobbering (Advanced Logic Hijacking)

## 🛡️ Deskripsi Kasus

Lab ini mensimulasikan kerentanan pada aplikasi yang mengandalkan variabel global atau objek konfigurasi yang belum diinisialisasi secara ketat. Dengan memanfaatkan perilaku browser dalam memetakan `id` dan `name` HTML ke dalam objek `window`, penyerang dapat "menimpa" (*clobber*) variabel tersebut dengan elemen DOM buatan.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi mencoba mengambil konfigurasi *endpoint* dari variabel global `window.config`. Jika tidak ditemukan, aplikasi akan menggunakan nilai *default*.

**Potongan Kode Bermasalah:**

```javascript
const settings = window.config || { endpoint: "default-api.com" };

if (settings.endpoint && settings.endpoint.toString().includes('javascript:')) {
    location.href = settings.endpoint;
}
```

### **Titik Lemah:**

1. **Namespace Collision:** Browser secara otomatis membuat properti pada objek `window` berdasarkan atribut `id` elemen HTML.
2. **Implicit Conversion:** Elemen `<a>` jika dipanggil sebagai string (`toString()`) secara otomatis akan mengembalikan nilai dari atribut `href`-nya.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **Level 2: Nested Clobbering (Koleksi HTML)**

Untuk menimpa properti di dalam sebuah objek (seperti `config.endpoint`), kita menggunakan teknik koleksi elemen dengan ID yang sama untuk membentuk struktur objek buatan di JavaScript.

**Payload yang Digunakan:**

```html
<a id="config"></a>
<a id="config" name="endpoint" href="javascript:alert('Hacked_by_Alam_Perfectly!')"></a>
```

**Mekanisme Serangan:**

1. Dua elemen dengan `id="config"` memaksa `window.config` menjadi sebuah `HTMLCollection`.
2. Elemen kedua memiliki atribut `name="endpoint"`, sehingga `window.config.endpoint` secara otomatis merujuk pada elemen tersebut.
3. Saat *script* memanggil `settings.endpoint`, ia mendapatkan elemen `<a>` alih-alih string *default*.
4. Saat divalidasi dengan `.includes('javascript:')`, elemen tersebut dikonversi menjadi string `href`-nya, yang kemudian memicu eksekusi *payload* saat diarahkan oleh `location.href`.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Logic Over Syntax:** Serangan ini unik karena tidak memerlukan tag `<script>`. Banyak filter XSS yang mengizinkan tag `<a>`, menjadikannya teknik *bypass* yang sangat efektif.
* **Debugging Typos:** Kesesuaian antara atribut `name` di HTML dan nama properti di JavaScript sangat krusial. Satu huruf salah (misal: `enpoint` vs `endpoint`) akan menggagalkan serangan.
* **Context is King:** Selalu periksa apakah aplikasi menggunakan variabel global tanpa deklarasi `const` atau `let`.

---

## ✅ Remediation (Saran Perbaikan)

Gunakan teknik deklarasi variabel yang aman dan hindari ketergantungan pada objek `window` secara global.

**Contoh Perbaikan (Safe Coding):**

```javascript
// Cara Aman: Gunakan pengecekan tipe data secara eksplisit
const settings = (window.config && !(window.config instanceof HTMLElement)) 
                 ? window.config 
                 : { endpoint: "default-api.com" };
```

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS (DOM Clobbering) |
| **Difficulty** | Medium |
| **Last Updated** | 27 April 2026 |
| **Researcher** | Squi7 |
