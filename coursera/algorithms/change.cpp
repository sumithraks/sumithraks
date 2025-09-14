#include <iostream>
#include <vector>

int get_change(int m) {

  std::vector<int> coins;
  coins.push_back(1);
  coins.push_back(5);
  coins.push_back(10);
  int balance = m;
  int numCoins = 0;
  int coin_index = coins.size()-1;
  do {
      if (balance/coins[coin_index] > 0 )
      {
          numCoins = numCoins + (balance/coins[coin_index]);
          balance = balance % coins[coin_index];
          coin_index--;
      } 
      else
          coin_index--;
      if (coin_index < 0) break;
  } while (balance!=0);
  return numCoins;
}

int main() {
  int m;
  std::cin >> m;
  std::cout << get_change(m) << '\n';
}
