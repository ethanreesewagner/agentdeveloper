def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

result = factorial_iterative(9)
print(result)