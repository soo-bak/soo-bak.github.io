---
layout: single
title: "[백준 16728] Chaarshanbegaan at Cafebazaar (C#, C++) - soo:bak"
date: "2025-12-27 03:35:00 +0900"
description: 다트 좌표로부터 거리 구간별 점수를 합산하는 문제
---

## 문제 링크
[16728번 - Chaarshanbegaan at Cafebazaar](https://www.acmicpc.net/problem/16728)

## 설명
원점(0,0)을 중심으로 한 다트판에서 각 투척 좌표가 주어질 때, 거리 구간에 따라 매겨진 점수를 모두 합산하는 문제입니다.

반지름이 10, 30, 50, 70, 90, 110, 130, 150, 170, 190인 동심원 안에 들어가면 각각 10부터 1까지 점수를 얻고, 그 밖이면 0점입니다.

<br>

## 접근법
각 좌표에서 원점까지의 거리 제곱을 구한 뒤, 가장 안쪽 원부터 바깥쪽으로 반지름 제곱과 비교하여 점수를 결정합니다. 제곱 값으로 비교하면 실수 오차를 피할 수 있습니다.

모든 점수의 합을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var limits = new int[] { 100, 900, 2500, 4900, 8100, 12100, 16900, 22500, 28900, 36100 };

    var total = 0;
    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var x = int.Parse(parts[0]);
      var y = int.Parse(parts[1]);
      var d2 = x * x + y * y;

      var score = 0;
      for (var j = 0; j < limits.Length; j++) {
        if (d2 <= limits[j]) {
          score = 10 - j;
          break;
        }
      }
      total += score;
    }

    Console.WriteLine(total);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi lim = {100, 900, 2500, 4900, 8100, 12100, 16900, 22500, 28900, 36100};

  int total = 0;
  for (int i = 0; i < n; i++) {
    int x, y; cin >> x >> y;
    int d2 = x * x + y * y;
    int score = 0;
    for (int j = 0; j < (int)lim.size(); j++) {
      if (d2 <= lim[j]) {
        score = 10 - j;
        break;
      }
    }
    total += score;
  }

  cout << total << "\n";

  return 0;
}
```
