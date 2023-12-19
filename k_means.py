import pandas as pd
import numpy as np

def euclidean_distance(point1, point2):
    # Ensure both points have the same number of dimensions
    assert len(point1) == len(point2), "Points must have the same number of dimensions"

    # Calculate the squared differences for each dimension
    squared_diff = [(p1 - p2) ** 2 for p1, p2 in zip(point1, point2)]

    # Sum up the squared differences and take the square root
    distance = sum(squared_diff) ** 0.5

    return distance
def kmeans(data, k, max_iterations=100):
    # Reset the index after sampling to ensure contiguous indices
    centroids = data.sample(k).values.tolist()

    for _ in range(max_iterations):
        # Calculate Euclidean distances manually between data points and centroids
        distances = [
            [euclidean_distance(point, centroid) for centroid in centroids]
            for _, point in data.iterrows()
        ]

        # Assign each data point to the nearest centroid
        cluster_labels = np.argmin(distances, axis=1)

        # Update centroids based on the mean of assigned data points
        new_centroids = [
            data.loc[cluster_labels == i].mean().tolist()
            for i in range(k)
        ]

        # Check for convergence
        if np.array_equal(centroids, new_centroids):
            break

        centroids = new_centroids

    return cluster_labels
