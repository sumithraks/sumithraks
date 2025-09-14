#include <iostream>
#include <vector>
#include <map>
#include <algorithm>

using std::vector;

vector<long> optimal_sequence(long n) {
  std::map<long,long> minOps;
  std::map<long,std::vector<long> > sequences;
  std::vector<long> sequence;
  std::vector<long> a;
  a.push_back(1);
  minOps[1]=0;
  sequences[1]=a;
  int last = 1;
  for (long current = 2; current <= n; ++current) {
       long numOps = LONG_MAX;
       int seq = 1;
       if (current%2==0) {
           if (minOps.find(current/2) != minOps.end()) {
               numOps=minOps[current/2]+1;
               if ((minOps.find(current) != minOps.end() && minOps[current] > numOps)||
                    minOps.find(current) == minOps.end()) {

                   minOps[current] = numOps;
                   if (sequences.find(current/2)!=sequences.end()) {
                       vector<long> sequence = sequences[current/2];
                       sequence.push_back(current);
                       sequences[current]=sequence;
                   }
                   
               }
           }
       } 

       if (current %3 == 0 ) {
           if (minOps.find(current/3) != minOps.end()) {
               numOps=minOps[current/3]+1;
               if ((minOps.find(current) != minOps.end() && minOps[current] > numOps)||
                    minOps.find(current) == minOps.end()) {
                   minOps[current] = numOps;
                   if (sequences.find(current/3)!=sequences.end()) {
                       vector<long> sequence = sequences[current/3];
                       sequence.push_back(current);
                       sequences[current]=sequence;
                   }
               }
           }
       }

      if (minOps.find(current-1) != minOps.end()) {
          numOps=minOps[current-1]+1;
          if ((minOps.find(current) != minOps.end() && minOps[current] > numOps)||
               minOps.find(current) == minOps.end()) {
             minOps[current] = numOps;
             if (sequences.find(current-1)!=sequences.end()) {
                  vector<long> sequence = sequences[current-1];
                  sequence.push_back(current);
                  sequences[current]=sequence;
             }
          }
      }
  }
  sequence = sequences[n];
  return sequence;
}

int main() {
  long n;
  std::cin >> n;
  vector<long> sequence = optimal_sequence(n);
  std::cout << sequence.size() - 1 << std::endl;
  for (size_t i = 0; i < sequence.size(); ++i) {
    std::cout << sequence[i] << " ";
  }
}
