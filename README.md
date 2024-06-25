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

#### Buat Pengguna MySQL dan Database

1. Masuk ke MySQL sebagai root:

    ```bash
    sudo mysql -u root -p
    ```

2. Buat pengguna baru dan berikan izin:

    ```sql
    CREATE USER 'your_name'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON *.* TO 'your_name'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```

3. Buat database `esport_db`:

    ```sql
    CREATE DATABASE esport_db;
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

Aplikasi akan berjalan dan dapat diakses melalui web browser di alamat [http://localhost:8501](http://localhost:8501).

## Struktur Proyek

Berikut adalah struktur direktori proyek:

```
.
├── app.py
├── setup_database.py
├── input.py
├── esport.sql
├── requirements.txt
├── README.md
└── images
    ├── player_default.jpg
    └── team_default.jpg
```

### Penjelasan Struktur Proyek

- `app.py`: File utama untuk menjalankan aplikasi Streamlit.
- `setup_database.py`: Script untuk membuat database dan tabel, serta memasukkan data sampel.
- `input.py`: Modul yang berisi fungsi untuk menangani input data.
- `esport.sql`: File SQL yang berisi perintah untuk membuat struktur database.
- `requirements.txt`: Daftar dependensi Python yang diperlukan.
- `README.md`: File dokumentasi ini.
- `images/`: Direktori yang berisi gambar default untuk pemain dan tim.

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

## Menghapus Database

Jika Anda ingin menghapus database dan semua tabel di dalamnya, jalankan `delete.py`:

```bash
python delete.py
```

## License

Proyek ini dilisensikan di bawah lisensi MIT. Lihat file LICENSE untuk detailnya.
```

Penjelasan:
- **Persyaratan**: Menjelaskan perangkat lunak yang harus terinstal.
- **Langkah-langkah Setup**: Instruksi untuk mengkloning repository, membuat virtual environment, menginstal dependensi, setup MySQL, membuat database dan tabel, serta menjalankan aplikasi.
- **Struktur Proyek**: Menyediakan gambaran umum tentang struktur direktori proyek.
- **Isi Requirements.txt**: Menyebutkan dependensi yang diperlukan.
- **Gambar Default**: Menjelaskan kebutuhan gambar default.
- **Masalah dan Solusi**: Memberikan langkah-langkah pemecahan masalah.
- **Menghapus Database**: Instruksi untuk menghapus database jika diperlukan.
- **License**: Informasi lisensi proyek.
