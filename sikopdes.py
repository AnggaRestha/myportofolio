# template.py

import sys

# TODO: Ubah NAMA dan NPM dengan nama dan NPM Anda
NAMA = "Angga Restha Rustyanto"
NPM = "2506656444"


def determinant_cofactor(matrix, row=0):
    """
    Menghitung determinan matriks secara rekursif menggunakan
    ekspansi kofaktor pada baris tertentu.

    Metode ini bekerja dengan cara:

    1. Basis rekursi:
        - Jika matriks berukuran 1x1, langsung kembalikan elemen
    tersebut.
        - Jika matriks berukuran 2x2, gunakan rumus determinan
    sederhana.

    2. Rekursi:
        - Pilih baris tertentu sebagai referensi untuk ekspansi
    kofaktor.
        - Untuk setiap elemen dalam baris yang dipilih, buat
    submatriks dengan
            menghapus baris tersebut dan kolom terkait.
        - Hitung kofaktor dengan mengalikan elemen dengan (-
    1)^(baris + kolom).
        - Lakukan pemanggilan rekursif untuk menghitung determinan
    dari submatriks.
        - Jumlahkan semua hasil untuk mendapatkan determinan akhir.

    Parameter:
        - matrix (list of lists): Matriks persegi ukuran n x n.
        - row (int): Indeks baris yang digunakan untuk ekspansi
    kofaktor
          (default: 0, baris pertama).

    Output:
        - float: Nilai determinan dari matriks input.
    """
    n = len(matrix)

    # Basis rekursi: Jika matriks berukuran 1x1
    if n == 1:
        return matrix[0][0]

    # Basis rekursi: Jika matriks berukuran 2x2
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0

    ## TODO: Implementasikan fungsi ini untuk menghitung determinan
    ## secara rekursif menggunakan ekspansi kofaktor
    for col in range(n):
            submatrix = [
                r[:col] + r[col + 1:]
                for i, r in enumerate(matrix)
                if i != row
            ]
            sign = (-1) ** (row + col)
            det += sign * matrix[row][col] * determinant_cofactor(submatrix, 0)

    return det


def generate_permutations(elements):
    """
    Menghasilkan semua permutasi dari daftar elemen.

    Parameter:
        - elements (list): Daftar elemen yang akan dibuat
    permutasinya.

    Output:
        - list of lists: Daftar semua kemungkinan permutasi dari
    elemen yang diberikan.

    Contoh Penggunaan:
    >>> generate_permutations([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3],
     [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    >>> generate_permutations([42])
    [[42]]

    >>> generate_permutations([])
    [[]]
    """
    if len(elements) == 0:
        return [[]]

    permutations = []

    for i in range(len(elements)):
        rest = elements[:i] + elements[i + 1:]
        for perm in generate_permutations(rest):
            permutations.append([elements[i]] + perm)

    return permutations


def count_inversions(perm):
    """
    Menghitung jumlah inversi dalam suatu permutasi.

    Inversi terjadi ketika elemen dengan indeks lebih kecil memiliki nilai lebih besar
    dibandingkan elemen dengan indeks lebih besar.

    Parameter:
        - perm (list): Permutasi dalam bentuk daftar.

    Output:
        - int: Jumlah inversi dalam permutasi.
    """
    inversions = 0
    n = len(perm)

    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inversions += 1

    return inversions


def determinant_combinatorics(matrix):
    """
    Menghitung determinan matriks menggunakan metode permutasi
    (metode Leibniz).

    Metode ini bekerja dengan:

    1. Menghasilkan semua kemungkinan permutasi dari indeks kolom.

    2. Untuk setiap permutasi:

        - Hitung tanda permutasi berdasarkan jumlah inversi.

        - Hitung hasil kali elemen yang sesuai dengan permutasi.

        - Kalikan hasil tersebut dengan tanda permutasi.

        - Tambahkan hasil ke determinan total.

    3. Kembalikan nilai determinan akhir.

    Parameter:

    - matrix (list of lists): Matriks persegi ukuran n x n.

    Output:

    - float: Nilai determinan dari matriks input.
    """

    n = len(matrix)

    det = 0

    ## TODO: Implementasikan fungsi ini untuk menghitung determinan
    ## menggunakan metode permutasi (Leibniz).
    ## HINT: Gunakan fungsi generate_permutations dan count_inversions.
    col_indices = list(range(n))
    perms = generate_permutations(col_indices)

    for perm in perms:
        inversions = count_inversions(perm)
        sign = (-1) ** inversions
        product = 1

        for row in range(n):
            product *= matrix[row][perm[row]]

        det += sign * product

    return det


def cramer_rule(A, b, determinant_method):
    """
    Menyelesaikan Sistem Persamaan Linear (SPL) Ax = b menggunakan
    Aturan Cramer.

    Langkah-langkah metode ini:

    1. Hitung determinan matriks A menggunakan metode yang
    diberikan.

    2. Jika determinan A = 0, sistem tidak memiliki solusi unik
       dan fungsi mengembalikan None.

    3. Untuk setiap variabel:
        - Gantilah kolom ke-i dalam A dengan vektor b.
        - Hitung determinan matriks hasil penggantian.
        - Hitung solusi x_i = det(A_i) / det(A).

    4. Kembalikan daftar solusi.

    Parameter:

    - A (list of lists): Matriks koefisien ukuran n x n.
    - b (list): Vektor hasil ukuran n x 1.
    - determinant_method (function): Fungsi yang digunakan untuk
    menghitung
        determinan.

    Output:

    - list: Solusi SPL [x1, x2, ..., xn], atau None jika tidak
    memiliki
        solusi unik.
    """

    det_A = determinant_method(A)

    if det_A == 0:
        return None

    n = len(A)

    solutions = []

    ## TODO: Implementasikan fungsi ini untuk menyelesaikan SPL
    ## menggunakan Aturan Cramer
    for i in range(n):
        A_i = [row[:] for row in A]
        for r in range(n):
            A_i[r][i] = b[r]

        det_A_i = determinant_method(A_i)
        x_i = det_A_i / det_A
        solutions.append(x_i)

    return solutions


def invers_matrix(matrix):
    """
    Menghitung invers dari matriks persegi menggunakan metode
    adjoin.

    Rumus:

        A^(-1) = adj(A) / det(A)

    Metode ini bekerja dengan cara:

    1. Hitung determinan matriks.

    2. Jika determinan = 0, matriks tidak memiliki invers.

    3. Bentuk matriks kofaktor.

    4. Transpose matriks kofaktor untuk mendapatkan adjoin.

    5. Bagi setiap elemen adjoin dengan determinan.

    Parameter:

    - matrix (list of lists): Matriks persegi ukuran n x n.

    Output:

    - list of lists: Matriks invers dari input, atau None jika
    tidak ada invers.
    """

    det_A = determinant_cofactor(matrix)

    if det_A == 0:
        return None

    n = len(matrix)

    ## TODO: Implementasikan fungsi ini untuk menghitung invers
    ## matriks persegi menggunakan metode adjoin

    if n == 1:
        return [[1 / det_A]]

    cofactor_matrix = []
    for r in range(n):
        cofactor_row = []
        for c in range(n):
            submatrix = [
                row[:c] + row[c + 1:] 
                for i, row in enumerate(matrix) 
                if i != r
            ]
            cofactor_val = ((-1) ** (r + c)) * determinant_cofactor(submatrix)
            cofactor_row.append(cofactor_val)
        cofactor_matrix.append(cofactor_row)

    inv_matrix = []
    for r in range(n):
        inv_row = []
        for c in range(n):
            # Transpose: ambil elemen dari kofaktor baris c kolom r
            inv_row.append(cofactor_matrix[c][r] / det_A)
        inv_matrix.append(inv_row)

    return inv_matrix


def multiply_matrix_vector(matrix, vector):
    """
    Mengalikan matriks persegi dengan vektor.

    Parameter:

    - matrix (list of lists): Matriks persegi ukuran n x n.
    - vector (list): Vektor ukuran n x 1.

    Output:

    - list: Vektor hasil ukuran n x 1.
    """

    n = len(matrix)

    ## TODO: Implementasikan fungsi ini untuk mengalikan matriks
    ## dengan vector
    result = []
    for r in range(n):
        row_sum = 0
        for c in range(n):
            row_sum += matrix[r][c] * vector[c]
        result.append(row_sum)

    return result


while True:

    print("\n=== Sistem Sikopdes ===")

    n = int(input("Masukkan ordo matriks persegi (n): "))

    A = []

    for i in range(n):

        row = list(
            map(
                float,
                input(
                    f"Masukkan baris {i + 1} dari matriks koefisien A "
                    "(dipisah spasi): "
                ).split()
            )
        )

        A.append(row)

    b = list(
        map(
            float,
            input("Masukkan vektor hasil b (dipisah spasi): ").split()
        )
    )

    while True:

        print("\nPilih metode penyelesaian:")

        print("1. Menggunakan Determinan (Cramer)")

        print("2. Menggunakan Invers Matriks")

        print("3. Masukkan SPL baru")

        print("4. Keluar")

        metode = input("Pilihan: ")

        if metode == "1":

            print("\nPilih metode perhitungan determinan:")

            print("1. Metode Kofaktor (rekursif)")

            print("2. Metode Kombinatorik (permutaasi)")

            metode_det = input("Pilihan: ")

            if metode_det == "1":

                solutions = cramer_rule(
                    A,
                    b,
                    determinant_cofactor
                )

            elif metode_det == "2":

                solutions = cramer_rule(
                    A,
                    b,
                    determinant_combinatorics
                )

            else:

                print("Pilihan tidak valid.")

                continue

            if solutions is None:

                print(
                    "Sistem tidak memiliki solusi unik "
                    "karena determinan = 0."
                )

            else:

                print(
                    "\nHasil solusi SPL menggunakan Aturan Cramer:"
                )

                for i, sol in enumerate(solutions):

                    print(f"  x{i + 1} = {sol:.2f}")

        elif metode == "2":

            A_inv = invers_matrix(A)

            if A_inv is None:

                print(
                    "Sistem tidak memiliki solusi unik "
                    "karena determinan = 0."
                )

            else:

                solutions = multiply_matrix_vector(A_inv, b)

                print(
                    "\nHasil solusi SPL menggunakan Invers Matriks:"
                )

                for i, sol in enumerate(solutions):

                    print(f"  x{i + 1} = {sol:.2f}")

        elif metode == "3":

            break

        elif metode == "4":

            print("Program selesai.")

            sys.exit()

        else:

            print("Pilihan tidak valid.")