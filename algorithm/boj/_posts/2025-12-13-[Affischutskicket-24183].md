---
layout: single
title: "[백준 24183] Affischutskicket (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: C4 봉투(두 장), A3 포스터 두 장, A4 안내문 한 장의 면적과 제지 gsm을 곱해 총 무게를 구하는 백준 24183번 Affischutskicket 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 24183
  - C#
  - C++
  - 알고리즘
keywords: "백준 24183, 백준 24183번, BOJ 24183, Affischutskicket, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24183번 - Affischutskicket](https://www.acmicpc.net/problem/24183)

## 설명
봉투, 포스터, 안내문 용지의 평량이 주어질 때, 우편물의 총 무게를 구하는 문제입니다.

<br>

## 접근법
봉투는 C4 규격 두 장, 포스터는 A3 규격 두 장, 안내문은 A4 규격 한 장입니다.

각 규격의 면적을 제곱미터로 환산한 뒤, 평량을 곱하면 한 장의 무게가 됩니다.

모든 용지의 무게를 더한 값을 소수점 아래 여섯 자리까지 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    const double mm2ToM2 = 1e-6;
    const double C4 = 229 * 324 * mm2ToM2;
    const double A3 = 297 * 420 * mm2ToM2;
    const double A4 = 210 * 297 * mm2ToM2;

    var line = Console.ReadLine()!.Split();
    var gEnv = double.Parse(line[0]);
    var gPoster = double.Parse(line[1]);
    var gInfo = double.Parse(line[2]);

    var weight = 2 * C4 * gEnv + 2 * A3 * gPoster + A4 * gInfo;
    Console.WriteLine($"{weight:F6}");
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

  const double mm2ToM2 = 1e-6;
  const double C4 = 229 * 324 * mm2ToM2;
  const double A3 = 297 * 420 * mm2ToM2;
  const double A4 = 210 * 297 * mm2ToM2;

  double gEnv, gPoster, gInfo; cin >> gEnv >> gPoster >> gInfo;
  double weight = 2 * C4 * gEnv + 2 * A3 * gPoster + A4 * gInfo;

  cout.setf(ios::fixed);
  cout.precision(6);
  cout << weight << "\n";

  return 0;
}
```
