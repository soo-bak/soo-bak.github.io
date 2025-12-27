---
layout: single
title: "[백준 9924] The Euclidean Algorithm (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 뺄셈 기반 유클리드 알고리듬에서 최대공약수에 도달하기까지의 반복 횟수를 세는 백준 9924번 문제에 대한 C# 및 C++ 설명
tags:
  - 백준
  - BOJ
  - 9924
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 정수론
  - 시뮬레이션
  - 유클리드호제법
keywords: "백준 9924, 백준 9924번, BOJ 9924, EuclideanAlgorithm, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9924번 - The Euclidean Algorithm](https://www.acmicpc.net/problem/9924)

## 설명
뺄셈 기반 유클리드 알고리듬으로 최대공약수를 구할 때 필요한 연산 횟수를 세는 문제입니다.

<br>

## 접근법
뺄셈 기반 유클리드 알고리듬은 두 수가 같아질 때까지 큰 수에서 작은 수를 반복해서 뺍니다. 두 수가 같아지면 그 값이 최대공약수입니다. 뺄셈을 수행할 때마다 카운트를 증가시키고, 루프가 종료되면 카운트를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);

    var cnt = 0;
    while (a != b) {
      if (a > b) a -= b;
      else b -= a;
      cnt++;
    }

    Console.WriteLine(cnt);
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

  int a, b; cin >> a >> b;
  int cnt = 0;

  while (a != b) {
    if (a > b) a -= b;
    else b -= a;
    cnt++;
  }

  cout << cnt << "\n";

  return 0;
}
```
