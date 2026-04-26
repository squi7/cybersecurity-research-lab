# 🧪 Lab 06: Eval Injection (The Executioner)

## 🛡️ Deskripsi Kasus

Lab ini mendemonstrasikan salah satu kerentanan paling kritis dalam JavaScript, yaitu penggunaan fungsi `eval()`. Fungsi ini mengeksekusi string sebagai kode program. Jika input pengguna digabungkan langsung ke dalam `eval()`, penyerang dapat mengambil alih seluruh logika aplikasi di sisi klien.

---

## 🧱 Analisis Kode (Vulnerability)

Aplikasi menggunakan input URL untuk melakukan kalkulasi pajak secara dinamis.

**Potongan Kode Bermasalah:**

```javascript
const result = eval(price + " * " + taxRate);
document.getElementById('tax-result').innerHTML = "Total Pajak: " + result;
```

### **Titik Lemah:**

* **Sink:** `eval()`. Ini adalah sink "High-Impact" karena mampu mengeksekusi *JavaScript Logic* murni, bukan sekadar merender HTML.
* **Missing Validation:** Aplikasi tidak memastikan bahwa `taxRate` adalah sebuah angka (`Number`) sebelum memasukkannya ke dalam mesin eksekusi.

---

## 🚀 Teknik Eksploitasi (Payloads)

### **1. Basic Logic Breakout**

Memutus rantai operasi matematika untuk menjalankan perintah baru.

* **Payload:** `?tax=0.1; alert(document.domain)`
* **Logika:** `eval("1000000 * 0.1; alert(document.domain)")`
* **Dampak:** Script berhasil dijalankan, namun fungsionalitas kalkulator mungkin rusak (menampilkan `undefined`).

### **2. Stealth "Ghost" Injection (Advanced)**

Menjalankan script berbahaya tanpa merusak tampilan angka pada aplikasi. Ini membuat serangan sulit dideteksi oleh pengguna awam.

* **Payload:** `?tax=0.1 + (alert('Hacked_by_Alam') || 0)`
* **Analisis:** * `alert()` dijalankan terlebih dahulu.
  * Fungsi `alert()` mengembalikan nilai `undefined`.
  * Operator `|| 0` mengubah `undefined` menjadi `0`.
  * Hasil akhir kalkulasi: `0.1 + 0 = 0.1` (Kalkulasi tetap akurat 100%).

---

## 💡 Pelajaran Teknis untuk Bug Hunter

* **Beyond alert(1):** Dalam skenario `eval()`, penyerang bisa melakukan *Data Exfiltration* (mencuri data sensitif) atau *Session Hijacking* dengan jauh lebih mudah dibanding jenis XSS lainnya.
* **Stealth Matters:** Selalu usahakan agar payload tidak merusak fungsionalitas asli aplikasi. Hal ini menunjukkan tingkat keahlian *researcher* yang lebih tinggi dalam laporan Bug Bounty.
* **Alternative Sinks:** Selain `eval()`, waspadai juga fungsi `setTimeout("string")`, `setInterval("string")`, dan `new Function("string")`.

---

## ✅ Remediasi (Saran Perbaikan)

**"Eval is Evil."** Hindari penggunaan `eval()` sepenuhnya. Gunakan konversi tipe data yang aman.

**Contoh Perbaikan Modern:**

```javascript
const tax = Number(taxRate); // Paksa input menjadi tipe Number

if (!isNaN(tax)) {
    const result = price * tax; // Operasi matematika murni, bukan eksekusi string
    document.getElementById('tax-result').textContent = "Total Pajak: " + result.toLocaleString('id-ID');
} else {
    console.error("Input pajak tidak valid!");
}
```

## 🛠️ Status Lab

| Informasi | Detail |
| :--- | :--- |
| **Vulnerability** | DOM XSS (Eval() Injection) |
| **Difficulty** | Medium |
| **Last Updated** | 26 April 2026 |
| **Researcher** | Squi7 |
