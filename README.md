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