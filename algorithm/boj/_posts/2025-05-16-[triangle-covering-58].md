---
layout: single
title: "[백준 11312] 삼각 무늬 - 2 (C#, C++) - soo:bak"
date: "2025-05-16 21:14:00 +0900"
description: 큰 정삼각형을 작은 정삼각형으로 정확히 덮기 위한 최소 개수를 계산하는 백준 11312번 삼각 무늬 - 2 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11312
  - C#
  - C++
  - 알고리즘
keywords: "백준 11312, 백준 11312번, BOJ 11312, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11312번 - 삼각 무늬 - 2](https://www.acmicpc.net/problem/11312)

## 설명

`한 변의 길이가 큰 정삼각형`**을** `동일한 형태의 작은 정삼각형`**으로 정확히 덮으려 할 때, 필요한 개수를 구하는 문제입니다.**

<br>
입력으로는 다음 두 값이 주어집니다:

- `A`: 큰 정삼각형의 한 변 길이
- `B`: 작은 정삼각형의 한 변 길이

<br>
이때 조건은 `B`가 `A`를 나누어 떨어지며, 정삼각형의 방향이 일정하게 정렬되어 있다는 가정 하에

큰 삼각형을 `B` 단위의 작은 삼각형으로 **빈틈없이** 덮는 데 필요한 최소 개수를 구해야 합니다.

<br>

## 접근법

정삼각형을 동일한 방향의 작은 정삼각형으로 채우는 경우, 가장 간단한 방법은 다음과 같습니다:

- 한 변에 들어가는 개수는 `A / B` 개입니다.
- 정삼각형은 계단처럼 줄어드는 구조이므로, 전체 면적은 **작은 삼각형을 정사각형처럼 배치했을 때의 개수**와 같습니다.

그 결과, 최종 개수는 다음과 같이 구할 수 있습니다:

$$
\left(\frac{A}{B}\right)^2
$$

이는 한 줄에 `A / B`개의 삼각형이 있고, 이런 줄이 `A / B`줄 반복된다는 구조를 떠올리면 이해하기 쉽습니다.

문제에서 항상 `B <= A`가 보장되므로 나눗셈 결과는 정수입니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split();
      long a = long.Parse(tokens[0]);
      long b = long.Parse(tokens[1]);
      long res = (a / b) * (a / b);
      Console.WriteLine(res);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    ll a, b; cin >> a >> b;
    cout << (a / b) * (a / b) << "\n";
  }

  return 0;
}
```
