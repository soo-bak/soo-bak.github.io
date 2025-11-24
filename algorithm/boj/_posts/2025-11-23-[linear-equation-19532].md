---
layout: single
title: "[백준 19532] 수학은 비대면강의입니다 (C#, C++) - soo:bak"
date: "2025-11-23 04:05:00 +0900"
description: 2×2 연립방정식을 Cramer의 공식으로 풀어 정수 해를 찾는 백준 19532번 문제의 C# 및 C++ 풀이
---

## 문제 링크
[19532번 - 수학은 비대면강의입니다](https://www.acmicpc.net/problem/19532)

## 설명

다음 연립방정식에서 `x`, `y`를 찾는 문제입니다.

```
ax + by = c
dx + ey = f
```

해가 유일하고, `x`, `y`가 `-999` 이상 `999` 이하의 정수인 입력만 주어집니다.

<br>

## 접근법

2×2 연립방정식은 Cramer의 공식으로 바로 풀 수 있습니다. 행렬식 `det = a×e - b×d`가 0이 아니므로 해가 유일합니다.

```
x = (c×e - b×f) / det
y = (a×f - c×d) / det
```

입력 범위가 작고 나눗셈 결과가 항상 정수로 떨어지도록 보장되므로 위 식을 정수 연산으로 계산해 출력하면 됩니다.

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
      int a = int.Parse(tokens[0]);
      int b = int.Parse(tokens[1]);
      int c = int.Parse(tokens[2]);
      int d = int.Parse(tokens[3]);
      int e = int.Parse(tokens[4]);
      int f = int.Parse(tokens[5]);

      int det = a * e - b * d;
      int x = (c * e - b * f) / det;
      int y = (a * f - c * d) / det;

      Console.WriteLine($"{x} {y}");
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

  int a, b, c, d, e, f; cin >> a >> b >> c >> d >> e >> f;

  int det = a * e - b * d;
  int x = (c * e - b * f) / det;
  int y = (a * f - c * d) / det;

  cout << x << ' ' << y << '\n';

  return 0;
}
```

