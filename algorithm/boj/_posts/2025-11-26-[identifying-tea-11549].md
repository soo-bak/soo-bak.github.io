---
layout: single
title: "[백준 11549] Identifying tea (C#, C++) - soo:bak"
date: "2025-11-26 23:00:00 +0900"
description: 실제 차 종류와 5명의 답안을 비교해 맞힌 사람 수를 세는 백준 11549번 Identifying tea 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 11549
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 11549, 백준 11549번, BOJ 11549, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11549번 - Identifying tea](https://www.acmicpc.net/problem/11549)

## 설명

1부터 4까지의 숫자로 표현되는 실제 차의 종류와 5명의 답안이 주어질 때, 정답을 맞힌 사람의 수를 구하는 문제입니다.

각 사람의 답안은 1부터 4까지의 숫자로 주어집니다.

<br>

## 접근법

실제 차의 종류를 먼저 입력받은 후, 5명의 답안을 순서대로 비교합니다.

각 답안이 실제 차의 종류와 일치하는지 확인하고, 일치할 때마다 정답자 수를 증가시킵니다.

예를 들어, 실제 차가 2번이고 5명의 답안이 2, 1, 2, 3, 2라면, 첫 번째, 세 번째, 다섯 번째 사람이 정답을 맞혔으므로 답은 3입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var parts = Console.ReadLine()!.Split();

      var cnt = 0;

      for (var i = 0; i < 5; i++)
        if (int.Parse(parts[i]) == t)
          cnt++;

      Console.WriteLine(cnt);
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

  int cnt = 0;
  for (int i = 0; i < 5; i++) {
    int x; cin >> x;
    if (x == t) ++cnt;
  }

  cout << cnt << "\n";

  return 0;
}
```

