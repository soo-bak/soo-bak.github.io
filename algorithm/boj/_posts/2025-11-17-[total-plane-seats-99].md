---
layout: single
title: "[백준 8370] Plane (C#, C++) - soo:bak"
date: "2025-11-17 23:08:00 +0900"
description: 비즈니스/이코노미 좌석 수를 합산하는 백준 8370번 Plane 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 8370
  - C#
  - C++
  - 알고리즘
keywords: "백준 8370, 백준 8370번, BOJ 8370, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[8370번 - Plane](https://www.acmicpc.net/problem/8370)

## 설명

비행기의 총 좌석 수를 계산하는 문제입니다.<br>

비즈니스석은 `n1`행이 있고 각 행에 `k1`개의 좌석이 있습니다. 이코노미석은 `n2`행이 있고 각 행에 `k2`개의 좌석이 있습니다.<br>

총 좌석 수는 `n1 × k1 + n2 × k2`입니다.<br>

<br>

## 접근법

입력받은 네 개의 값을 사용하여 공식을 계산합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var n1 = int.Parse(tokens[0]);
      var k1 = int.Parse(tokens[1]);
      var n2 = int.Parse(tokens[2]);
      var k2 = int.Parse(tokens[3]);

      Console.WriteLine(n1 * k1 + n2 * k2);
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

  int n1, k1, n2, k2; cin >> n1 >> k1 >> n2 >> k2;

  cout << n1 * k1 + n2 * k2 << "\n";

  return 0;
}
```

