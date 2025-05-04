---
layout: single
title: "[백준 10698] Ahmed Aly (C#, C++) - soo:bak"
date: "2025-05-04 19:04:00 +0900"
description: 단순한 사칙연산 수식을 입력받아 식이 맞는지 판별하는 시뮬레이션 문제, 백준 10698번 Ahmed Aly 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10698번 - Ahmed Aly](https://www.acmicpc.net/problem/10698)

## 설명
`덧셈` 또는 `뺄셈` 수식이 주어졌을 때, 해당 수식이 올바른지를 판별하는 문제입니다.

각 테스트케이스는 다음 형식의 문자열로 주어집니다:<br>
`X + Y = Z` 또는 `X - Y = Z`

<br>

## 접근법

- 테스트케이스 수를 입력받고, 그만큼 수식 입력을 반복합니다.
- 각 수식을 정수 `X`, `Y`, `Z`와 연산자 `+` 또는 `-`로 분리하여 분석합니다.
- 주어진 연산자가 덧셈인 경우 `X + Y == Z`, 뺄셈인 경우 `X - Y == Z`를 판별합니다.
- 각 테스트케이스마다 `"Case n: YES"` 또는 `"Case n: NO"` 형식으로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    for (int i = 1; i <= t; i++) {
      var parts = Console.ReadLine().Split();
      int x = int.Parse(parts[0]);
      string op = parts[1];
      int y = int.Parse(parts[2]);
      int z = int.Parse(parts[4]);

      bool correct = op == "+" ? x + y == z : x - y == z;
      Console.WriteLine($"Case {i}: {(correct ? "YES" : "NO")}");
    }
  }
}
```

<br>

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  for (int i = 1; i <= t; i++) {
    int l, r, a;
    string o, tmp;
    cin >> l >> o >> r >> tmp >> a;
    bool ok = (o == "+" ? l + r == a : l - r == a);
    cout << "Case " << i << ": " << (ok ? "YES" : "NO") << "\n";
  }

  return 0;
}
```
