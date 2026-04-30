# 🧪 Lab 09: Prototype Pollution to XSS (The Gadget Chain)

## 🛡️ Deskripsi Kasus

Lab ini mendemonstrasikan bagaimana kerentanan **Prototype Pollution** dapat ditingkatkan menjadi **Cross-Site Scripting (XSS)**. Serangan ini memanfaatkan objek kosong yang digunakan oleh aplikasi untuk konfigurasi dinamis, di mana properti yang tidak terdefinisi secara eksplisit diambil dari prototipe yang telah dicemari.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi memiliki fungsi `merge` yang tidak aman dan sebuah fungsi "Gadget" (`renderContent`) yang membuat elemen skrip secara dinamis.

### **Potongan Kode Gadget**

```javascript
function renderContent() {
    const options = {}; 
    if (options.transportUrl) { // Titik Gadget
        const script = document.createElement('script');
        script.src = options.transportUrl; // Injeksi Sink (Dangerous Sink)
        document.body.appendChild(script);
    }
}
```

### **Titik Lemah**

* **Uninitialized Objects:** Objek `options` didefinisikan sebagai objek kosong `{}` tanpa perlindungan terhadap polusi prototipe.
* **Dangerous Sink:** Atribut `src` pada elemen `<script>` digunakan tanpa validasi atau sanitasi URL, memungkinkan pemuatan skrip dari skema `data:`.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **The Script Injection Gadget**

Kita tidak menyentuh variabel `options` secara langsung, melainkan meracuni "induk" dari semua objek agar memberikan nilai ke properti `transportUrl`.

**Payload yang Digunakan:**
`?__proto__[transportUrl]=data:,alert('XSS_via_Prototype_Pollution')`

### **Mekanisme Serangan**

1. **Pollution:** Parameter URL diproses oleh fungsi `merge`, menyuntikkan `transportUrl` ke dalam `Object.prototype`.
2. **Gadget Trigger:** Saat `renderContent` berjalan, pengecekan `options.transportUrl` yang tadinya *undefined* kini bernilai string `data:,alert(...)`.
3. **XSS Execution:** Aplikasi membuat tag `<script>` dengan sumber dari payload kita, yang langsung dieksekusi oleh mesin JavaScript browser.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Gadget Hunting:** Dalam audit nyata, carilah kata kunci seperti `.src`, `.innerHTML`, atau `.href` yang mengambil nilai dari objek yang terlihat "aman" atau opsional.
* **Library Analysis:** Banyak library populer (seperti jQuery lama) memiliki gadget internal yang bisa dipicu jika kita berhasil melakukan Prototype Pollution pada aplikasi utama.
* **Data URI:** Skema `data:` sangat berguna dalam eksploitasi XSS jika kita tidak bisa memanggil file skrip eksternal (*Remote Script*).

---

## ✅ Remediation (Saran Perbaikan)

1. **Object Protection:** Gunakan `Object.create(null)` untuk objek konfigurasi agar tidak memiliki prototipe.
2. **Input Validation:** Selalu validasi URL atau sumber skrip menggunakan *allowlist* sebelum memasukkannya ke dalam atribut sensitif seperti `src`.
3. **Prototype Freezing:** Gunakan `Object.freeze(Object.prototype)` di awal aplikasi untuk mencegah mutasi global.

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | Prototype Pollution to XSS |
| **Difficulty** | Advanced |
| **Last Updated** | 29 April 2026 |
| **Researcher** | Squi7 |

---
