if __name__ == '__main__':
    while True:
        try:
            n = int(input())
            m = int(input())
            if not 1 <= n < m <= 10000:
                print('Input numbers need to be in a range from 1 to 10000.')
                continue
            break
        except ValueError:
            print('Invalid input. Please enter numbers.')

    for i in range(n, m+1):
        if i % 3 == 0 and i % 5 == 0:
            print('FizzBuzz')
        elif i % 3 == 0:
            print('Fizz')
        elif i % 5 == 0:
            print('Buzz')
        else:
            print(i)
