---
layout: single
title: "[백준 2160] 그림 비교 (C#, C++) - soo:bak"
date: "2025-12-07 01:10:00 +0900"
description: 가장 비슷한 두 그림을 찾는 백준 2160번 그림 비교 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[2160번 - 그림 비교](https://www.acmicpc.net/problem/2160)

## 설명
N개의 그림이 주어질 때, 서로 다른 칸의 개수가 가장 적은 두 그림의 번호를 구하는 문제입니다. 각 그림은 5행 7열의 문자 배열입니다.

<br>

## 접근법
먼저, 그림 한 장은 35칸뿐이므로 모든 쌍을 직접 비교해도 충분합니다. 두 그림의 다른 칸 수를 세고, 최소값과 그 쌍의 인덱스를 갱신합니다.

다음으로, 모든 쌍에 대해 비교를 완료하면 가장 비슷한 두 그림의 번호를 출력합니다. 번호는 1부터 시작하며 작은 번호를 먼저 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var pic = new string[n, 5];

      for (var i = 0; i < n; i++) {
        for (var r = 0; r < 5; r++)
          pic[i, r] = Console.ReadLine()!;
      }

      var best = int.MaxValue;
      var aIdx = 1;
      var bIdx = 2;

      for (var i = 0; i < n; i++) {
        for (var j = i + 1; j < n; j++) {
          var diff = 0;
          for (var r = 0; r < 5; r++) {
            var s1 = pic[i, r];
            var s2 = pic[j, r];
            for (var c = 0; c < 7; c++) {
              if (s1[c] != s2[c])
                diff++;
            }
          }
          if (diff < best) {
            best = diff;
            aIdx = i + 1;
            bIdx = j + 1;
          }
        }
      }

      Console.WriteLine($"{aIdx} {bIdx}");
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<array<string, 5>> pic(n);
  for (int i = 0; i < n; i++) {
    for (int r = 0; r < 5; r++)
      cin >> pic[i][r];
  }

  int best = INT_MAX, ai = 1, bi = 2;
  for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
      int diff = 0;
      for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 7; c++) {
          if (pic[i][r][c] != pic[j][r][c])
            diff++;
        }
      }
      if (diff < best) {
        best = diff;
        ai = i + 1;
        bi = j + 1;
      }
    }
  }

  cout << ai << " " << bi << "\n";

  return 0;
}
```
