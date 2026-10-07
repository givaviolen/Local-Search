import random
import math
import time

# ==========================================
# 1. REPRESENTASI STATE DAN FUNGSI HEURISTIC
# ==========================================

import random
import math
# Fungsi untuk menghitung nilai h (jumlah pasangan ratu yang saling menyerang)
# Sesuai dengan definisi pada slide [cite: 120]
def objective_function(board):
    h = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            # Cek serangan pada baris yang sama (horizontal) dan diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                h += 1
    return h

# Fungsi untuk membuat state awal secara acak
def create_random_board(size=8):
    return [random.randint(0, size - 1) for _ in range(size)]


def display_board(board):
    """Menampilkan papan catur 8x8."""
    for row in range(8):
        line = ""
        for col in range(8):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()


# ==========================================
# 2. HILL-CLIMBING SEARCH
# ==========================================

def hill_climbing(verbose=True):
    """
    Memilih tetangga terbaik dengan heuristic terkecil.
    Berhenti jika solusi ditemukan atau terjebak
    pada local minimum.
    """
    current_board = create_random_board()
    current_h = objective_function(current_board)
    steps = 0

    if verbose:
        print("Initial board:", current_board, "with h =", current_h)

    while current_h != 0:
        best_neighbor = current_board.copy()
        best_neighbor_h = current_h

        # Mencari semua kemungkinan tetangga
        for col in range(8):
            for row in range(8):
                if current_board[col] == row:
                    continue

                neighbor = current_board.copy()
                neighbor[col] = row
                h = objective_function(neighbor)

                # Memilih tetangga yang lebih baik
                if h < best_neighbor_h:
                    best_neighbor_h = h
                    best_neighbor = neighbor

        # Tidak ada tetangga yang lebih baik
        if best_neighbor_h >= current_h:
            if verbose:
                print("Stuck at local minimum.")
                print("Final board:", current_board, "with h =", current_h)
            return current_board, current_h, steps

        # Pindah ke tetangga terbaik
        current_board = best_neighbor
        current_h = best_neighbor_h
        steps += 1

        if verbose:
            print("Moved to board:", current_board, "with h =", current_h)

    if verbose:
        print("Solution found!")
        print("Final board:", current_board, "with h =", current_h)

    return current_board, current_h, steps


# ==========================================
# 3. SIMULATED ANNEALING
# ==========================================

def simulated_annealing(temp=1000, cooling_rate=0.995,
                        verbose=True):
    """
    Memungkinkan perpindahan yang lebih buruk
    berdasarkan probabilitas dan suhu.
    """
    current_board = create_random_board()
    current_h = objective_function(current_board)
    t = 0

    if verbose:
        print("Initial board:", current_board, "with h =", current_h)

    while temp > 0.1:
        t += 1

        # Pilih tetangga secara acak
        next_board = current_board.copy()
        col = random.randint(0, 7)
        row = random.randint(0, 7)
        next_board[col] = row

        next_h = objective_function(next_board)
        delta_h = next_h - current_h

        # Terima langkah yang lebih baik
        if delta_h < 0:
            current_board = next_board
            current_h = next_h

        # Terima langkah yang sama atau lebih buruk
        else:
            probability = math.exp(-delta_h / temp)

            if random.random() < probability:
                current_board = next_board
                current_h = next_h

        # Turunkan suhu
        temp *= cooling_rate

        if verbose and t % 100 == 0:
            print(
                f"Iteration {t}: temp={temp:.2f}, "
                f"board={current_board}, h={current_h}"
            )

        # Berhenti jika solusi ditemukan
        if current_h == 0:
            if verbose:
                print(f"Solution found after {t} iterations!")
                print("Final board:", current_board, "with h =", current_h)
            return current_board, current_h, t

    if verbose:
        print("Search ended.")
        print("Final board:", current_board, "with h =", current_h)

    return current_board, current_h, t


# ===============================
# 4. RANDOM-RESTART HILL-CLIMBING
# ===============================

def random_restart_hill_climbing(max_restarts=100):
    """
    Menjalankan Hill-Climbing berulang kali
    dengan state awal yang berbeda.
    """
    total_steps = 0

    for restart in range(1, max_restarts + 1):
        board, h, steps = hill_climbing(verbose=False)
        total_steps += steps

        if h == 0:
            return board, h, restart, total_steps

    return board, h, max_restarts, total_steps


# ==========================================
# 5. PERCOBAAN PERBANDINGAN 10 KALI
# ==========================================

def compare_algorithms(trials=10):
    print("\n" + "=" * 65)
    print("PERCOBAAN PERBANDINGAN HILL-CLIMBING DAN SIMULATED ANNEALING")
    print("=" * 65)

    hc_success = 0
    sa_success = 0
    hc_total_time = 0
    sa_total_time = 0
    hc_total_h = 0
    sa_total_h = 0

    print(f"{'No':<5}{'HC h':<12}{'HC Waktu':<15}"
          f"{'SA h':<12}{'SA Waktu':<15}")

    for i in range(1, trials + 1):
        # Hill-Climbing
        start = time.perf_counter()
        hc_board, hc_h, hc_steps = hill_climbing(verbose=False)
        hc_time = time.perf_counter() - start

        # Simulated Annealing
        start = time.perf_counter()
        sa_board, sa_h, sa_steps = simulated_annealing(
            verbose=False
        )
        sa_time = time.perf_counter() - start

        if hc_h == 0:
            hc_success += 1

        if sa_h == 0:
            sa_success += 1

        hc_total_time += hc_time
        sa_total_time += sa_time
        hc_total_h += hc_h
        sa_total_h += sa_h

        print(f"{i:<5}{hc_h:<12}{hc_time:<15.6f}"
              f"{sa_h:<12}{sa_time:<15.6f}")

    print("-" * 65)
    print("HASIL AKHIR")
    print(f"Total percobaan              : {trials}")
    print(f"Keberhasilan Hill-Climbing   : {hc_success}/{trials}")
    print(f"Keberhasilan Simulated Annealing: {sa_success}/{trials}")
    print(f"Rata-rata heuristic HC       : {hc_total_h / trials:.2f}")
    print(f"Rata-rata heuristic SA       : {sa_total_h / trials:.2f}")
    print(f"Rata-rata waktu HC           : {hc_total_time / trials:.6f} detik")
    print(f"Rata-rata waktu SA           : {sa_total_time / trials:.6f} detik")


# ==========================================
# 6. PENGUJIAN PARAMETER SIMULATED ANNEALING
# ==========================================

def test_parameters(trials=5):
    print("\n" + "=" * 65)
    print("PENGUJIAN PARAMETER SIMULATED ANNEALING")
    print("=" * 65)

    configurations = [
        (100, 0.90),
        (500, 0.95),
        (1000, 0.995),
        (2000, 0.999)
    ]

    print(f"{'Temp':<10}{'Cooling':<12}{'Success':<12}"
          f"{'Avg h':<12}{'Avg Time (s)':<15}")

    for temp, cooling_rate in configurations:
        success = 0
        total_h = 0
        total_time = 0

        for _ in range(trials):
            start = time.perf_counter()

            board, h, steps = simulated_annealing(
                temp=temp,
                cooling_rate=cooling_rate,
                verbose=False
            )

            elapsed = time.perf_counter() - start

            if h == 0:
                success += 1

            total_h += h
            total_time += elapsed

        print(
            f"{temp:<10}{cooling_rate:<12}"
            f"{success}/{trials:<10}"
            f"{total_h / trials:<12.2f}"
            f"{total_time / trials:<15.6f}"
        )


# ==========================================
# 7. RANDOM-RESTART (TUGAS OPSIONAL)
# ==========================================

def test_random_restart(trials=10, max_restarts=100):
    print("\n" + "=" * 65)
    print("RANDOM-RESTART HILL-CLIMBING")
    print("=" * 65)

    success = 0
    total_restarts = 0
    total_time = 0

    for i in range(1, trials + 1):
        start = time.perf_counter()

        board, h, restarts, steps = random_restart_hill_climbing(
            max_restarts=max_restarts
        )

        elapsed = time.perf_counter() - start

        if h == 0:
            success += 1

        total_restarts += restarts
        total_time += elapsed

        print(
            f"Percobaan {i}: h={h}, "
            f"restarts={restarts}, waktu={elapsed:.6f} detik"
        )

    print("-" * 65)
    print(f"Keberhasilan: {success}/{trials}")
    print(f"Rata-rata restart: {total_restarts / trials:.2f}")
    print(f"Rata-rata waktu: {total_time / trials:.6f} detik")


# ==========================================
# 8. PROGRAM UTAMA
# ==========================================

if __name__ == "__main__":

    # Demonstrasi Hill-Climbing
    print("\n--- Running Hill-Climbing Search ---")
    hc_board, hc_h, hc_steps = hill_climbing()
    print("Jumlah langkah:", hc_steps)
    print("Papan akhir:")
    display_board(hc_board)

    # Demonstrasi Simulated Annealing
    print("\n--- Running Simulated Annealing Search ---")
    sa_board, sa_h, sa_steps = simulated_annealing()
    print("Jumlah iterasi:", sa_steps)
    print("Papan akhir:")
    display_board(sa_board)

    # Percobaan perbandingan
    compare_algorithms(trials=10)

    # Pengujian parameter
    test_parameters(trials=5)

    # Tugas tambahan opsional
    test_random_restart(trials=10, max_restarts=100)
    