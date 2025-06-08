import matplotlib.pyplot as plt
from itertools import permutations
import random

class WeightedGraph:
    def __init__(self):
        self.kota = {}

    def tambah_kota(self, kota):
        self.kota[kota] = {}

    def tambah_jalur(self, k1, k2, jarak):
        self.kota[k1][k2] = self.kota[k2][k1] = jarak

    def cetak_graf(self):
        print("=== GRAF KOTA INGGRIS ===")
        print(f"Total kota: {len(self.kota)}\nTotal jalur: {sum(len(j) for j in self.kota.values()) // 2}\n")

        for kota in sorted(self.kota.keys()):
            if self.kota[kota]:
                print(f"{kota}:")
                [print(f"  -> {tetangga}: {jarak} km") for tetangga, jarak in sorted(self.kota[kota].items())]
                print()

    def dijkstra(self, awal):
        jarak = {k: float('inf') for k in self.kota}
        jarak[awal] = 0
        belum = set(self.kota.keys())
        prev = {k: None for k in self.kota}

        while belum:
            now = min(belum, key=lambda k: jarak[k])
            if jarak[now] == float('inf'):
                break
            belum.remove(now)

            for tetangga, bobot in self.kota[now].items():
                if tetangga in belum and jarak[now] + bobot < jarak[tetangga]:
                    jarak[tetangga] = jarak[now] + bobot
                    prev[tetangga] = now

        return jarak, prev

    def jalur_terpendek(self, awal, akhir):
        if awal == akhir:
            return [awal], 0

        jarak, prev = self.dijkstra(awal)
        if jarak[akhir] == float('inf'):
            return None, float('inf')

        jalur, now = [], akhir
        while now:
            jalur.append(now)
            now = prev[now]

        return jalur[::-1], jarak[akhir]

    def tsp(self):
        kota_list = list(self.kota.keys())
        if not kota_list:
            return [], float('inf')

        print(f"Menghitung TSP untuk {len(kota_list)} kota...")
        best_dist, best_route, start = float('inf'), [], kota_list[0]

        for perm in permutations(kota_list[1:]):
            route, total, valid = [start] + list(perm), 0, True

            for i in range(len(route)):
                dari, ke = route[i], route[(i + 1) % len(route)]
                if ke in self.kota[dari]:
                    total += self.kota[dari][ke]
                else:
                    valid = False
                    break

            if valid and total < best_dist:
                best_dist, best_route = total, route

        return best_route, best_dist

    def visualisasi(self, highlight=None, judul="Graf Kota Inggris"):
        pos = {
            "London": (5, 2), "Cambridge": (6, 3), "Birmingham": (5, 4), "Nottingham": (5, 5),
            "Sheffield": (6, 5), "Leeds": (6, 6), "Manchester": (5, 6), "Liverpool": (4, 6),
            "Bristol": (3, 3), "Newcastle": (6, 8)
        }

        plt.figure(figsize=(12, 8))

        for k1 in self.kota:
            for k2, jarak in self.kota[k1].items():
                if k1 < k2:
                    x1, y1, x2, y2 = *pos[k1], *pos[k2]
                    plt.plot([x1, x2], [y1, y2], 'gray', linewidth=1.5, alpha=0.7)
                    plt.text((x1+x2)/2, (y1+y2)/2, str(jarak), fontsize=8, ha='center',
                             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

        if highlight:
            for i in range(len(highlight) - 1):
                k1, k2 = highlight[i], highlight[i + 1]
                plt.plot([pos[k1][0], pos[k2][0]], [pos[k1][1], pos[k2][1]], 'blue', linewidth=3)

            if len(highlight) > 2 and highlight[0] in self.kota[highlight[-1]]:
                k1, k2 = highlight[-1], highlight[0]
                plt.plot([pos[k1][0], pos[k2][0]], [pos[k1][1], pos[k2][1]], 'blue', linewidth=3)

        for kota in self.kota:
            x, y = pos[kota]
            plt.scatter(x, y, s=500, color='red', edgecolor='black', linewidth=2)
            plt.text(x, y, kota, fontsize=9, fontweight='bold', ha='center', va='center')

        plt.title(judul, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def pilih_kota(graf, pesan="Pilih kota"):
    kota_list = sorted(graf.kota.keys())
    print(f"\n{pesan}:")
    [print(f"{i}. {kota}") for i, kota in enumerate(kota_list, 1)]

    while True:
        try:
            nomor = int(input(f"Nomor (1-{len(kota_list)}): "))
            if 1 <= nomor <= len(kota_list):
                return kota_list[nomor - 1]
            print("Nomor tidak valid!")
        except:
            print("Masukkan nomor!")

def setup():
    graf = WeightedGraph()
    kota_list = ["London", "Cambridge", "Birmingham", "Nottingham", "Sheffield", "Leeds", "Manchester", "Liverpool", "Bristol", "Newcastle"]
    jalur = [
        ('Manchester', 'Bristol', 228), ('London', 'Bristol', 158), ('London', 'Birmingham', 137),
        ('Birmingham', 'Nottingham', 121), ('Cambridge', 'Bristol', 89), ('Leeds', 'Cambridge', 172),
        ('Manchester', 'Liverpool', 113), ('London', 'Cambridge', 173), ('London', 'Manchester', 169),
        ('Leeds', 'London', 109), ('Sheffield', 'Newcastle', 72), ('Liverpool', 'Cambridge', 141),
        ('Leeds', 'Liverpool', 180), ('Cambridge', 'Manchester', 133), ('Liverpool', 'Birmingham', 152),
        ('Nottingham', 'Newcastle', 202), ('Manchester', 'Sheffield', 212), ('Newcastle', 'London', 108),
        ('Nottingham', 'Cambridge', 154), ('Newcastle', 'Liverpool', 199), ('Cambridge', 'Birmingham', 67),
        ('Sheffield', 'Birmingham', 158), ('Nottingham', 'Bristol', 229), ('Leeds', 'Nottingham', 80),
        ('Newcastle', 'Bristol', 246), ('Newcastle', 'Birmingham', 91), ('Manchester', 'Leeds', 237),
        ('Leeds', 'Bristol', 74), ('Manchester', 'Newcastle', 143), ('Nottingham', 'Liverpool', 134)
    ]

    [graf.tambah_kota(kota) for kota in kota_list]
    [graf.tambah_jalur(k1, k2, jarak) for k1, k2, jarak in jalur]
    return graf

def tampilkan_hasil(jalur, jarak, awal, akhir, graf, tipe="jalur"):
    if jalur and jarak != float('inf'):
        print(f"\nRute TSP: {' -> '.join(jalur)} -> {jalur[0]}" if tipe == "tsp" 
              else f"\n{'='*40}\nHASIL: {awal} -> {akhir}\n{'='*40}\nRute: {' -> '.join(jalur)}")
        print(f"Jarak: {jarak} km\nWaktu: {jarak / 60:.1f} jam")

        if input("\nLihat visualisasi? (y/n): ").lower() == 'y':
            judul = f"Rute TSP Optimal ({jarak} km)" if tipe == "tsp" else f"Jalur: {awal} -> {akhir} ({jarak} km)"
            graf.visualisasi(highlight=jalur, judul=judul)
    else:
        print("TSP tidak valid!" if tipe == "tsp" else "Jalur tidak ditemukan!")

def main():
    graf = setup()
    print("SISTEM PETA NAVIGASI INGGRIS\nData dimuat!")

    actions = {
        "1": lambda: (print("\nDAFTAR KOTA:"), [print(f"{i}. {kota}") for i, kota in enumerate(sorted(graf.kota.keys()), 1)]),
        "2": graf.cetak_graf,
        "4": lambda: (print("Menampilkan graf..."), graf.visualisasi())
    }

    while True:
        try:
            print(f"\n{'='*40}\nPETA NAVIGASI INGGRIS⚽🏰\n{'='*40}")
            print("1. Daftar kota\n2. Struktur graf\n3. Jalur terpendek\n4. Visualisasi graf\n5. TSP\n6. Keluar")
            print("="*40)

            pilihan = input("Pilihan: ").strip()

            if pilihan in actions:
                actions[pilihan]()
            elif pilihan == "3":
                awal, akhir = pilih_kota(graf, "Kota asal🚃"), pilih_kota(graf, "Kota tujuan📍")
                tampilkan_hasil(*graf.jalur_terpendek(awal, akhir), awal, akhir, graf)
            elif pilihan == "5":
                print("Menjalankan TSP...")
                tampilkan_hasil(*graf.tsp(), None, None, graf, "tsp")
            elif pilihan == "6":
                print("\nThank you lads!󠁧󠁢󠁥🍻")
                break
            else:
                print("Pilihan tidak valid!")

        except KeyboardInterrupt:
            print("\nProgram dihentikan.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
