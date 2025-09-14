#include <iostream>
#include <vector>

using std::vector;

vector<int> optimal_summands(int n) {
  vector<int> summands;
  int current = n;
  int num = 0;
  do {
     num++;
     if (current-num >= 0 ) {
         //std::cerr << "Adding " << num;
         summands.push_back(num);
         current -= num;
         //std::cerr << " Current " << current << std::endl;
     }
     if (current + num > n) {
         //std::cerr << " Current plus num " << current+num << std::endl;
         break;
     }
  }while (current > 0);
  if (current != 0 ) {
     //std::cerr << "Current not zero " << num << std::endl;
     summands[summands.size()-1]=(summands[summands.size()-1]+current);
  }
  return summands;
}

int main() {
  int n;
  std::cin >> n;
  vector<int> summands = optimal_summands(n);
  std::cout << summands.size() << '\n';
  for (size_t i = 0; i < summands.size(); ++i) {
    std::cout << summands[i] << ' ';
  }
}
