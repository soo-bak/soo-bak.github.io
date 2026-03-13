---
layout: single
title: "[백준 24313] 알고리즘 수업 - 점근적 표기 1 (C#, C++) - soo:bak"
date: "2026-03-13 23:41:00 +0900"
description: "백준 24313번 C#, C++ 풀이 - f(n)=a1n+a0가 주어진 c와 n0에 대해 O(n) 정의를 만족하는지 판정하는 문제"
tags:
  - 백준
  - BOJ
  - 24313
  - C#
  - C++
  - 알고리즘
  - 수학
keywords: "백준 24313, 백준 24313번, BOJ 24313, 알고리즘 수업 - 점근적 표기 1, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24313번 - 알고리즘 수업 - 점근적 표기 1](https://www.acmicpc.net/problem/24313)

## 설명
함수 `f(n) = a1n + a0`가 주어진 `c`, `n0`에 대해 문제에서 정의한 `O(n)` 조건을 만족하는지 판정하는 문제입니다.

<br>

## 접근법
문제의 조건은 모든 `n >= n0`에 대해 다음 부등식이 성립하는지 확인하는 것입니다.

`a1n + a0 <= cn`

이를 정리하면 다음과 같습니다.

`(a1 - c)n + a0 <= 0`

여기서 `a1 > c`이면 `n`이 커질수록 왼쪽 값이 증가하므로, 어떤 시점부터는 반드시 조건을 만족할 수 없습니다. 따라서 `a1 <= c`가 먼저 필요합니다.

그리고 `a1 <= c`이면 왼쪽 식은 `n`이 커질수록 감소하거나 그대로이므로, 가장 작은 검사 지점인 `n0`에서만 확인하면 충분합니다.  
즉 아래 두 조건을 모두 만족하면 정답은 `1`, 아니면 `0`입니다.

- `a1 <= c`
- `a1 * n0 + a0 <= c * n0`

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int[] line = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    int a1 = line[0];
    int a0 = line[1];
    int c = int.Parse(Console.ReadLine()!);
    int n0 = int.Parse(Console.ReadLine()!);

    if (a1 <= c && a1 * n0 + a0 <= c * n0)
      Console.WriteLine(1);
    else
      Console.WriteLine(0);
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

  int a1, a0, c, n0;
  cin >> a1 >> a0;
  cin >> c;
  cin >> n0;

  if (a1 <= c && a1 * n0 + a0 <= c * n0)
    cout << 1 << "\n";
  else
    cout << 0 << "\n";

  return 0;
}
```
