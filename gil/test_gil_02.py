import time

COUNT = 500_000_000

def countdown(n):
    while n > 0:
        n -= 1

if __name__ == '__main__':
    start = time.time()
    countdown(COUNT)
    end = time.time()

    print('Затраченное время -', end - start)