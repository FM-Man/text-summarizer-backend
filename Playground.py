import math


def euclidean_distance(vect1, vect2):
    # print(vect1, vect2)
    x = 0
    for i in range(len(vect1)):
        x += (vect1[i] - vect2[i]) ** 2
    return x ** 0.5


def pair_finder(matrix):
    minimum = math.inf
    index = (0, 0)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < minimum:
                minimum = matrix[i][j]
                index = (i, j)

    new_matrix = []
    x, y = index
    for i in range(len(matrix)):
        if i != x:
            row = []
            for j in range(len(matrix[i])):
                if j != y:
                    row.append(matrix[i][j])
            new_matrix.append(row)

    print(new_matrix)
    return minimum, new_matrix


sent_x = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]
sent_y = [[11, 12, 13, 14],
          [15, 16, 17, 18],
          [19, 10, 11, 12],
          [11, 12, 13, 14]]


matrix = []
for i in range(len(sent_x)):
    row = []
    for j in range(len(sent_y)):
        dist = euclidean_distance(sent_x[i], sent_y[j])
        row.append(dist)
    matrix.append(row)

final_tally = []
while len(matrix) != 0:
    minimum, matrix = pair_finder(matrix)
    final_tally.append(minimum)

print(final_tally)
