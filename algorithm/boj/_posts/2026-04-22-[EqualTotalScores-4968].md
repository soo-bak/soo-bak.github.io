---
layout: single
title: "[백준 4968] Equal Total Scores (C#, C++) - soo:bak"
date: "2026-04-22 21:03:00 +0900"
description: "백준 4968번 C#, C++ 풀이 - 교환 후 총합이 같아지는 카드 쌍 중 합이 가장 작은 쌍을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 4968
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 4968, 백준 4968번, BOJ 4968, Equal Total Scores, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4968번 - Equal Total Scores](https://www.acmicpc.net/problem/4968)

## 설명
타로와 하나코가 카드 한 장씩 교환해서 총점을 같게 만들 수 있는지 찾고, 가능하다면 그중 카드 점수의 합이 가장 작은 쌍을 구하는 문제입니다.

<br>

## 접근법
타로가 `a`를 주고 하나코가 `b`를 주었다고 하면, 교환 뒤 총점이 같아지려면
`타로합 - a + b = 하나코합 - b + a`
를 만족해야 합니다.

정리하면 `a - b = (타로합 - 하나코합) / 2`가 됩니다. 즉 두 카드의 차이는 이미 정해져 있습니다. 따라서 합의 차이가 홀수면 애초에 불가능합니다.

이후에는 타로의 카드와 하나코의 카드를 모두 확인하면서, 위 식을 만족하는 쌍만 후보로 보고 그중 `a + b`가 가장 작은 것을 고르면 됩니다. 가능한 쌍이 없으면 `-1`을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    while (true) {
      string[] first = Console.ReadLine()!.Split();
      int n = int.Parse(first[0]);
      int m = int.Parse(first[1]);

      if (n == 0 && m == 0)
        break;

      var taro = new List<int>();
      var hanako = new List<int>();
      int sumTaro = 0;
      int sumHanako = 0;

      for (int i = 0; i < n; i++) {
        int value = int.Parse(Console.ReadLine()!);
        taro.Add(value);
        sumTaro += value;
      }

      for (int i = 0; i < m; i++) {
        int value = int.Parse(Console.ReadLine()!);
        hanako.Add(value);
        sumHanako += value;
      }

      int diff = sumTaro - sumHanako;
      if (diff % 2 != 0) {
        Console.WriteLine(-1);
        continue;
      }

      int target = diff / 2;
      int bestA = -1;
      int bestB = -1;
      int bestSum = int.MaxValue;

      for (int i = 0; i < taro.Count; i++) {
        for (int j = 0; j < hanako.Count; j++) {
          int a = taro[i];
          int b = hanako[j];

          if (a - b == target && a + b < bestSum) {
            bestSum = a + b;
            bestA = a;
            bestB = b;
          }
        }
      }

      if (bestA == -1)
        Console.WriteLine(-1);
      else
        Console.WriteLine(bestA + " " + bestB);
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

  while (true) {
    int n, m;
    cin >> n >> m;

    if (n == 0 && m == 0)
      break;

    vector<int> taro(n), hanako(m);
    int sumTaro = 0;
    int sumHanako = 0;

    for (int i = 0; i < n; i++) {
      cin >> taro[i];
      sumTaro += taro[i];
    }

    for (int i = 0; i < m; i++) {
      cin >> hanako[i];
      sumHanako += hanako[i];
    }

    int diff = sumTaro - sumHanako;
    if (diff % 2 != 0) {
      cout << -1 << "\n";
      continue;
    }

    int target = diff / 2;
    int bestA = -1;
    int bestB = -1;
    int bestSum = INT_MAX;

    for (int a : taro) {
      for (int b : hanako) {
        if (a - b == target && a + b < bestSum) {
          bestSum = a + b;
          bestA = a;
          bestB = b;
        }
      }
    }

    if (bestA == -1)
      cout << -1 << "\n";
    else
      cout << bestA << " " << bestB << "\n";
  }

  return 0;
}
```
