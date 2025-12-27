---
layout: single
title: "[백준 17946] 피자는 나눌 수록 커지잖아요 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 17946번 C#, C++ 풀이 - 최대 조각 수와 요구 조각 수를 비교해 남는 조각을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 17946
  - C#
  - C++
  - 알고리즘
  - 수학
keywords: "백준 17946, 백준 17946번, BOJ 17946, PizzaGetsBigger, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17946번 - 피자는 나눌 수록 커지잖아요](https://www.acmicpc.net/problem/17946)

## 설명
최대 K번 칼질할 수 있을 때, 예찬이가 먹을 수 있는 최대 피자 조각 수를 구하는 문제입니다.

<br>

## 접근법
k번 칼질로 만들 수 있는 최대 조각 수는 `k(k+1)/2 + 1`입니다.  
윤희에게 주는 조각 수는 `1+2+...+k = k(k+1)/2`이므로 남는 조각은 항상 1입니다.

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
    for (var i = 0; i < t; i++) {
      var k = int.Parse(parts[idx++]);
      var total = k * (k + 1) / 2 + 1;
      var give = k * (k + 1) / 2;
      sb.AppendLine((total - give).ToString());
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
    int k; cin >> k;
    int total = k * (k + 1) / 2 + 1;
    int give = k * (k + 1) / 2;
    cout << total - give << "\n";
  }

  return 0;
}
```
