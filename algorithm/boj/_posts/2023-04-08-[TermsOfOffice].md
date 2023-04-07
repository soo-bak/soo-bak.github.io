---
layout: single
title: "[백준 9782] Terms of Office (C#, C++) - soo:bak"
date: "2023-04-08 01:22:00 +0900"
---

## 문제 링크
  [9782번 - Terms of Office](https://www.acmicpc.net/problem/9782)

## 설명
입력으로 주어지는 두 연도 사이에서, 각 직업들이 <b>동시에</b> 변경되는 연도를 탐색하여 출력하는 문제입니다. <br>

문제의 조건에 따르면, 각 직업은 다음의 임기마다 변경됩니다. <br>
1. Mayor : 4년마다 선출
2. Treasurer : 2년마다 선출
3. Programer : 3년마다 선출
4. dog-catcher : 5년마다 선출

따라서, 입력으로 주어지느 두 연도 사이의 범위에서 각 직업들이 모두 변경되는 연도를 탐색 후, <br>

문제의 출력 조건에 따라 적절히 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var x = int.Parse(Console.ReadLine()!);
      var y = int.Parse(Console.ReadLine()!);

      for (var year = x; year <= y; year++) {
        if ((year - x) % 4 == 0 && (year - x) % 2 == 0 && (year - x) % 3 == 0 && (year - x) % 5 == 0)
          Console.WriteLine($"All positions change in year {year}");
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

  int x, y; cin >> x >> y;

  for (int year = x; year <= y; year++) {
    if (!((year - x) % 4) && !((year - x) % 2) && !((year - x) % 3) && !((year - x) % 5))
      cout << "All positions change in year " << year << "\n";
  }

  return 0;
}
  ```
