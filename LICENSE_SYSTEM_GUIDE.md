# 🔐 Aventa HFT Pro 2026 - Serial Number & License System

## Ringkasan Sistem

Sistem ini memastikan bahwa:
1. ✅ Program hanya bisa digunakan setelah aktivasi serial number
2. ✅ Serial number terikat ke hardware komputer spesifik
3. ✅ Serial yang sudah diaktivasi di satu komputer tidak bisa digunakan di komputer lain
4. ✅ Data license terenkripsi dan tidak bisa di-copy ke komputer lain

---

## 🏗️ Arsitektur Sistem

### File-file yang digunakan:

1. **license_manager.py** - Core sistem license
   - `HardwareIDGenerator` - Mengidentifikasi komputer unik
   - `SerialKeyGenerator` - Membuat dan validasi serial numbers
   - `LicenseManager` - Manajemen license (save/load/verify)
   - `LicenseDialog` - UI untuk aktivasi license

2. **license_check.py** - License enforcement pada startup
   - `LicenseCheckWindow` - Splash screen & verification
   - `enforce_license_on_startup()` - Function untuk dipanggil saat program start

3. **serial_generator.py** - Admin tool untuk generate serial
   - `SerialGeneratorGUI` - Tool untuk admin generate serial numbers
   - `AdminConsole` - Console management untuk admin

---

## 🛠️ Cara Kerja Sistem

### 1. Hardware ID Generation

Hardware ID dibuat dari kombinasi:
- Machine UUID
- MAC Address
- Processor ID
- Disk Serial Number
- Hostname

```
Hardware ID = SHA256(kombinasi_hardware)[:16]
Contoh: A4F2E9B1C3D7E2F5
```

### 2. Serial Number Generation

Ketika admin ingin membuat serial untuk customer:
- Admin menggunakan `serial_generator.py`
- Customer memberikan Hardware ID mereka
- Admin generate serial number yang unik untuk hardware tersebut
- Serial format: `AV-XXXX-XXXX-XXXX-HHHH`
  - Bagian terakhir (HHHH) adalah checksum dari hardware ID

```
Serial Example: AV-8F2A-3C7B-9E1D-4F7C
```

### 3. License Activation

Ketika customer menjalankan program pertama kali:
1. Program check jika license file sudah ada
2. Jika tidak ada, tampilkan dialog activation
3. Customer masukkan serial number yang diberikan admin
4. Program validate:
   - Apakah serial valid untuk hardware ID komputer ini?
   - Apakah format serial correct?
5. Jika valid, save license file terenkripsi
6. Program bisa digunakan

### 4. License Verification

Setiap program start:
1. Baca license file yang terenkripsi
2. Decrypt menggunakan encryption key dari hardware ID
3. Verify:
   - Hardware ID dalam license sama dengan current hardware?
   - Serial number masih valid?
   - License status active?
4. Jika semua OK, jalankan program
5. Jika tidak, tampilkan error dan minta re-activation

---

## 📦 Installation & Setup

### Requirements

```bash
pip install cryptography
```

### Dependencies dalam project

- `license_manager.py` (Core)
- `license_check.py` (Integration)
- `serial_generator.py` (Admin Tool)

---

## 🚀 Implementasi di Main Program

### Step 1: Tambahkan import di awal `Aventa_HFT_Pro_2026_v7_3_6.py`

```python
# Add at the top of the file
from license_check import enforce_license_on_startup
```

### Step 2: Tambahkan license check di function `main()` atau saat GUI initialization

```python
# Before creating main window
if __name__ == "__main__":
    # ENFORCE LICENSE CHECK
    if not enforce_license_on_startup():
        print("License verification failed. Exiting...")
        sys.exit(1)
    
    # Continue with normal program startup
    root = tk.Tk()
    app = AvantaHFTGUI(root)
    root.mainloop()
```

### Step 3: Tambahkan Menu untuk License Management (Optional)

```python
# Di menu bar, tambahkan:
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)

help_menu.add_command(
    label="License Information",
    command=self.show_license_info
)
help_menu.add_command(
    label="Deactivate License",
    command=self.deactivate_license
)

# Tambahkan methods:
def show_license_info(self):
    from license_manager import LicenseManager
    manager = LicenseManager()
    license_data = manager.load_license()
    info = f"Serial: {license_data.get('serial')}\n"
    info += f"Status: {license_data.get('status')}\n"
    info += f"Activated: {license_data.get('activation_date')}"
    messagebox.showinfo("License Info", info)

def deactivate_license(self):
    from license_manager import LicenseManager
    if messagebox.askyesno("Confirm", "Deactivate license?"):
        manager = LicenseManager()
        manager.deactivate_license()
        messagebox.showinfo("Success", "License deactivated. Program will close.")
        self.root.quit()
```

---

## 👨‍💼 Untuk Admin/Reseller

### Cara Generate Serial untuk Customer

1. **Run serial generator tool:**
   ```bash
   python serial_generator.py
   ```

2. **Minta customer untuk:**
   - Run program mereka
   - Lihat Hardware ID mereka di activation dialog
   - Berikan Hardware ID ke admin

3. **Di serial generator:**
   - Paste Hardware ID di field input
   - Click "Generate Serial"
   - Dapatkan serial number
   - Kirim serial ke customer

4. **Customer:**
   - Input serial number di activation dialog
   - Click "Activate"
   - Program siap digunakan

---

## 🔒 Security Features

### 1. Hardware Binding
- Serial hanya bisa digunakan di komputer yang sesuai
- Jika user coba pindah ke komputer lain, akan error
- Hardware ID tidak bisa di-spoof (dibuat dari multiple identifiers)

### 2. Encryption
- License file dienkripsi menggunakan Fernet (symmetric encryption)
- Encryption key dibuat dari hardware ID
- License file tidak bisa dibaca/dimodifikasi tanpa hardware yang sesuai

### 3. Validation
- Setiap program start, license di-verify
- Hardware ID di-check ulang
- Serial number di-validate

### 4. File Protection
- `license.json` - Encrypted, tidak bisa di-edit manual
- `serial_records.json` - Admin records, untuk tracking

---

## 🐛 Troubleshooting

### "License file not found"
**Solusi:** Customer perlu jalankan program sekali untuk activation

### "Serial number does not match this hardware"
**Solusi:** Serial yang diberikan adalah untuk hardware lain, minta admin generate ulang

### "License is bound to a different hardware"
**Solusi:** License file sudah active di komputer lain, tidak bisa dipindah. Perlu deactivate di komputer lama atau generate serial baru

### Error decrypt license
**Solusi:** License file corrupted atau hardware berubah, delete `license.json` dan re-activate

---

## 📝 File Locations

```
Aventa_HFT_Pro_2026_v736/
├── Aventa_HFT_Pro_2026_v7_3_6.py       (Main program - EDIT untuk integrasi)
├── license_manager.py                   (Core license system)
├── license_check.py                     (License enforcement)
├── serial_generator.py                  (Admin tool)
├── license.json                         (Generated saat aktivasi - encrypted)
└── serial_records.json                  (Admin records)
```

---

## 🔄 Workflow Lengkap

### Customer End:
```
1. Download & Run Program
   ↓
2. Activation Dialog Appears
   ↓
3. Copy Hardware ID dari dialog
   ↓
4. Contact Admin dengan Hardware ID
   ↓
5. Receive Serial Number dari Admin
   ↓
6. Input Serial di dialog
   ↓
7. Click Activate
   ↓
8. License saved & encrypted
   ↓
9. Program Ready to Use ✅
```

### Admin End:
```
1. Run serial_generator.py
   ↓
2. Receive Hardware ID dari customer
   ↓
3. Paste Hardware ID di tool
   ↓
4. Click Generate Serial
   ↓
5. Send Serial ke customer
   ↓
6. Record saved otomatis
```

---

## 💡 Advanced Features (Opsional)

Jika ingin menambah fitur:

1. **License Expiry**
   - Modify `create_license()` untuk add expiry date
   - Check expiry saat verification

2. **Trial Period**
   - Generate trial serial dengan durasi terbatas
   - Check tanggal aktivasi

3. **Multi-Activation**
   - Modify system untuk allow 2-3 komputer per serial
   - Track jumlah aktivasi

4. **Online Validation**
   - Kirim activation ke server
   - Server validate dan track
   - Bisa remote deactivate jika perlu

5. **License Transfer**
   - Admin tool untuk deactivate serial dari distance
   - Customer bisa reactive di komputer baru

---

## ✅ Testing Checklist

- [ ] Test generate serial dengan berbagai Hardware ID
- [ ] Test activation dengan correct serial
- [ ] Test activation dengan wrong serial (should fail)
- [ ] Test license verification on program start
- [ ] Test copy license.json ke komputer lain (should fail)
- [ ] Test delete license.json (should require re-activation)
- [ ] Test multiple program restarts (license should persist)
- [ ] Test license info display di Help menu
- [ ] Test deactivate license function

---

## 📞 Support

Untuk issues atau pertanyaan tentang license system, hubungi admin.

License System Created: 2026-01-21
Version: 1.0
