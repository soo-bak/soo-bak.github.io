---
layout: single
title: "[백준 9070] 장보기 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 가성비가 가장 좋은 맛살의 가격을 선택하는 문제
---

## 문제 링크
[9070번 - 장보기](https://www.acmicpc.net/problem/9070)

## 설명
각 맛살의 중량과 가격이 주어질 때, 같은 가격 대비 중량이 최대인 제품의 가격을 출력하는 문제입니다.

<br>

## 접근법
중량/가격 비율이 큰 제품을 선택하면 됩니다.  
비율이 같으면 더 낮은 가격을 선택하므로 `W1*C2`와 `W2*C1`로 비교해 처리합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var tc = 0; tc < t; tc++) {
      var n = int.Parse(parts[idx++]);
      var bestW = 0;
      var bestC = 1;

      for (var i = 0; i < n; i++) {
        var w = int.Parse(parts[idx++]);
        var c = int.Parse(parts[idx++]);
        var left = w * bestC;
        var right = bestW * c;
        if (left > right || (left == right && c < bestC)) {
          bestW = w;
          bestC = c;
        }
      }

      sb.AppendLine(bestC.ToString());
    }

    Console.Write(sb);
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

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    int bestW = 0, bestC = 1;
    for (int i = 0; i < n; i++) {
      int w, c; cin >> w >> c;
      int left = w * bestC;
      int right = bestW * c;
      if (left > right || (left == right && c < bestC)) {
        bestW = w;
        bestC = c;
      }
    }
    cout << bestC << "\n";
  }

  return 0;
}
```
