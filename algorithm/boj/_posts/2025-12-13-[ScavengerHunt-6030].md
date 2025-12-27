---
layout: single
title: "[백준 6030] Scavenger Hunt (C#, C++) - soo:bak"
date: "2025-12-13 22:20:00 +0900"
description: P의 약수와 Q의 약수를 오름차순으로 나열해 모든 조합을 출력하는 백준 6030번 Scavenger Hunt 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 6030
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
  - 정수론
keywords: "백준 6030, 백준 6030번, BOJ 6030, ScavengerHunt, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6030번 - Scavenger Hunt](https://www.acmicpc.net/problem/6030)

## 설명
p의 약수와 q의 약수로 만들 수 있는 모든 순서쌍을 출력하는 문제입니다.

<br>

## 접근법
1부터 각 수까지 순회하며 나누어떨어지는 수를 약수로 저장합니다.

p의 약수와 q의 약수를 이중 반복으로 조합해 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var pq = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    var p = pq[0];
    var q = pq[1];
    var fp = new List<int>();
    var fq = new List<int>();

    for (var i = 1; i <= p; i++)
      if (p % i == 0) fp.Add(i);
    for (var i = 1; i <= q; i++)
      if (q % i == 0) fq.Add(i);

    foreach (var a in fp) {
      foreach (var b in fq)
        Console.WriteLine($"{a} {b}");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int p, q; cin >> p >> q;
  vi fp, fq;
  for (int i = 1; i <= p; i++)
    if (p % i == 0) fp.push_back(i);
  for (int i = 1; i <= q; i++)
    if (q % i == 0) fq.push_back(i);

  for (int a : fp) {
    for (int b : fq)
      cout << a << " " << b << "\n";
  }

  return 0;
}
```
