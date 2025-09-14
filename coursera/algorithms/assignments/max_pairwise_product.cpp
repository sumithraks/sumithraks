#include <iostream>
#include <vector>
#include <cstdlib>

using namespace std;

long long findMaxPairTest(vector<int> arr, int n) {
    long long result = 0;
    for (int i=0; i < n; ++i) {
        for (int j=i+1; j < n;++j) 
            if (result < arr[i] * arr[j])
                result = arr[i]*arr[j];
    }
    return result;
}

long long findMaxPairTestFast(vector<int> arr, int n) {
    long long maxIndex=  0;
    long long secMaxIndex = 0;
    if (arr[0] < arr[1]) {
        secMaxIndex=0;
        maxIndex = 1;
    } else {
        secMaxIndex=1;
        maxIndex=0;
    }
    for (int i=2; i < n; ++i) {
        
        if (arr[maxIndex] <= arr[i] )
        {
           secMaxIndex=maxIndex;
           maxIndex = i;
        } else if (arr[secMaxIndex] < arr[i]) {
           secMaxIndex=i;
        }
    }
//    cout << maxIndex << " " << secMaxIndex << endl;
    long long result = (long long)arr[maxIndex] * (long long)arr[secMaxIndex];
    return result;
}

bool stressTest() {
    int n = rand()%1000;
    vector<int> arr;
    cout << n << endl;
    for (int i=0; i < n; ++i) {
        int num = rand()%100000;
        cout << num << " ";
        arr.push_back(num);
    }
    cout << endl;
    long long expected = findMaxPairTest(arr,n);
    long long actual = findMaxPairTest(arr,n);
    if (expected != actual) {
        cout << "Expected = " << expected << " Actual = " << actual << endl;
        return false;
    }
    cout << "OK" << endl;
    return true;
}


int main(int argc, char* argv[]) {
    int n;
    vector<int> arr;
#ifdef TEST
    while (true) {
        if (!stressTest()) break;
    }
    return 0;
#endif
    cin >> n;
    int number;
    if (n < 2) return -1;
    for (int i=0; i < n;++i) {
        cin >> number;
        arr.push_back(number);
    }
    cout << findMaxPairTestFast(arr,n);
}
