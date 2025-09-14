#include <iostream>
#include <vector>
#include <cstdlib>

using std::vector;
using std::swap;

void partition2(vector<int> &a, int l, int r, int &m1, int &m2) {
  int x = a[l];
  //std::cout << "Left = " << l << " Right " << r << " Element " << x << std::endl;
  int j = l;
  for (int i = l + 1; i <= r; i++) {
    if (a[i] <= x) {
      j++;
      swap(a[i], a[j]);
    }
    //for (int n = l ; n <= r; n++) 
      //std::cout << a[n] << " " ;
    //std::cout << std::endl;
  }
  swap(a[l], a[j]);
  m2=m1=j;
  for (int i = l + 1; i < j; i++) {      
      if (a[i]==x) {
          j--;
          swap(a[i], a[j]);
      }
  }
  m2=j;
  if (a[m1]==a[m2])
      m1=m2;
  //std::cerr << "M1 =  " << m1 << std::endl;
  //std::cerr << "M2 =  " << m2 << std::endl;
}

void randomized_quick_sort(vector<int> &a, int l, int r) {
  if (l >= r) {
    return;
  }

  int k = l + rand() % (r - l + 1);
//  int k = 3;
  swap(a[l], a[k]);
  int low,high;
  partition2(a, l, r,low,high);

  randomized_quick_sort(a, l, low - 1);
  randomized_quick_sort(a, high + 1, r);
}

int main() {
  int n;
  std::cin >> n;
  vector<int> a(n);
  for (size_t i = 0; i < a.size(); ++i) {
    std::cin >> a[i];
  }
  randomized_quick_sort(a, 0, a.size() - 1);
  for (size_t i = 0; i < a.size(); ++i) {
    std::cout << a[i] << ' ';
  }
}
