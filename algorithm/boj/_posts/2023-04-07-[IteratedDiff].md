---
layout: single
title: "[백준 4807] Iterated Difference (C#, C++) - soo:bak"
date: "2023-04-07 23:31:00 +0900"
---

## 문제 링크
  [4807번 - Iterated Difference](https://www.acmicpc.net/problem/4807)

## 설명
입력으로 주어지는 정수의 배열에서 인접한 원소 간의 절대값 차이를 이용하여 새로운 리스트를 만드는 과정을 반복 할 때, <br>

"몇 번 반복하여야" 모든 원소가 동일한 정수로 수렴하는 지에 대해 필요한 반복 횟수를 탐색하는 문제입니다. <br>

문제의 조건에 따라서 적절히 시뮬레이션을 진행하며, <br>

만약, `1000` 번의 반복을 진행하였는데도 모든 원소가 동일한 정수로 수렴하지 않으면, <br>

문제의 조건에 따라서, `"not attained"` 를 출력해야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int cntCase = 1;
      while (true) {
        var n = int.Parse(Console.ReadLine()!);
        if (n == 0) break ;

        var lst = new List<int>(n);
        var input = Console.ReadLine()?.Split(' ');
        for (var i = 0; i < n; i++)
          lst.Add(int.Parse(input![i]));

        int cnt = 1_000;
        for (var i = 0; i < 1_000; i++) {
          if (lst.All(x => x == lst[0])) {
            cnt = i; break ;
          }

          var cache = new List<int>(n);
          for (var j = 0; j < n; j++)
          cache.Add(Math.Abs(lst[j] - lst[(j + 1) % n]));

          lst = cache;
        }

        Console.Write($"Case {cntCase}: ");
        if (cnt == 1_000) Console.WriteLine("not attained");
        else Console.WriteLine($"{cnt} iterations");

        cntCase++;
      }

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase = 1;
  while (true) {
    int n; cin >> n;
    if (n == 0) break ;

    vector<int> v(n);
    for (int i = 0; i < n; i++)
      cin >> v[i];

    int cnt = 1'000;
    for (int i = 0; i < 1'000; i++) {
      if (count(v.begin(), v.end(), 0) == n) {
        cnt = max(0, i - 1); break ;
      }

      vector<int> cache(n);
      for (int j = 0; j < n; j++)
        cache[j] = abs(v[j] - v[(j + 1) % n]);

      v = cache;
    }

    cout << "Case " << cntCase << ": ";
    if (cnt == 1'000) cout << "not attained\n";
    else cout << cnt << " iterations\n";

    cntCase++;
  }

  return 0;
}
  ```
