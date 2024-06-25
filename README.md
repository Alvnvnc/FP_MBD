### **README.md**

```markdown
# Esport Database Viewer

Aplikasi Streamlit untuk menampilkan dan menganalisis data dari database esport.

## Persyaratan

Pastikan Anda memiliki perangkat lunak berikut terinstal di sistem Anda:

- Python 3.7 atau lebih baru
- MySQL Server

## Langkah-langkah Setup

### 1. Clone Repository

Clone repository ini ke direktori lokal Anda:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Membuat dan Mengaktifkan Virtual Environment

Buat dan aktifkan virtual environment untuk mengisolasi dependensi proyek:

```bash
python3 -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
venv\Scripts\activate  # Untuk Windows
```

### 3. Instal Dependensi

Instal semua dependensi yang diperlukan menggunakan `pip`:

```bash
pip install -r requirements.txt
```

### 4. Setup MySQL

Pastikan MySQL Server berjalan di sistem Anda. Anda dapat memulai MySQL Server dengan perintah berikut:

```bash
sudo service mysql start
```

### 5. Buat Database dan Tabel

Jalankan script `setup_database.py` untuk membuat database, tabel, dan memasukkan data sampel:

```bash
python setup_database.py
```

### 6. Jalankan Aplikasi

Jalankan aplikasi Streamlit:

```bash
streamlit run app.py
```

Aplikasi akan berjalan dan dapat diakses melalui web browser di alamat `http://localhost:8501`.

## Struktur Proyek

Berikut adalah struktur direktori proyek:

```
.
├── app.py
├── setup_database.py
├── requirements.txt
├── README.md
└── images
    ├── player_default.jpg
    └── team_default.jpg
```

## Konfigurasi MySQL

Pastikan Anda telah membuat pengguna MySQL dan memberikan izin yang diperlukan:

1. Masuk ke MySQL sebagai root:

```bash
sudo mysql -u root -p
```

2. Buat pengguna baru dan berikan izin:

```sql
CREATE USER 'your_name'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON esport_db.* TO 'your_name'@'localhost';
FLUSH PRIVILEGES;
```

## Isi Requirements.txt

Pastikan file `requirements.txt` Anda mencakup semua paket yang diperlukan. Berikut adalah contoh isi `requirements.txt`:

```text
streamlit
mysql-connector-python
pandas
altair
```

## Gambar Default

Pastikan Anda memiliki gambar default di direktori `images` untuk pemain dan tim:

- `images/player_default.jpg`
- `images/team_default.jpg`

Jika tidak ada gambar pemain atau tim, aplikasi akan menggunakan gambar default ini.

## Masalah dan Solusi

Jika Anda mengalami masalah saat menjalankan aplikasi, pastikan:

- Semua dependensi telah terinstal dengan benar.
- MySQL Server berjalan dan Anda dapat terhubung ke database.
- Username dan password MySQL di `setup_database.py` dan `app.py` sesuai dengan yang Anda buat.

Jika masalah berlanjut, periksa log kesalahan dan sesuaikan konfigurasi sesuai kebutuhan.

