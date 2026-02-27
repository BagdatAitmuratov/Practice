# n-ге дейінгі сандардың квадратын шығаратын генератор
def gensquares(N):
    for i in range(N):
        yield i**2

for x in gensquares(5):
    print(x) # 0, 1, 4, 9, 16