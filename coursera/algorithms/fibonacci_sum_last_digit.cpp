#include <iostream>

long length()
{
    long previousMinusOne = 0;
    long previous = 1;
    long current;
    long res = 0;
    for(int i = 0; i < 100; i++)
    {
        current = previous + previousMinusOne;
        current = current %10;
        previousMinusOne=previous;
        previous = current;
        if (previousMinusOne == 0 && previous == 1)
            res = i + 1;
    }
    return res;
}

int get_fibonacci_last_digit(unsigned long long n) {
    if (n <= 1)
        return n;
    int len  = length();
    //std::cout << "Len " << len << std::endl;

    n = (n+2) % len;
    //std::cout << "n= " << n << std::endl;

    if (n <= 1) {
        return (n-1<0?9:n-1)%10;
    } 

    long long previousMinusOne = 0;
    long long previous  = 1;
    long long current=1;

    for (long long i = 2; i <= n ; ++i) {
        current = previous + previousMinusOne;
        current = current %10;
        previousMinusOne=previous;
        previous = current;
    }
    return (current-1<0?9:current-1)%10;
}

int main() {
    unsigned long long n;
    std::cin >> n;
    int c = get_fibonacci_last_digit(n);
    std::cout << c << '\n';
}
