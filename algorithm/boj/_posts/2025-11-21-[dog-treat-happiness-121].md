---
layout: single
title: "[백준 19602] Dog Treats (C#, C++) - soo:bak"
date: "2025-11-21 23:41:00 +0900"
description: 1×S + 2×M + 3×L 점수로 강아지 행복 여부를 판단하는 백준 19602번 Dog Treats 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 19602
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 19602, 백준 19602번, BOJ 19602, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[19602번 - Dog Treats](https://www.acmicpc.net/problem/19602)

## 설명

강아지에게 준 세 종류의 간식 개수가 주어집니다. 작은 간식 `S`개, 중간 간식 `M`개, 큰 간식 `L`개입니다.<br>

강아지의 행복 여부를 판단하여 행복하면 `"happy"`, 아니면 `"sad"`를 출력합니다.<br>

<br>

## 접근법

강아지의 행복 점수는 `1 × S + 2 × M + 3 × L`로 계산합니다.

작은 간식은 `1`점, 중간 간식은 `2`점, 큰 간식은 `3`점의 가치를 가집니다.<br>

계산된 점수가 `10` 이상이면 `"happy"`, 미만이면 `"sad"`를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var s = int.Parse(Console.ReadLine()!);
      var m = int.Parse(Console.ReadLine()!);
      var l = int.Parse(Console.ReadLine()!);

      var score = s + 2 * m + 3 * l;
      Console.WriteLine(score >= 10 ? "happy" : "sad");
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

  int s, m, l; cin >> s >> m >> l;

  int score = s + 2 * m + 3 * l;
  cout << (score >= 10 ? "happy" : "sad") << "\n";

  return 0;
}
```

