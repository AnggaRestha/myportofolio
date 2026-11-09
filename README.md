Namaku : Angga Restha Rustyanto

NPM : 2506656444

Kelas : PBP C

Jawaban pertanyaan : 

Alur Permintaan (Request-Response Cycle) Django saat Membuka Halaman Portofolio :
    - Permintaan dari Browser: Pengguna mengetikkan URL atau mengklik tautan halaman portofolio di browser. Permintaan HTTP ini dikirimkan ke server Django.
    - urls.py Proyek (Root URLconf):Django menerima permintaan dan memeriksanya di urls.py tingkat proyek. Di sini, Django mencocokkan awalan (path) URL dan melempar/meneruskan penanganan URL tersebut ke urls.py milik aplikasi terkait menggunakan fungsi include().
    - urls.py Aplikasi: urls.py aplikasi mencocokkan sisa pola URL dan mengarahkannya ke fungsi atau kelas view tertentu yang bertanggung jawab menangani halaman tersebut.
    - View (views.py):View bertindak sebagai pengendali logika (controller). View akan memanggil Model jika memerlukan data dari basis data.
    - Model (models.py):Model merepresentasikan struktur data portofolio. Model melakukan kueri ke basis data (seperti mengambil daftar item portofolio, judul, deskripsi, gambar, dsb.) dan mengembalikan data tersebut ke view dalam bentuk objek /QuerySet.
    - Template (.html): View mengambil data dari Model, memasukkannya ke dalam konteks (context dictionary), lalu menyajikannya (render) bersama file Template HTML yang relevan.
    - Respon ke Browser: Django menggabungkan data dengan template HTML menjadi respon HTTP utuh, kemudian mengirimkannya kembali ke browser pengguna untuk ditampilkan.

Alasan Menyimpan Data Portofolio pada Model (Bukan Hardcode di Template) & Dampaknya:
    - Pemisahan Logika dan Tampilan (Separation of Concerns): Menyimpan data di basis data melalui Model menjaga template tetap bersih dan fokus hanya pada aspek presentasi/tampilan UI.
    - Kemudahan Pemeliharaan (Maintainability): Jika ada penambahan, perubahan, atau penghapusan data portofolio, kita cukup mengubah data di basis data (misalnya melalui Django Admin) tanpa harus menyunting file HTML secara manual.
    - Skalabilitas dan Dinamisme (Scalability):plikasi dapat menangani ratusan hingga ribuan item portofolio secara dinamis menggunakan perulangan (looping) pada template, tanpa membuat ukuran file HTML membengkak.
    - Fleksibilitas Pengolahan Data:Data yang disimpan di Model dapat dengan mudah difilter, diurutkan, dicari, atau diekspos melalui REST API jika di kemudian hari aplikasi dikembangkan ke platform lain (seperti aplikasi mobile).


Perbedaan Fungsi makemigrations dan migrate serta Contoh Perubahan Model:
    - makemigrations: Berfungsi untuk menyiapkan dan mencatat berkas migrasi baru berdasarkan perubahan yang dibuat pada file models.py. Perintah ini belum mengubah struktur tabel di dalam basis data nyata, melainkan hanya membuat blueprint/instruksi perubahan di folder migrations/.
    - migrate: Berfungsi untuk menjalankan dan mengaplikasikan berkas migrasi yang telah dibuat ke dalam basis data nyata. Perintah ini mengeksekusi perintah SQL untuk memperbarui skema/tabel basis data agar sesuai dengan model aplikasi.

Misalkan kita memiliki model Portfolio di models.py dan ingin menambahkan atribut baru tech_stack:
     python
     class Portfolio(models.Model):
         title = models.CharField(max_length=100)
         description = models.TextField()
         # Perubahan/Penambahan field baru:
         tech_stack = models.CharField(max_length=200, default="")
     
     Setelah menambahkan atribut tech_stack tersebut, Anda wajib menjalankan python manage.py makemigrations untuk membuat berkas migrasi baru, lalu diikuti dengan python manage.py migrate untuk menambahkan kolom tech_stack ke tabel basis data Anda.



TUGAS 3 :

1. Kita pakai ModelForm di Django dikarenakan dia bisa bikin kita menjadi lebih mudah dibanding pakai form HTML manual. kalo manual, kita mesti nulis pribadi semua tagnya, ngatur setiap field dan ngehandle data dari form ke model satu persatu. kalo pake ModelForm, semua otomatis di generate langsung dari model kita, input type sampe validasi.

soal {% csrf_token %}, ini wajib ditambahin karna buat protek dari serangan CSRF (pas banget ini lagi dijelasin bu ara dikelas). kalau gada token ini, situ lain bisa nyamar jadi kita dan ngirim req POST ke server kita tanpa sepengetahuan kita. initinya CSTF ini kode rahasia kita buat generate server dan dicek tiap kali form di submit.


2. JSON lebih disuka dibanding XML dikarenakan lebih ringkas, lebih gampang dibaca, dan dia native di JS. karna JSON itu basically format objek JavaScript, jadi di sisi frontend gaperlu parsing ribet, tinggal JSON.parse() langsung jadi objek yang bisa dipake


3. Alurnya kaya gini kurang lebih :
    -   User akses halaman/endpoint tertentu (misal `/api/awards/` atau `/awards/`)
    -   Fungsi view di Django manggil query ke database lewat ORM (misal `Award.objects.all()`), yang hasilnya berupa objek-objek model Python (instance dari class `Award`)
    -   Objek Python ini gak bisa langsung dikirim sebagai response HTTP, karena HTTP cuma bisa transfer data dalam bentuk teks/string. Makanya perlu proses serialization ngubah objek Python jadi format teks standar (di kasus kita, JSON) pake `serializers.serialize("json", awards)`
    -   Hasil serialize ini di-bungkus jadi `HttpResponse` dengan `content_type="application/json"`, terus dikirim balik ke browser/client
    -   Kalau datanya mau ditampilkan lagi di halaman HTML (bukan cuma buat API), kita perlu proses sebaliknya yaitu deserialization ngubah teks JSON itu balik jadi objek Python lagi (`serializers.deserialize()`), biar bisa diakses field-fieldnya (`.title`, `.description`, dst) dan ditampilin pake template Django (`{{ item.title }}`)


Tugas 5 :

1. Pengertian *Debouncing* dan Pentingnya pada Fitur Pencarian AJAX :
    Debouncing adalah teknik pemrograman yang digunakan untuk membatasi frekuensi eksekusi suatu fungsi asinkron (seperti panggilan API/AJAX) sampai ada jeda waktu tertentu setelah event terakhir dipanggil.

    pentignya adalah :
        - Mengurangi Jumlah Request ke Server
        - Meengoptimalkan Performa & Beban Server
        - Mencegah race condition

2. Fungsi `await` pada `fetch()` dan Dampak Jika Tidak Menggunakannya :
    `await` digunakan di dalam fungsi `async` untuk menghentikan sementara eksekusi kode sampai proses Promise yang dikembalikan oleh `fetch()` selesai resolved atau rejected.
    
    Fungsi Utama `await`: Memungkinkan kita menulis kode asinkron dengan gaya penulisan sinkron yang mudah dibaca, memastikan nilai kembalian dari `fetch()` Response object atau `.json()` benar-benar sudah siap digunakan sebelum baris kode berikutnya dieksekusi.

    ika Tidak Menggunakan `await`: Fungsi `fetch()` akan mengembalikan sebuah objek Promise yang berstatus pending, bukan hasil respon aktual dari server. Jika kita mencoba mengakses properti atau method dari objek tersebut tanpa `await` (misalnya mencoba melakukan `.json()`), eksekusi kode akan berlanjut secara prematur dan menghasilkan error seperti `TypeError: response.json is not a function` atau mendapatkan nilai `undefined`.


3. Pengertian Serangan XSS (Cross-Site Scripting) dan Rentannya Rendering via AJAX/JavaScript :
    Cross-Site Scripting (XSS) adalah kerentanan keamanan web di mana penyerang menyisipkan skrip JavaScript berbahaya ke dalam input data aplikasi yang nantinya dieksekusi oleh browser milik pengguna lain.

    Data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan XSS daripada data yang ditampilkan langsung melalui template Django karena:
        - Pembersihan Otomatis pada Template Django
        - Rendering Manual di JavaScript


    
Tugas 6 :

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful. Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!**

    REST (Representational State Transfer) merupakan pendekatan arsitektur untuk membangun layanan web yang memungkinkan komunikasi antara client dan server melalui resource yang diidentifikasi menggunakan URL. Sebuah API tidak otomatis disebut RESTful hanya karena menghasilkan JSON, sebab REST juga memiliki prinsip seperti komunikasi stateless, penggunaan metode HTTP sesuai fungsinya, dan antarmuka yang konsisten.

    PUT digunakan untuk mengganti representasi data suatu resource secara menyeluruh, sedangkan PATCH digunakan untuk memperbarui sebagian data saja. Sebagai contoh, pada API Awards, PUT dapat digunakan ketika seluruh informasi award ingin diperbarui, sementara PATCH lebih sesuai jika hanya ingin mengubah judul award tanpa memengaruhi field lainnya.


2. **Jelaskan peran serializer pada Django REST Framework. Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?**

    Serializer pada Django REST Framework berfungsi untuk mengubah objek model Django menjadi data yang dapat dikirim melalui API, sekaligus memvalidasi dan mengolah data yang diterima sebelum disimpan ke database.

    Dibandingkan membuat dictionary secara manual menggunakan JsonResponse, serializer membuat kode lebih terstruktur dan mudah dipelihara. Serializer juga menyediakan validasi field, pengaturan field read-only, serta integrasi langsung dengan model melalui ModelSerializer.

    Pada proyek saya, AwardSerializer digunakan untuk menentukan field yang ditampilkan, membersihkan input menggunakan strip_tags, dan menghasilkan informasi tambahan seperti star_count dan is_starred tanpa mengizinkan pengguna mengubahnya secara langsung.

3. **Jelaskan perbedaan autentikasi dan autorisasi pada Django REST Framework. Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

   Autentikasi merupakan proses untuk memastikan identitas pengguna, misalnya melalui login menggunakan username dan password. Sementara itu, autorisasi merupakan proses untuk menentukan tindakan yang boleh dilakukan pengguna setelah identitasnya diketahui.

   Pada proyek saya, autentikasi menggunakan SessionAuthentication, sedangkan autorisasi diterapkan melalui permission class. Pengunjung hanya dapat membaca data, pengguna biasa dapat memberikan star, Editor dapat memperbarui data, dan superuser memiliki akses penuh untuk mengelola data.

   Pemeriksaan permission harus dilakukan di server karena menyembunyikan tombol pada template hanya memengaruhi tampilan. Pengguna masih dapat mengirim request secara langsung melalui API. Dengan permission class, server tetap dapat menolak tindakan yang tidak sesuai dengan hak akses pengguna.

4. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication. Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**

   Token CSRF diperlukan untuk melindungi pengguna dari serangan Cross-Site Request Forgery, yaitu kondisi ketika situs lain mencoba mengirim permintaan yang mengubah data menggunakan sesi login pengguna tanpa persetujuannya. Pada SessionAuthentication, browser menggunakan cookie sesi untuk mengenali pengguna sehingga request yang mengubah data, seperti POST, PUT, PATCH, dan DELETE, perlu dilindungi dengan pemeriksaan CSRF.

   Pengujian menggunakan force_authenticate tidak cukup untuk membuktikan perlindungan tersebut karena metode ini mengatur autentikasi pengguna secara langsung dan melewati proses autentikasi sesi yang normal, termasuk pemeriksaan CSRF.

   Oleh karena itu, pengujian perlu menggunakan APIClient dengan enforce_csrf_checks=True dan login() untuk membuat sesi autentikasi. Pengujian dilakukan dengan memastikan request tanpa token CSRF ditolak, sedangkan request menggunakan token CSRF yang valid dapat diproses sesuai permission pengguna.

