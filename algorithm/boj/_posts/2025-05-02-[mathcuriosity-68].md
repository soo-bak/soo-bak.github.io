---
layout: single
title: "[백준 9094] 수학적 호기심 (C#, C++) - soo:bak"
date: "2025-05-02 20:48:00 +0900"
description: 두 정수 쌍 (a, b)에 대해 조건을 만족하는 경우의 수를 구하는 백준 9094번 수학적 호기심 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9094
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 9094, 백준 9094번, BOJ 9094, mathcuriosity, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9094번 - 수학적 호기심](https://www.acmicpc.net/problem/9094)

## 설명
두 정수 `n`과 `m`이 주어졌을 때, 다음 조건을 만족하는 정수 쌍 `(a, b)`의 개수를 구하는 문제입니다.

$$ \frac{a^2 + b^2 + m}{a \cdot b} $$


## 접근법

- `1` 이상 `n - 1` 미만의 두 정수 `a`, `b` 쌍을 모두 확인합니다. 이때 `a < b` 조건을 만족해야 합니다.
- 각 쌍에 대해 $$a^2 + b^2 + m$$ 을 계산한 뒤, 이 값이 $$a \cdot b$$로 나누어떨어지는지 확인합니다.
- 조건을 만족하는 쌍이 나올 때마다 개수를 세어, 그 총합을 정답으로 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split();
      int n = int.Parse(tokens[0]);
      int m = int.Parse(tokens[1]);

      int count = 0;
      for (int a = 1; a < n - 1; a++) {
        for (int b = a + 1; b < n; b++) {
          if ((a * a + b * b + m) % (a * b) == 0)
            count++;
        }
      }
      Console.WriteLine(count);
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
    int n, m; cin >> n >> m;
    int ans = 0;
    for (int a = 1; a < n; a++) {
      for (int b = a + 1; b < n; b++) {
        if ((a * a + b * b + m) % (a * b) == 0)
          ans++;
      }
    }
    cout << ans << "\n";
  }

  return 0;
}
```
