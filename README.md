<div align="center">

# ✨ Credit utama: [github.com/prismalaster](https://github.com/prismalaster) ✨

</div>

---

# Solana SPL Token Drain Script

Script Python untuk mentransfer seluruh saldo token SPL dari satu akun ke akun lain secara otomatis di blockchain Solana.

---

## 🚀 Fitur
- Transfer otomatis seluruh saldo token SPL dari satu akun ke akun tujuan.
- Support auto-create token account jika belum ada.
- Konfigurasi mudah via file `data.json`.
- Bisa custom interval cek saldo.
- Support custom payer (untuk fee/gas).

---

## 📦 Persyaratan
- Python 3.8+
- Library: `solana`, `solders`, `spl-token` (solana-py), `argparse`

Install dependensi:
```bash
pip install solana solders spl-token argparse
```

---

## ⚙️ Konfigurasi
Edit file `data.json` :
```json
{
  "rpc": "https://api.mainnet-beta.solana.com", // endpoint RPC Solana
  "payer": [..], // private key array untuk membayar fee (opsional, bisa diisi via argumen)
  "receiver": "", // public key tujuan
  "interval": 1 // interval cek saldo (detik)
}
```

---

## 🛠️ Cara Pakai
Jalankan script dengan perintah berikut:

```bash
python draintoken.py [PRIVATE_KEY_SOURCE] [TOKEN_MINT_ADDRESS] [--token-account-index INDEX] [--create-sccount] [--payer PRIVATE_KEY_PAYER] [--receiver RECEIVER_ADDRESS]
```

### Contoh:
```bash
python draintoken.py "[1,2,3,...]" "So11111111111111111111111111111111111111112" --receiver "Soladdresstarget"
```

- **[PRIVATE_KEY_SOURCE]**: Private key array dari akun sumber (format: "[1,2,3,...]")
- **[TOKEN_MINT_ADDRESS]**: Alamat mint token SPL (contoh: So111... untuk SOL wrapped)
- **--token-account-index**: (opsional) Index token account (default: 0)
- **--create-sccount**: (opsional) Auto create token account jika belum ada
- **--payer**: (opsional) Private key array untuk membayar fee
- **--receiver**: (opsional) Public key tujuan (override dari file json)

---

## 📝 Penjelasan Script
- Script akan terus memantau saldo token pada akun sumber.
- Jika saldo > 0, maka seluruh saldo akan langsung ditransfer ke akun tujuan.
- Jika token account tujuan belum ada, script akan otomatis membuatkan (jika pakai --create-account).
- Semua parameter bisa diatur via argumen atau file json.

---

## ⚠️ Disclaimer
- **Gunakan script ini dengan tanggung jawab penuh.**
- Pastikan private key dan data sensitif Anda aman.
- Script ini hanya untuk edukasi dan riset.

---

<div align="center">

✨ Credit utama: [github.com/prismalaster](https://github.com/prismalaster) ✨

</div> 