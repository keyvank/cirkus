def f1(x, y):
    return x * y + y - 15


def f1_x(x, y):
    return y


def f1_y(x, y):
    return x + 1


def f2(x, y):
    return x + y - x * x - 3


def f2_x(x, y):
    return 1 - 2 * x


def f2_y(x, y):
    return 1


def f(x):
    return [f1(x[0], x[1]), f2(x[0], x[1])]


def f_prime(x):
    return [[f1_x(x[0], x[1]), f1_y(x[0], x[1])], [f2_x(x[0], x[1]), f2_y(x[0], x[1])]]


def vec_mat(m, v):
    return [v[0] * m[0][0] + v[1] * m[0][1], v[0] * m[1][0] + v[1] * m[1][1]]


def vec_sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]


def mat_inv(m):
    det = 1 / (m[0][0] * m[1][1] - m[0][1] * m[1][0])
    return [
        [m[1][1] * det, -m[0][1] * det],
        [-m[1][0] * det, m[0][0] * det],
    ]


X = [3, 3]

for _ in range(100):
    X_prime = f_prime(X)
    X = vec_sub(X, vec_mat(mat_inv(X_prime), f(X)))

print(X)
print(f(X))
