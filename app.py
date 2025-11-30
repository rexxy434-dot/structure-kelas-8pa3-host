from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import os  # Tambahkan ini untuk production

app = Flask(__name__)
app.secret_key = 'spider_theme_secret_key_2025'  # Kunci rahasia untuk session

# Template untuk halaman login
login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Struktur Kelas8PA3</title>
    <style>
        body {
            font-family: 'Creepster', cursive;
            text-align: center;
            background: radial-gradient(circle, #000 1px, transparent 1px), #000;
            background-size: 20px 20px;
            color: #fff;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 30px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            animation: fadeIn 2s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: #ff0000;
            text-shadow: 0 0 10px #ff0000;
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #ff0000; }
            to { text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000; }
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ff0000;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
        }
        button {
            background: #ff0000;
            color: #fff;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background: #cc0000; }
        .error { color: #ff4500; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Login ke Struktur Kelas8PA3</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="error">{{ messages[0] }}</div>
            {% endif %}
        {% endwith %}
    </div>
</body>
</html>
"""

# Template utama (halaman struktur kelas)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Struktur Kelas8PA3 - Tema Jam Laba-Laba</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"> <!-- Untuk ikon -->
    <style>
        body {
            font-family: 'Creepster', cursive; /* Font seram-keren */
            text-align: center;
            background: radial-gradient(circle, #000 1px, transparent 1px), #000; /* Hitam bintik-bintik putih */
            background-size: 20px 20px; /* Ukuran bintik */
            color: #fff;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        .container {
            max-width: 700px;
            margin: 50px auto;
            padding: 30px;
            background: rgba(0, 0, 0, 0.8); /* Semi-transparan untuk efek misterius */
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); /* Glow merah */
            position: relative;
            animation: fadeIn 2s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: #ff0000;
            text-shadow: 0 0 10px #ff0000;
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #ff0000; }
            to { text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000; }
        }
        h2, h3 { color: #ddd; }
        p { font-size: 18px; margin: 10px 0; }
        ul { list-style-type: none; padding: 0; }
        li {
            margin: 15px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        li:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
        }
        .icon { margin-right: 10px; color: #ff4500; }
        .jabatan-desc {
            font-size: 16px;
            color: #ccc;
            margin-top: 5px;
            display: none; /* Sembunyikan secara default */
        }
        li:hover .jabatan-desc {
            display: block; /* Tampilkan saat hover */
        }
        
        /* Jam Real-Time */
        #clock {
            font-size: 24px;
            color: #ff0000;
            margin: 20px 0;
            text-shadow: 0 0 5px #ff0000;
        }
        
        /* Animasi Laba-Laba (7 laba-laba) */
        .spider {
            position: absolute;
            font-size: 30px;
            color: #000;
            animation: crawl 10s linear infinite;
        }
        .spider:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
        .spider:nth-child(2) { top: 20%; left: 20%; animation-delay: 1s; }
        .spider:nth-child(3) { top: 30%; left: 30%; animation-delay: 2s; }
        .spider:nth-child(4) { top: 40%; left: 40%; animation-delay: 3s; }
        .spider:nth-child(5) { top: 50%; left: 50%; animation-delay: 4s; }
        .spider:nth-child(6) { top: 60%; left: 60%; animation-delay: 5s; }
        .spider:nth-child(7) { top: 70%; left: 70%; animation-delay: 6s; }
        @keyframes crawl {
            0% { left: 10%; top: 10%; }
            25% { left: 80%; top: 20%; }
            50% { left: 60%; top: 70%; }
            75% { left: 20%; top: 80%; }
            100% { left: 10%; top: 10%; }
        }
        
        /* Tombol Toggle Mode */
        #toggle-mode {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff0000;
            color: #fff;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        #toggle-mode:hover { background: #cc0000; }
        
        /* Audio */
        audio { display: none; } /* Sembunyikan, kontrol via JS */
        #music-toggle {
            position: fixed;
            top: 70px;
            right: 20px;
            background: #ff4500;
            color: #fff;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        
        /* Tombol Logout */
        #logout {
            position: fixed;
            top: 120px;
            right: 20px;
            background: #ff4500;
            color: #fff;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <button id="toggle-mode">Toggle Mode Gelap/Terang</button>
    <button id="music-toggle">Play/Pause Musik</button>
    <button id="logout" onclick="window.location.href='/logout'">Logout</button>
    <audio id="bg-music" loop>
        <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.wav" type="audio/wav"> <!-- Musik jam tua, ganti jika perlu -->
    </audio>
    
    <!-- 7 Laba-Laba Animasi -->
    <div class="spider">🕷️</div>
    <div class="spider">🕷️</div>
    <div class="spider">🕷️</div>
    <div class="spider">🕷️</div>
    <div class="spider">🕷️</div>
    <div class="spider">🕷️</div>
    <div class="spider">🕷️</div>
    
    <div class="container">
        <h1>Struktur Kelas8PA3</h1>
        <h2>SMPS Nurul Ilmi</h2>
        <p><strong>Waktu Berlaku:</strong> 2025-2025</p>
        <p><strong>Dibuat oleh:</strong> Muhammad Lutfi Lubis</p>
        <div id="clock"></div> <!-- Jam Real-Time -->
        <h3>Jabatan dan Nama:</h3>
        <ul>
            <li><i class="fas fa-crown icon"></i><strong>Wali Kelas:</strong> Muhammad Iqbal
                <div class="jabatan-desc">Bertanggung jawab atas pengelolaan kelas, pembelajaran, dan kesejahteraan siswa. Mengkoordinasi dengan guru lain dan orang tua.</div>
            </li>
            <li><i class="fas fa-star icon"></i><strong>Ketua Kelas:</strong> Adit
                <div class="jabatan-desc">Memimpin kegiatan kelas, mengkoordinasi siswa, dan mewakili kelas dalam acara sekolah.</div>
            </li>
            <li><i class="fas fa-star icon"></i><strong>Wakil Ketua Kelas:</strong> Al Fadli
                <div class="jabatan-desc">Membantu ketua kelas dalam tugas-tugas kepemimpinan dan menggantikan ketua jika diperlukan.</div>
            </li>
            <li><i class="fas fa-book icon"></i><strong>Sekretaris:</strong> Fazri
                <div class="jabatan-desc">Mengurus administrasi kelas, seperti catatan rapat, absensi, dan dokumentasi kegiatan.</div>
            </li>
            <li><i class="fas fa-pen icon"></i><strong>Wakil Sekretaris:</strong> Abil
                <div class="jabatan-desc">Membantu sekretaris dalam tugas administrasi dan menggantikan sekretaris jika diperlukan.</div>
            </li>
            <li><i class="fas fa-wallet icon"></i><strong>Bendahara:</strong> Nazri
                <div class="jabatan-desc">Mengurus keuangan kelas, seperti pengumpulan iuran, pembelian perlengkapan, dan laporan keuangan.</div>
            </li>
            <li><i class="fas fa-coins icon"></i><strong>Wakil Bendahara:</strong> Barka
                <div class="jabatan-desc">Membantu bendahara dalam pengelolaan keuangan dan menggantikan bendahara jika diperlukan.</div>
            </li>
            <li><i class="fas fa-shield-alt icon"></i><strong>Keamanan:</strong> Evan Zaky
                <div class="jabatan-desc">Bertanggung jawab atas keamanan dan ketertiban di kelas, mencegah gangguan, menjaga lingkungan belajar yang aman, dan melaporkan masalah keamanan kepada wali kelas.</div>
            </li>
        </ul>
    </div>
    
    <script>
        // Jam Real-Time
        function updateClock() {
            const now = new Date();
            const time = now.toLocaleTimeString();
            document.getElementById('clock').innerText = 'Waktu Sekarang: ' + time;
        }
        setInterval(updateClock, 1000);
        updateClock();
        
        // Toggle Mode Gelap/Terang
        document.getElementById('toggle-mode').addEventListener('click', function() {
            document.body.classList.toggle('light-mode');
            if (document.body.classList.contains('light-mode')) {
                document.body.style.background = 'url(https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80) no-repeat center center fixed'; // Gambar terang
                document.body.style.color = '#000';
            } else {
                document.body.style.background = 'radial-gradient(circle, #000 1px, transparent 1px), #000'; // Kembali ke hitam bintik-bintik putih
                document.body.style.backgroundSize = '20px 20px';
                document.body.style.color = '#fff';
            }
        });
        
        // Toggle Musik
        const music = document.getElementById('bg-music');
        document.getElementById('music-toggle').addEventListener('click', function() {
            if (music.paused) {
                music.play();
                this.innerText = 'Pause Musik';
            } else {
                music.pause();
                this.innerText = 'Play Musik';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template_string(html_template)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'kelas 8pa3' and password == 'class 8pa3':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Username atau password salah!')
            return redirect(url_for('login'))
    return render_template_string(login_template)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Siap untuk production
