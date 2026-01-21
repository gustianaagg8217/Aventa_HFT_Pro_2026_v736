# 🎯 RINGKASAN FITUR EXPIRY LICENSE - BAHASA INDONESIA

## Apa Itu Fitur Expiry?

Fitur expiry memungkinkan admin untuk membuat **serial number yang kadaluarsa** pada tanggal tertentu. Ini berguna untuk:

- ✅ **Trial 7 hari** - Pelanggan baru mencoba program
- ✅ **Subscription bulanan** - Pelanggan membayar per bulan
- ✅ **Lisensi unlimited** - Pelanggan permanent

---

## Tiga Tipe Lisensi

### 1️⃣ Unlimited (Tidak Pernah Kadaluarsa)
- Serial dapat digunakan selamanya
- Tidak ada tanggal kadaluarsa
- Untuk pelanggan permanent

**Contoh**: Pelanggan membeli lisensi selamanya

### 2️⃣ Trial (7 Hari - Otomatis Expire)
- Serial berlaku 7 hari
- Setelah 7 hari, program tidak bisa dijalankan
- Untuk mencoba gratis

**Contoh**: Pelanggan baru mendapat akses trial 7 hari, setelah itu harus bayar

### 3️⃣ Custom Days (Jumlah Hari Pilihan)
- Serial berlaku N hari (bisa 30, 60, 90, dll)
- Admin memilih berapa lama
- Untuk subscription

**Contoh**: Pelanggan bayar Rp 500.000/bulan → dapat serial 30 hari

---

## Cara Kerja Admin

### Langkah 1: Jalankan Serial Generator

```bash
python serial_generator.py
```

### Langkah 2: Pilih Tipe Lisensi

```
🔓 Unlimited (No expiry)      → Serial tidak pernah expire
⏱️  Trial 7 Days               → Serial expire dalam 7 hari
📅 Custom Days [30]            → Serial expire dalam 30 hari
```

### Langkah 3: Generate Serial

```
Hardware ID: ABC123XYZ789
License Type: Trial 7 Days
Click: Generate Serial
Result: AV-38C9-6035-D6B3-249C
Expires: 2026-01-28
```

### Langkah 4: Kirim ke Pelanggan

Pelanggan menerima:
- Serial: `AV-38C9-6035-D6B3-249C`
- Tipe: Trial 7 hari
- Expire: 2026-01-28

---

## Cara Kerja Pelanggan

### Pertama Kali Menjalankan

```
1. Run: python Aventa_HFT_Pro_2026_v7_3_6.py
2. Lihat: Dialog aktivasi dengan Hardware ID
3. Send: Hardware ID ke admin
4. Terima: Serial dari admin
5. Paste: Serial di dialog
6. Click: Activate
7. Program: Mulai bekerja
```

### Saat Program Berjalan (7 Hari Trial)

**Hari 1-4**: 
- Program berjalan normal
- Tidak ada warning

**Hari 5-6**: 
- ⚠️ Warning: "License expires in 3 days"
- Pelanggan bisa click OK lanjutkan
- Warning muncul setiap kali start program

**Hari 8 (Sudah Expired)**:
- ❌ Error: "License has expired"
- Program tidak bisa dijalankan
- Pelanggan harus get serial baru atau upgrade

---

## Contoh Penggunaan

### Scenario 1: Trial Program

**Admin**:
```
1. Customer minta coba program
2. Generate serial dengan "Trial 7 Days"
3. Send serial ke customer
```

**Customer**:
```
Hari 1-7: Program berjalan normal, bebas coba
Hari 8: Muncul "License expired", harus bayar untuk aktivasi permanent
```

### Scenario 2: Pelanggan Baru Berlangganan 1 Bulan

**Admin**:
```
1. Customer baru bayar Rp 500.000
2. Generate serial dengan "Custom Days: 30"
3. Send serial ke customer
```

**Customer**:
```
Hari 1-27: Program berjalan normal
Hari 28-30: Muncul warning "License expires in X days"
Hari 31: License expired, harus renew untuk bulan berikutnya
```

### Scenario 3: Pelanggan Permanent

**Admin**:
```
1. Customer bayar Rp 10.000.000 selamanya
2. Generate serial dengan "Unlimited"
3. Send serial ke customer
```

**Customer**:
```
Program: Berjalan normal selamanya
Ekspiry: Tidak ada (∞)
```

---

## Data Yang Disimpan

### File Lisensi Pelanggan (Encrypted)
```json
{
  "serial": "AV-38C9-6035-D6B3-249C",
  "hardware_id": "444F6B290AAE751D",
  "activation_date": "2026-01-21",
  "expiry_date": "2026-01-28",
  "license_type": "trial",
  "expiry_days": 7,
  "status": "active",
  "version": "7.3.6"
}
```

### File Records Admin (Tracking)
```json
{
  "serial": "AV-38C9-6035-D6B3-249C",
  "hardware_id": "ABC123XYZ789",
  "generated": "2026-01-21T10:30:00",
  "license_type": "Trial (7 days)",
  "expiry_days": 7,
  "expiry_date": "2026-01-28T10:30:00",
  "activated": true
}
```

---

## Tabel License Types

| Tipe | Durasi | Ekspiry | Kapan Digunakan |
|---|---|---|---|
| Unlimited | ∞ | Tidak | Pelanggan permanent |
| Trial | 7 hari | Otomatis | Demo/coba gratis |
| 7 hari | 7 hari | Otomatis | Promo gratis seminggu |
| 14 hari | 14 hari | Otomatis | Trial 2 minggu |
| 30 hari | 30 hari | Otomatis | Subscription 1 bulan |
| 60 hari | 60 hari | Otomatis | Subscription 2 bulan |
| 90 hari | 90 hari | Otomatis | Subscription 3 bulan |
| 180 hari | 180 hari | Otomatis | Subscription 6 bulan |
| 365 hari | 365 hari | Otomatis | Subscription 1 tahun |

---

## Istilah Teknis

| Istilah | Arti |
|---|---|
| `expiry_days: -1` | Unlimited (tidak expire) |
| `expiry_days: 7` | Expire dalam 7 hari |
| `expiry_days: 30` | Expire dalam 30 hari |
| `expiry_date: null` | Tidak ada tanggal expire |
| `expiry_date: 2026-01-28` | Expire pada 28 Januari 2026 |
| `license_type: unlimited` | Lisensi permanent |
| `license_type: trial` | Trial (otomatis 7 hari) |
| `license_type: limited` | Limited (custom days) |

---

## Pesan Error/Warning

### Program Bisa Berjalan
- ✅ "License is valid" → OK
- ✅ "License expires in 5 days" → Warning tapi masih bisa jalan

### Program Tidak Bisa Berjalan
- ❌ "License has expired 3 days ago" → Sudah kadaluarsa
- ❌ "License file not found" → Belum aktivasi
- ❌ "Serial does not match hardware" → Serial untuk hardware lain

---

## Yang Baru di Update

### File `license_manager.py`
- Tambah: dukungan expiry_date
- Tambah: pengecekan tanggal kadaluarsa
- Tambah: license_type field

### File `serial_generator.py`
- Tambah: Radio button untuk pilih license type
- Tambah: Input field untuk custom days
- Tambah: Display expiry info saat generate

### File `license_check.py`
- Tambah: Display expiry date saat startup
- Tambah: Warning jika expiry ≤ 3 hari

### File Baru
- `test_expiry_system.py` - Test semua fitur expiry
- `test_integration_expiry.py` - Test end-to-end workflow
- `LICENSE_EXPIRY_SYSTEM.md` - Dokumentasi lengkap
- `LICENSE_EXPIRY_IMPLEMENTATION.md` - Detail implementasi

---

## Test Results

✅ **12 Unit Tests** - Semua PASS
- ✓ Unlimited license
- ✓ Trial license (7 hari)
- ✓ Custom license (30-90 hari)
- ✓ Expired license detection
- ✓ License type determination
- ✓ Data persistence

✅ **6 Integration Tests** - Semua PASS
- ✓ Complete trial flow
- ✓ Complete unlimited flow
- ✓ Complete custom flow
- ✓ Expiry warning detection
- ✓ License format & encryption
- ✓ Serial records tracking

**Success Rate: 100%** 🎉

---

## Cara Test Sendiri

### Test Unit Expiry
```bash
python test_expiry_system.py
```

### Test Integration Lengkap
```bash
python test_integration_expiry.py
```

### Test GUI Serial Generator
```bash
python test_serial_generator_gui.py
```

---

## Quick Reference

### Admin Generate Serial
```
python serial_generator.py
→ Pilih License Type
→ Click Generate Serial
→ Copy dan send ke customer
```

### Admin Lihat Records
```
python serial_generator.py
→ Records tab
→ Lihat semua serial yang pernah generate
```

### Customer Aktivasi
```
python Aventa_HFT_Pro_2026_v7_3_6.py
→ Lihat Hardware ID di dialog
→ Send ke admin
→ Terima serial
→ Paste serial di dialog
→ Click Activate
```

---

## FAQ

**Q: Serial saya sudah expired, apa harus beli baru?**
A: Ya, admin perlu generate serial baru dengan expiry lebih panjang.

**Q: Bisa pakai serial lain di komputer yang sama?**
A: Bisa, tapi hardware binding akan tetap cek. Serial harus untuk hardware itu.

**Q: Berapa lama maksimal custom days?**
A: Tidak ada limit, bisa 365 hari, 730 hari, dll.

**Q: Unlimited license bisa di-remove nanti?**
A: Bisa, admin delete file `license.json` di customer computer, lalu generate serial baru.

**Q: Bagaimana jika customer tidak ingat password?**
A: Tidak ada password, hanya serial number saja.

---

## Dokumentasi Lengkap

Baca file ini untuk detail:
- `LICENSE_EXPIRY_SYSTEM.md` - Panduan lengkap
- `LICENSE_QUICK_START.md` - Quick start
- `LICENSE_EXPIRY_IMPLEMENTATION.md` - Detail teknis

---

**Last Updated**: 21 Januari 2026  
**Status**: ✅ Production Ready

