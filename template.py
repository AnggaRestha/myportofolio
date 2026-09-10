EPS = 1e-10

def gauss_jordan(M):
    pivot_row = 0
    n_rows = len(M)
    n_vars = len(M[0]) - 1

    for col in range(n_vars):
        pivot = None
        for r in range(pivot_row, n_rows):
            if abs(M[r][col]) > EPS:
                pivot = r
                break

        if pivot is None:
            continue

        # TODO 1: tukar baris pivot dengan pivot_row
        M[pivot_row], M[pivot] = M[pivot], M[pivot_row]

        pivot_value = M[pivot_row][col]

        # TODO 2: normalisasi seluruh baris pivot
        
        for c in range(len(M[pivot_row])):
            M[pivot_row][c] /= pivot_value

        for r in range(n_rows):
            if r == pivot_row:
                continue
            factor = M[r][col]
            # TODO 3: eliminasi seluruh entri pada baris r
            # dengan Rr <- Rr - factor * Rpivot
            for c in range(len(M[r])):
                M[r][c] -= factor * M[pivot_row][c]

        pivot_row += 1
        if pivot_row == n_rows:
            break

    return M

# TODO 4: Masukkan matriks augmented-nya

M = [
    [1,  1, -1,  0],
    [4,  0, 10, 38],
    [0,  6, 10, 36]
]

for row in gauss_jordan(M):
    print(row)