---
layout: single
title: "[백준 4527] Patterns and Pictures (C#, C++) - soo:bak"
date: "2026-04-17 21:33:00 +0900"
description: "백준 4527번 C#, C++ 풀이 - 한 full set의 전체 넓이를 구한 뒤 1, 2, 3제곱야드에 들어가는 개수를 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 4527
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 4527, 백준 4527번, BOJ 4527, Patterns and Pictures, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4527번 - Patterns and Pictures](https://www.acmicpc.net/problem/4527)

## 설명
패턴을 이루는 이미지들의 넓이와 개수가 주어질 때, 1제곱야드, 2제곱야드, 3제곱야드 안에 최대 몇 개의 full set이 들어갈 수 있는지 구하는 문제입니다.

<br>

## 접근법
이미지 배치 방법은 중요하지 않고, 한 full set이 차지하는 전체 넓이만 알면 됩니다.

각 이미지에 대해 `넓이 × 개수`를 더하면 한 full set의 넓이가 나옵니다. 1야드는 36인치이므로 1제곱야드는 `36 × 36 = 1296` 제곱인치입니다.

따라서 답은 각각 `1296 / setArea`, `2592 / setArea`, `3888 / setArea`의 몫입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine()!);

    for (int tc = 0; tc < t; tc++) {
      int images = int.Parse(Console.ReadLine()!);
      long setArea = 0;

      for (int i = 0; i < images; i++) {
        long[] input = Console.ReadLine()!.Split().Select(long.Parse).ToArray();
        long s = input[0];
        long r = input[1];
        setArea += s * r;
      }

      Console.WriteLine($"{1296 / setArea} {2592 / setArea} {3888 / setArea}");
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

  int t;
  cin >> t;

  while (t--) {
    int images;
    cin >> images;

    long long setArea = 0;
    for (int i = 0; i < images; i++) {
      long long s, r;
      cin >> s >> r;
      setArea += s * r;
    }

    cout << 1296 / setArea << " "
         << 2592 / setArea << " "
         << 3888 / setArea << "\n";
  }

  return 0;
}
```
