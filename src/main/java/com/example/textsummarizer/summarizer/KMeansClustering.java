package com.example.textsummarizer.summarizer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class KMeansClustering {
//    public static void main(String[] args) {
//        ArrayList<double[]> arrayList = new ArrayList<>();
//        // Add your vectors to the arrayList
//
//        int k = 3; // Number of clusters
//
//        List<double[]> clusters = kMeansClustering(arrayList, k);
//
//        // Print the resulting clusters
//        for (int i = 0; i < clusters.size(); i++) {
//            System.out.println("Cluster " + (i + 1) + ": " + Arrays.toString(clusters.get(i)));
//        }
//    }

    public ArrayList<ArrayList<EigenPoint>> kMeansClustering(ArrayList<EigenPoint> data, int k) {
        ArrayList<double[]> centroids = initializeRandomCentroids(data, k);
        ArrayList<ArrayList<EigenPoint>> clusters = new ArrayList<>();

        for (int iteration = 0; iteration < 100; iteration++) {
            clusters.clear();
            // Initialize clusters
            for (int i = 0; i < k; i++) {
                clusters.add(new ArrayList<>());
            }

            // Assign data points to clusters
            for (EigenPoint ep : data) {
                int closestClusterIndex = findClosestCluster(ep.vector, centroids);
                clusters.get(closestClusterIndex).add(ep);
            }

            // Update centroids
            ArrayList<double[]> newCentroids = new ArrayList<>();
            for (ArrayList<EigenPoint> cluster : clusters) {
                if (!cluster.isEmpty()) {
                    newCentroids.add(calculateCentroid(cluster));
                }
            }

            if (centroids.equals(newCentroids)) {
                break; // Convergence reached
            }

            centroids = newCentroids;
        }

        return clusters;
    }

    private ArrayList<double[]> initializeRandomCentroids(ArrayList<EigenPoint> data, int k) {
        ArrayList<double[]> centroids = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < k; i++) {
            int randomIndex = random.nextInt(data.size());
            centroids.add(data.get(randomIndex).vector);
        }

        return centroids;
    }

    private int findClosestCluster(double[] vector, ArrayList<double[]> centroids) {
        int closestIndex = 0;
        double closestDistance = Double.MAX_VALUE;

        for (int i = 0; i < centroids.size(); i++) {
            double distance = calculateDistance(vector, centroids.get(i));
            if (distance < closestDistance) {
                closestDistance = distance;
                closestIndex = i;
            }
        }

        return closestIndex;
    }

    private double calculateDistance(double[] vector1, double[] vector2) {
        double sum = 0.0;
        for (int i = 0; i < vector1.length; i++) {
            sum += Math.pow(vector1[i] - vector2[i], 2);
        }
        return Math.sqrt(sum);
    }

    private double[] calculateCentroid(ArrayList<EigenPoint> cluster) {
        int dimensions = cluster.get(0).vector.length;
        double[] centroid = new double[dimensions];

        for (int i = 0; i < dimensions; i++) {
            double sum = 0.0;
            for (EigenPoint ep : cluster) {
                sum += ep.vector[i];
            }
            centroid[i] = sum / cluster.size();
        }

        return centroid;
    }
}

