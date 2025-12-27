---
layout: single
title: "[백준 9375] 패션왕 신해빈 (C#, C++) - soo:bak"
date: "2025-11-14 23:58:00 +0900"
description: 의상 종류별 조합을 곱셈 원리로 계산하여 가능한 경우의 수를 구하는 백준 9375번 패션왕 신해빈 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 9375
  - C#
  - C++
  - 알고리즘
  - 수학
  - 자료구조
  - set
  - 조합론
  - hash_set
keywords: "백준 9375, 백준 9375번, BOJ 9375, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9375번 - 패션왕 신해빈](https://www.acmicpc.net/problem/9375)

## 설명

의상의 종류별 개수가 주어질 때, 서로 다른 옷을 조합하여 입을 수 있는 경우의 수를 구하는 문제입니다.<br>

각 종류마다 최대 한 개의 의상만 착용할 수 있으며, 특정 종류를 착용하지 않는 것도 가능합니다.<br>

단, 아무것도 입지 않는 경우는 제외합니다.<br>

<br>

## 접근법

각 종류별로 독립적인 선택을 하므로 곱셈 원리를 적용합니다.

각 의상 종류마다 해당 종류의 의상을 하나 입거나 입지 않는 선택이 가능하므로 `(개수 + 1)`가지 경우의 수를 가집니다.

<br>
모든 종류에 대해 `(개수 + 1)`을 곱하면 전체 조합의 수가 나옵니다.

이때 아무것도 입지 않는 경우 `1`가지가 포함되어 있으므로, 최종 결과에서 `1`을 빼줍니다.

<br>
먼저 해시맵을 사용하여 각 종류별 의상 개수를 카운트합니다.

C#에서는 `Dictionary<string, int>`를, C++에서는 `unordered_map<string, int>`를 사용합니다.

이후 각 종류별로 `(개수 + 1)`을 곱한 뒤 마지막에 `1`을 빼서 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var answers = new int[t];

      for (var i = 0; i < t; i++) {
        var n = int.Parse(Console.ReadLine()!);
        var closet = new Dictionary<string, int>();
        for (var j = 0; j < n; j++) {
          var input = Console.ReadLine()!.Split();
          var kind = input[1];
          if (!closet.ContainsKey(kind)) closet[kind] = 0;
          closet[kind]++;
        }

        var combinations = 1;
        foreach (var count in closet.Values)
          combinations *= (count + 1);

        answers[i] = combinations - 1;
      }

      Console.WriteLine(string.Join("\n", answers));
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

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    unordered_map<string, int> closet;
    while (n--) {
      string name, kind; cin >> name >> kind;
      closet[kind]++;
    }

    int combinations = 1;
    for (const auto& entry : closet)
      combinations *= (entry.second + 1);

    cout << combinations - 1 << "\n";
  }

  return 0;
}
```

