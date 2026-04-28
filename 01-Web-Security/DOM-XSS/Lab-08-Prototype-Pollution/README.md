# 🧪 Lab 08: Client-Side Prototype Pollution (DNA Mutation)

## 🛡️ Deskripsi Kasus

Lab ini mendemonstrasikan kerentanan **Prototype Pollution**, sebuah serangan yang menargetkan mekanisme pewarisan (inheritance) pada JavaScript. Dengan memanipulasi objek prototipe dasar (`Object.prototype`), penyerang dapat menyuntikkan properti ke semua objek di dalam aplikasi, yang sering kali berujung pada bypass logika keamanan atau XSS.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi menggunakan fungsi penggabungan objek (*merge*) secara manual untuk mengolah konfigurasi pengguna dari parameter URL.

**Potongan Kode Bermasalah:**

```javascript
function transport(target, source) {
    for (let key in source) {
        if (key === "__proto__") {
            // Kerentanan Kritis: Mengizinkan akses ke Prototype Dasar
            Object.assign(target.__proto__, source[key]);
        } else {
            target[key] = source[key];
        }
    }
}
```

### **Titik Lemah:**

1. **Lack of Property Sanitization:** Fungsi `transport` tidak memblokir atau melakukan *sanitasi* terhadap kata kunci sensitif seperti `__proto__`, `constructor`, atau `prototype`.
2. **Global Inheritance:** Di JavaScript, hampir semua objek mewarisi dari `Object.prototype`. Mengubah satu titik ini akan memengaruhi setiap objek kosong yang dibuat setelahnya.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **The Admin Logic Bypass**

Penyerang tidak perlu mengubah variabel yang sudah ada, melainkan menyuntikkan "aturan baru" ke DNA aplikasi.

**Payload yang Digunakan:**
`?__proto__[isAdmin]=true`

**Mekanisme Serangan:**

1. **Injection:** Fungsi `transport` menerima input dari URL dan mengeksekusi `Object.assign(target.__proto__, {isAdmin: true})`.
2. **Pollution:** `Object.prototype` sekarang memiliki properti `isAdmin: true`.
3. **Inheritance:** Saat aplikasi mengeksekusi `const session = {}`, objek `session` yang kosong tersebut secara otomatis "mewarisi" properti `isAdmin` dari prototipenya.
4. **Bypass:** Logika `if (session.isAdmin)` bernilai **TRUE**, memberikan akses administratif ilegal kepada penyerang.

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Invisible Properties:** Kerentanan ini sangat berbahaya karena properti yang disuntikkan tidak terlihat saat Anda melakukan `console.log(session)`, tetapi ada di dalam `__proto__`.
* **Beyond Logic Bypass:** Dalam skenario nyata, Prototype Pollution sering digunakan untuk memicu **DOM XSS** dengan menimpa properti sensitif seperti `innerHTML` atau `src` pada library pihak ketiga (seperti jQuery atau lodash).
* **Deep Merge Warning:** Selalu curigai fungsi yang melakukan *deep merge* atau *object cloning* secara rekursif.

---

## ✅ Remediation (Saran Perbaikan)

Mencegah mutasi pada prototipe objek sangat krusial untuk aplikasi JavaScript modern.

### **1. Gunakan Objek Tanpa Prototipe**

Buat objek yang benar-benar bersih tanpa warisan `__proto__`.

```javascript
const userConfig = Object.create(null);
```

### **2. Bekukan Prototipe**

Mencegah perubahan pada prototipe dasar di seluruh aplikasi.

```javascript
Object.freeze(Object.prototype);
```

### **3. Gunakan Map()**

Gunakan struktur data `Map` alih-alih objek biasa untuk menyimpan pasangan *key-value* dari input pengguna.

---

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | Prototype Pollution (Client-Side) |
| **Difficulty** | High |
| **Last Updated** | 28 April 2026 |
| **Researcher** | Squi7 |
