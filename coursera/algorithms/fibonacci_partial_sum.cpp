#include <iostream>
#include <vector>
using std::vector;

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

long long get_fibonacci_partial_sum_naive(long long from, long long to) {
    int len = length();
    from = from%len;
    to = to%len;
    if (from >= to) to+=len;
    //std::cout << "From = " << from << std::endl;
    //std::cout << "To = " << to << std::endl;
    long long sum = 0;
    long long current = 0;
    long long next  = 1;

    for (long long i = 0; i <= to; ++i) {
        if (i >= from) {
            sum += current;
            sum = sum % 10;
        }

        long long new_current = next;
        next = next + current;
        next = next % 10;
        current = new_current;
        current = current % 10;
    }

    return sum % 10;
}

int main() {
    long long from, to;
    std::cin >> from >> to;
    std::cout << get_fibonacci_partial_sum_naive(from, to) << '\n';
}
