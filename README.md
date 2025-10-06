# 8-Puzzle-Solver
Aplikasi 8-Puzzle Sovler yang berisikan minigames klasik yang dimana bisa diselesaikan secara manual ataupun dengan bantuan fitur auto solve yang menggunakan algoritma HC (Hill Climbing).

## Fitur Aplikasi
- Antarmuka GUI interaktif dengan gerakan tile / ubin visual
- Pemecahan puzzle manual dengan mengklik tile/ ubin
- Solver algoritma hill climbing secara otomatis
- Beberapa contoh puzzle untuk dipilih atau random
- Visualisasi solusi per langkah
- Support kustom puzzle
  
## Syarat Aplikasi
- Python 3.x
- tkinter (biasanya sudah termasuk dengan Python)
- PIL (Pillow) untuk pemrosesan gambar
```bash
pip install Pillow
```

## Instalasi / Cara Menggunakan Aplikasi
```bash
cd https://github.com/Starscream-14/8-puzzle-solver.git
python main.py
```

## Struktur File
8-puzzle/
├── main.py              # File / Aplikasi Utama
├── gui.py               # GUI dan Game Logic
├── hc.py                # Algoritma Puzzle
├── var.py               # Variabel Puzzle
├── picture/
│   └── puzzle.jpg       # Gambar Puzzle (Bisa Custom)

### Menu Game
- **Play**: Memulai permainan
- **Rules**: Lihat tata cara permainan
- **Exit**: Keluar aplikasi

### Menu In Game
- **Klik tile**: Pindahkan tile yang berdekatan ke ruang kosong
- **Restart**: Reset puzzle ke keadaan awal
- **Solve Step**: Tampilkan satu langkah optimal
- **Auto Solve**: Gunakan algoritma hill climbing untuk menyelesaikan secara otomatis
- **Random**: Beralih ke contoh puzzle berbeda
