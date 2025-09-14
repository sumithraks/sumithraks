#include <iostream>

long length(long m)
{
    long previousMinusOne = 0;
    long previous = 1;
    long current;
    long res = 0;
    for(int i = 0; i < m * m; i++)
    {
        current = previous + previousMinusOne;
        current = current %m;
        previousMinusOne=previous;
        previous = current;
        if (previousMinusOne == 0 && previous == 1)
            res = i + 1;
    }
    return res;
}

long long get_fibonacci_huge_naive(long long n, long long m) {
    if (n <= 1)
        return n;

    n = n % length(m);
    if (n <= 1)
        return n;
    long long previousMinusOne = 0;
    long long previous  = 1;
    long long current=1;

    for (long long i = 2; i <= n ; ++i) {
        current = previous + previousMinusOne;
        current = current %m;
        previousMinusOne=previous;
        previous = current;
    }

    return current % m;
}

int main() {
    long long n, m;
    std::cin >> n >> m;
    std::cout << get_fibonacci_huge_naive(n, m) << '\n';
}
