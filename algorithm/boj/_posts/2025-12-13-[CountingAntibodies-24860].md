---
layout: single
title: "[백준 24860] Counting Antibodies (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: 경쇄 두 타입 조합 수(VJ 합)와 중쇄 조합 수(VDJ 곱)를 곱해 면역글로불린 가짓수를 구하는 백준 24860번 Counting Antibodies 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 24860
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
  - 조합론
keywords: "백준 24860, 백준 24860번, BOJ 24860, CountingAntibodies, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24860번 - Counting Antibodies](https://www.acmicpc.net/problem/24860)

## 설명
경쇄와 중쇄의 조합으로 만들 수 있는 면역글로불린의 가짓수를 구하는 문제입니다.

<br>

## 접근법
경쇄는 κ형과 λ형이 있으며, 각각 V와 J 조각을 선택합니다.

경쇄 가짓수는 두 타입의 조합 수를 합한 것이고, 중쇄 가짓수는 V, D, J 조각의 곱입니다.

면역글로불린은 경쇄와 중쇄 각각 하나씩 조합하므로 두 값을 곱하여 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var kappa = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
    var lambda = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
    var heavy = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);

    var light = kappa[0] * kappa[1] + lambda[0] * lambda[1];
    var heavyCnt = heavy[0] * heavy[1] * heavy[2];
    Console.WriteLine(light * heavyCnt);
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

  ll vk, jk; cin >> vk >> jk;
  ll vl, jl; cin >> vl >> jl;
  ll vh, dh, jh; cin >> vh >> dh >> jh;

  ll light = vk * jk + vl * jl;
  ll heavy = vh * dh * jh;
  cout << light * heavy << "\n";

  return 0;
}
```
