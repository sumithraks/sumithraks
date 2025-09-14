#include <iostream>

int gcd(int a, int b) {
    if (b==0) return a;
    int reminder = a % b;
    return gcd(b,reminder);
}

long long lcm(int a, int b) {
    int hcf = gcd(a,b);
    return ((long long)a*b)/hcf;
}

int main() {
  int a, b;
  std::cin >> a >> b;
  std::cout << lcm(a, b) << std::endl;
  return 0;
}
