def f(x):
    return x * x * x + 2 * x - 2


def f_prime(x):
    return 3 * x * x + 2


x = 0.5

for _ in range(10):
    x = x - f(x) / f_prime(x)

print(x)
