---
layout: single
title: "[백준 18096] Арифметическая магия (C#, C++) - soo:bak"
date: "2025-11-22 03:07:00 +0900"
description: 연산 결과가 항상 1이 되는 수학 마술을 그대로 구현하는 백준 18096번 Арифметическая магия 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 18096
  - C#
  - C++
  - 알고리즘
keywords: "백준 18096, 백준 18096번, BOJ 18096, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18096번 - Арифметическая магия](https://www.acmicpc.net/problem/18096)

## 설명

두 수 `x`와 `y`를 생각한 후, 특정 연산을 수행한 결과를 `N`제곱한 값을 구하는 문제입니다.

입력으로 정수 `N`이 주어지며, 결과를 출력해야 합니다.

<br>

## 접근법

문제에서 제시한 연산을 수식으로 표현하면 `((x + 1)(y + 1) - x - y - xy)^N`입니다.

괄호 안의 식을 전개하면 `(xy + x + y + 1) - x - y - xy = 1`이 되어 항상 1이 됩니다.

따라서 `x`와 `y`의 값에 관계없이 괄호 안의 결과는 항상 1이며, 최종 결과는 `1^N = 1`입니다.

즉, 입력 `N`의 값과 관계없이 항상 1을 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      Console.WriteLine(1);
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

  cout << 1 << "\n";

  return 0;
}
```
