# Bellman-Ford Algoritması ile En Kısa Yol Bulma

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Düğüm sayısı
        self.edges = []    # Kenar listesi

    def add_edge(self, u, v, w):
        self.edges.append([u, v, w])

    def bellman_ford(self, src):
        # Başlangıç mesafelerini sonsuz olarak ayarla
        dist = [float("Inf")] * self.V
        dist[src] = 0

        # Düğüm sayısı - 1 kez kenarları güncelle
        for _ in range(self.V - 1):
            for u, v, w in self.edges:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        # Negatif ağırlıklı döngü kontrolü
        for u, v, w in self.edges:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Graf negatif ağırlıklı bir döngü içeriyor!")
                return

        # Sonuçları yazdır
        print("Düğüm   Mesafe")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))



# Örnek grafikler
def create_example_graph(choice):
    if choice == 1:
        g = Graph(5)
        g.add_edge(0, 1, -1)
        g.add_edge(0, 2, 4)
        g.add_edge(1, 2, 3)
        g.add_edge(1, 3, 2)
        g.add_edge(1, 4, 2)
        g.add_edge(3, 2, 5)
        g.add_edge(3, 1, 1)
        g.add_edge(4, 3, -3)
        src = 0
    elif choice == 2:
        g = Graph(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 7)
        g.add_edge(2, 3, -2)
        g.add_edge(3, 0, 6)
        src = 1
    elif choice == 3:
        g = Graph(3)
        g.add_edge(0, 1, 3)
        g.add_edge(1, 2, 4)
        g.add_edge(2, 0, -8)
        src = 2
    else:
        print("Geçersiz seçim!")
        return None, None
    return g, src


if __name__ == '__main__':
    print("Graf Seçenekleri:")
    print("1. Örnek 1: 5 düğüm, negatif kenarlarla")
    print("2. Örnek 2: 4 düğüm, küçük bir grafik")
    print("3. Örnek 3: 3 düğüm, negatif ağırlıklı döngü içeriyor")
    
    choice = int(input("Bir grafik seçin (1, 2 veya 3): "))
    
    g, src = create_example_graph(choice)
    
    if g:
        print(f"\nSeçilen grafikte başlangıç düğümü: {src}")
        g.bellman_ford(src)
        
# Kullanıcıdan girdi alma
# if __name__ == '__main__':
#     V = int(input("Düğüm sayısını girin: "))
#     E = int(input("Kenar sayısını girin: "))

#     g = Graph(V)

#     print("Kenarları girin (kaynak hedef ağırlık):")
#     for _ in range(E):
#         u, v, w = map(int, input().split())
#         g.add_edge(u, v, w)

#     src = int(input("Başlangıç düğümünü girin: "))

#     g.bellman_ford(src)
    