#include <algorithm>
#include <iostream>
#include <climits>
#include <vector>

using std::vector;

struct Segment {
  int start, end;
};

bool orderByLeft(const Segment &a, const Segment &b) {
    return a.start < b.start;
}

vector<int> optimal_points(vector<Segment> &segments) {
 //     std::cerr << "Before sorting " << std::endl;
  sort(segments.begin(),segments.end(),&orderByLeft);
//      std::cerr << "After sorting " << std::endl;
  vector<Segment> selected;
  vector<int> points;
  Segment current = segments[0];
//      std::cerr << "Starting loop " << segments.size() << std::endl;
  for (int i = 1; i < segments.size();++i) {
//      std::cerr << "Comparing (" << segments[i].start << "," << segments[i].end << ") with ( " << current.start << "," << current.end <<")\n";
      if (segments[i].start <= current.end )  //&& (segments[i].end-segments[i].start <= current.end-current.start ))
      {
          if (segments[i].end < current.end)
              current.end=segments[i].end;
//          std::cerr << "Skipping" << std::endl;
          continue;
      }
      {
      //    std::cerr << "Selecting new segment" << std::endl;
          selected.push_back(current);
          current = segments[i];
      }
  }
  selected.push_back(current);
  //write your code here
  for (size_t i = 0; i < selected.size(); ++i) {
    points.push_back(selected[i].end);
  }
  return points;
}

int main() {
  int n;
  std::cin >> n;
  vector<Segment> segments(n);
  for (size_t i = 0; i < segments.size(); ++i) {
    std::cin >> segments[i].start >> segments[i].end;
  }
  vector<int> points = optimal_points(segments);
  std::cout << points.size() << "\n";
  for (size_t i = 0; i < points.size(); ++i) {
    std::cout << points[i] << " ";
  }
}
