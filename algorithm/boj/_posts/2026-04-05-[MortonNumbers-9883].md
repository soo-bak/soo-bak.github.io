---
layout: single
title: "[백준 9883] Morton Numbers (C#, C++) - soo:bak"
date: "2026-04-05 19:52:00 +0900"
description: "백준 9883번 C#, C++ 풀이 - x와 y의 비트를 번갈아 끼워 넣어 Morton number를 만드는 문제"
tags:
  - 백준
  - BOJ
  - 9883
  - C#
  - C++
  - 알고리즘
  - 비트마스킹
  - 구현
keywords: "백준 9883, 백준 9883번, BOJ 9883, Morton Numbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9883번 - Morton Numbers](https://www.acmicpc.net/problem/9883)

## 설명
두 정수 `x`, `y`의 비트를 번갈아 끼워 넣어 Morton number를 만드는 문제입니다.

<br>

## 접근법
`x`와 `y`는 최대 `16`비트이므로, 각 비트를 하나씩 꺼내서 결과 값의 알맞은 위치에 넣으면 됩니다.

문제의 위치는 `1`부터 세므로, 구현에서 `i`번째 비트를 볼 때 `y`의 비트는 결과의 `2i`번째 위치에, `x`의 비트는 `2i + 1`번째 위치에 넣어야 합니다. 이 과정을 `0`부터 `15`까지 반복하면 Morton number가 완성됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string[] input = Console.ReadLine()!.Split();
    ulong x = ulong.Parse(input[0]);
    ulong y = ulong.Parse(input[1]);

    ulong answer = 0;

    for (int i = 0; i < 16; i++) {
      answer |= ((y >> i) & 1UL) << (2 * i);
      answer |= ((x >> i) & 1UL) << (2 * i + 1);
    }

    Console.WriteLine(answer);
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

  unsigned long long x, y;
  cin >> x >> y;

  unsigned long long answer = 0;

  for (int i = 0; i < 16; i++) {
    answer |= ((y >> i) & 1ULL) << (2 * i);
    answer |= ((x >> i) & 1ULL) << (2 * i + 1);
  }

  cout << answer << "\n";

  return 0;
}
```
