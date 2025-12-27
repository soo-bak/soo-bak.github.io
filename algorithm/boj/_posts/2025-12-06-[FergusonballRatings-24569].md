---
layout: single
title: "[백준 24569] Fergusonball Ratings (C#, C++) - soo:bak"
date: "2025-12-06 21:10:00 +0900"
description: 점수와 파울을 이용해 선수별 별점이 40을 넘는지 세고 골드 팀 여부를 판단하는 백준 24569번 Fergusonball Ratings 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 24569
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 24569, 백준 24569번, BOJ 24569, FergusonballRatings, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24569번 - Fergusonball Ratings](https://www.acmicpc.net/problem/24569)

## 설명
선수마다 점수와 파울이 주어집니다. 별점은 점수에 5를 곱하고 파울에 3을 곱한 값을 뺀 것입니다.

별점이 40을 초과하는 선수의 수를 세고, 모든 선수가 40을 넘으면 골드 팀이므로 출력 끝에 +를 붙이는 문제입니다.

<br>

## 접근법
먼저, 각 선수의 점수와 파울을 입력받아 별점을 계산합니다.

다음으로, 별점이 40을 초과하면 개수를 증가시킵니다.

이후, 개수를 출력하고 개수가 선수 수와 같으면 +를 덧붙입니다.

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
      var cnt = 0;
      for (var i = 0; i < n; i++) {
        var points = int.Parse(Console.ReadLine()!);
        var fouls = int.Parse(Console.ReadLine()!);
        var rating = points * 5 - fouls * 3;
        if (rating > 40)
          cnt++;
      }
      Console.Write(cnt);
      if (cnt == n)
        Console.Write("+");
      Console.WriteLine();
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
  int cnt = 0;
  for (int i = 0; i < n; i++) {
    int points, fouls; cin >> points >> fouls;
    int rating = points * 5 - fouls * 3;
    if (rating > 40)
      cnt++;
  }
  cout << cnt;
  if (cnt == n) cout << "+";

  cout << "\n";

  return 0;
}
```
