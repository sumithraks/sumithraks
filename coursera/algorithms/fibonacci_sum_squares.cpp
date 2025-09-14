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

int fibonacci_sum_squares_naive(long long n) {

    if (n <= 1)
        return n;

    int len = length();
    n = n % len;
    if (n <= 1)
        return n;
    
    long long previous = 0;
    long long current  = 1;
    unsigned long long sum      = 1;

    for (long long i = 0; i < n-1 ; ++i) {

        long long tmp_previous = previous;
        previous = current;
        previous = previous%10;
        current = tmp_previous + current;
        current = current%10;
        sum += (current * current);
        //std::cout << "current = " << current << " current sum = " << sum << std::endl;
        sum=sum%10;
    }

    return sum % 10;
}

int main() {
    long long n = 0;
    std::cin >> n;
    std::cout << fibonacci_sum_squares_naive(n);
}
