import numpy as np


def euclidean_distance(point1, point2):
    assert len(point1) == len(point2), "Girdiler aynı boyutta olmalı"

    # zip fonksiyonu aynı indisli değerleri eşler
    # öklid uzaklığı
    # farkların kareleri
    squared_diff = [(p1 - p2) ** 2 for p1, p2 in zip(point1, point2)]

    # farkların karelerinin toplamının karekökü
    distance = sum(squared_diff) ** 0.5

    return distance


def kmeans(data, k, max_iterations=100):
    # k adet merkez başlangıçta veri uzayından seçilir
    centroids = data.sample(k).values.tolist()

    for _ in range(max_iterations):
        # her nokta için öklid uzaklıklarının listesi tutulur
        # distances[0, 1] 0 noktasının 2. merkeze uzaklığı, distances[0, 3] 0 noktasının 4. merkeze uzaklığı
        distances = [
            [euclidean_distance(point, centroid) for centroid in centroids]
            for _, point in data.iterrows()  # indis değerine ihtiyacımız yok (_)
        ]

        # argmin liste içerisindeki en düşük değerin indisini döndürür
        # distances[x] n adet merkeze ait uzaklıkları içerir,
        # örneğin 4 döndürmesi en küçük uzaklığın 5. merkeze olan uzaklık olduğunu bildirir
        # bu iterasyon için bu nokta 5. küme şeklinde etiketlenecektir
        cluster_labels = np.argmin(distances, axis=1)

        # kümelerin ortalaması alınarak her kümeye ait yeni merkezler hesaplanır
        new_centroids = [
            data.loc[cluster_labels == i].mean().tolist()
            for i in range(k)
        ]

        # merkezler değişmemişse son kümeler hesaplanmış demektir
        if np.array_equal(centroids, new_centroids):
            break

        centroids = new_centroids

    return cluster_labels
