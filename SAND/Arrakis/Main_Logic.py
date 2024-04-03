def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

def print_fibonacci_pyramid(rows):
    for i in range(rows):
        fib_sequence = fibonacci(i+1)
        print(' '.join(map(str, fib_sequence)).center(rows * 4))

if __name__ == "__main__":
    #rows = int(input("Enter the number of rows for the Fibonacci pyramid: "))
    rows = 20
    print_fibonacci_pyramid(rows)
