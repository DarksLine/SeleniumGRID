import datetime


def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return a


current_day = datetime.datetime.now().day
fib_number = fibonacci(current_day + 1)
