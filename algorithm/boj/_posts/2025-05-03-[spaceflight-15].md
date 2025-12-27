---
layout: single
title: "[백준 9501] 꿍의 우주여행 (C#, C++) - soo:bak"
date: "2025-05-03 02:13:00 +0900"
description: 우주선의 최고속도와 연료 정보를 바탕으로 목적지까지 도달 가능한 우주선의 개수를 판단하는 백준 9501번 꿍의 우주여행 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9501
  - C#
  - C++
  - 알고리즘
  - arithmetic
  - 구현
  - 수학
keywords: "백준 9501, 백준 9501번, BOJ 9501, spaceflight, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9501번 - 꿍의 우주여행](https://www.acmicpc.net/problem/9501)

## 설명
각 우주선의 **최고 속도**, **보유 연료**, **연료 소비율**이 주어졌을 때,

해당 우주선이 **목적지까지 도달할 수 있는지 판단하는 문제**입니다.

- 우주선은 즉시 최고 속도에 도달하며,
- 이동 시간은 `목적지 거리 ÷ 최고 속도`로 계산됩니다.
- 이때 **이동 시간에 연료 소비율을 곱한 값**은 목적지까지 이동하는 데 필요한 연료의 총량을 의미합니다.
- 이 값이 현재 보유한 연료량보다 작거나 같아야, 해당 우주선은 목적지까지 무사히 도달할 수 있습니다.

즉, **도달 시간 × 연료 소비율 ≤ 보유 연료** 조건을 만족하는 우주선의 개수를 세어야 합니다.

<br>

## 접근법
- 테스트케이스 수를 입력받습니다.
- 각 테스트케이스마다 우주선의 개수와 목적지까지의 거리를 입력받습니다.
- 이어서 각 우주선에 대해 **최고속도**, **연료량**, **연료 소비율**을 입력받습니다.
- 다음 식을 통해 조건을 판단합니다:

  $$
  \frac{\text{목적지까지의 거리}}{\text{최고속도}} \times \text{연료 소비율} \leq \text{보유 연료}
  $$

- 조건을 만족하는 우주선의 개수를 세어 출력합니다.

<br>

---

## C# 코드

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var parts = Console.ReadLine().Split();
      int n = int.Parse(parts[0]);
      int d = int.Parse(parts[1]);
      int cnt = 0;
      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine().Split();
        int v = int.Parse(input[0]);
        int f = int.Parse(input[1]);
        int c = int.Parse(input[2]);
        double time = (double)d / v;
        if (time * c <= f) cnt++;
      }
      Console.WriteLine(cnt);
    }
  }
}
```

## C++ 코드

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int n, d; cin >> n >> d;
    int cnt = 0;
    while (n--) {
      int v, f, c; cin >> v >> f >> c;
      if ((double)d / v * c <= f) cnt++;
    }
    cout << cnt << "\n";
  }

  return 0;
}
```

---
