import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import cv2
import os

# Bellman-Ford algoritması (adım adım kenar gevşetme)
def bellman_ford(graph, num_nodes, start_node):
    # Başlangıçta tüm düğümleri sonsuz (∞) mesafeyle başlat
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start_node] = 0  # Kaynak düğüm 0 mesafede

    # Tüm adımların mesafelerini kaydedeceğimiz liste
    steps = []
    edges_in_steps = []  # Her adımda işlenen kenarlar
    explanations = []    # Her adımın açıklaması

    # Kenar gevşetme işlemi |V|-1 kez
    for iteration in range(num_nodes - 1):
        for u, v, w in graph:
            explanation = f"Adım {len(steps)+1}: Kenar {u} -> {v} ağırlık {w} kontrol ediliyor. "
            old_distance = distances[v]

            # Gevşetme işlemi (relaxation)
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                explanation += f"Düğüm {v} mesafesi {old_distance} iken {distances[v]} olarak güncellendi."
            else:
                explanation += f"Düğüm {v} için güncelleme gerekmedi."

            # Adımın verilerini kaydet
            steps.append(distances.copy())
            edges_in_steps.append([(u, v)])  # İşlenen kenarı kaydet
            explanations.append(explanation)

    # Negatif ağırlıklı döngü kontrolü
    for u, v, w in graph:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            print("Negatif ağırlıklı döngü tespit edildi!")
            explanations.append("Negatif ağırlıklı döngü bulundu!")
            return steps, edges_in_steps, explanations, True

    return steps, edges_in_steps, explanations, False

# Adım adım tabloyu göstermek için fonksiyon
def display_steps(steps, num_nodes):
    df = pd.DataFrame(steps)
    df.columns = [f'Düğüm {i}' for i in range(num_nodes)]
    df.index = [f'Adım {i+1}' for i in range(len(steps))]

    # Sonsuzlukları '∞' ile değiştir
    df.replace(float('inf'), '∞', inplace=True)

    # Tabloyu terminalde göster
    print(df)

# Her adımı görsel olarak kaydet ve sonrasında video oluştur
def plot_graph_and_save_video(graph, num_nodes, steps, edges_in_steps, explanations, video_filename="bellman_ford_output.mp4"):
    G = nx.DiGraph()

    for u, v, w in graph:
        G.add_edge(u, v, weight=w)

    pos = nx.shell_layout(G)  # Grafiğin düzenini sizin kodunuzdaki gibi ayarladık

    img_dir = 'bellman_ford_images'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    else:
        # Önceki görselleri temizle
        for file in os.listdir(img_dir):
            file_path = os.path.join(img_dir, file)
            os.remove(file_path)

    for step, distances in enumerate(steps):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.clear()  # Önceki grafiği temizle

        # Kenarları ve düğümleri çiz
        nx.draw(G, pos, with_labels=False, node_color='lightblue', ax=ax, node_size=1000)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=12)

        # Düğüm etiketlerini güncelle (düğüm adı ve mesafesi)
        node_labels = {}
        for node in range(num_nodes):
            dist = distances[node]
            if dist < float('inf'):
                node_labels[node] = f'{node}\n{dist}'
            else:
                node_labels[node] = f'{node}\n∞'

        # Düğüm etiketlerini çiz
        nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax, font_size=12, font_color='black', font_weight='bold')

        # Bu adımda işlenen kenarı kırmızıyla vurgula
        if step < len(edges_in_steps):
            u, v = edges_in_steps[step][0]
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=2.5, alpha=0.6, edge_color="r", ax=ax)

        # Açıklamayı ekle
        ax.text(0.5, 0.01, explanations[step], horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

        # Görseli kaydet
        img_path = os.path.join(img_dir, f"adim_{step+1}.png")
        plt.savefig(img_path)
        plt.close(fig)

    # Görsellerden video oluştur
    create_video_from_images(img_dir, video_filename)
    print(f"Video kaydedildi: {video_filename}")

# Görsellerden video oluşturma fonksiyonu
def create_video_from_images(img_dir, video_filename):
    images = sorted([img for img in os.listdir(img_dir) if img.endswith(".png")],
                    key=lambda x: int(x.split('_')[1].split('.')[0]))
    frame = cv2.imread(os.path.join(img_dir, images[0]))
    height, width, layers = frame.shape

    # Video oluşturma
    video = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(img_dir, image)))

    video.release()

# Kullanıcıdan input alalım
num_nodes = 5  # Düğüm sayısı
graph = [
    # (0, 1, -1),  # Kenarlar (u, v, w): u'dan v'ye w ağırlığı ile kenar
    # (0, 2, 4),
    # (1, 2, 3),
    # (1, 3, 2),
    # (1, 4, 2),
    # (3, 2, 5),
    # (4, 3, -3)
    
    (0, 1, 5),  # Kenarlar (u, v, w): u'dan v'ye w ağırlığı ile kenar
    (0, 2, 2),
    (1, 2, 2),
    (1, 3, 4),
    (2, 4, 5),
    (3, 2, -10),
    (4, 3, 3)
]

start_node = 0  # Başlangıç düğümü

# Bellman-Ford algoritmasını çalıştır
steps, edges_in_steps, explanations, negative_cycle = bellman_ford(graph, num_nodes, start_node)

# Çözüm tablosunu göster
display_steps(steps, num_nodes)

# Eğer negatif döngü yoksa adım adım görselleri kaydet ve videoyu oluştur
if not negative_cycle:
    plot_graph_and_save_video(graph, num_nodes, steps, edges_in_steps, explanations, video_filename="bellman_ford_output.mp4")
else:
    print("Negatif ağırlıklı döngü olduğundan animasyon gösterilemiyor.")