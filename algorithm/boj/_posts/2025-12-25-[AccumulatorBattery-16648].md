---
layout: single
title: "[백준 16648] Accumulator Battery (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 16648번 C#, C++ 풀이 - 배터리 소모 속도를 역산해 남은 시간을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 16648
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 16648, 백준 16648번, BOJ 16648, AccumulatorBattery, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16648번 - Accumulator Battery](https://www.acmicpc.net/problem/16648)

## 설명
출발 시 배터리 100%에서 시작해 t분 뒤 p%가 되었을 때, 만난 이후 배터리가 0%가 될 때까지의 시간을 구하는 문제입니다.

<br>

## 접근법
20% 이상에서는 정상 모드(속도 r), 20% 아래에서는 에코 모드(속도 r/2)로 소모됩니다.  
p ≥ 20이면 아직 정상 모드이므로 r = (100 − p) / t, 남은 시간은 (p − 20)/r + 20/(r/2) = (p + 20) / r입니다.  
p < 20이면 이미 에코 모드이며 p = 60 − (r/2)·t가 되어 r = 2(60 − p) / t, 남은 시간은 p / (r/2) = p·t / (60 − p)입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var t = double.Parse(parts[0]);
    var p = double.Parse(parts[1]);

    double ans;
    if (p >= 20.0) {
      var r = (100.0 - p) / t;
      ans = (p + 20.0) / r;
    } else ans = p * t / (60.0 - p);

    Console.WriteLine(ans.ToString("0.000000"));
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

  double t, p; cin >> t >> p;
  double ans;
  if (p >= 20.0) {
    double r = (100.0 - p) / t;
    ans = (p + 20.0) / r;
  } else ans = p * t / (60.0 - p);

  cout << fixed << setprecision(6) << ans << "\n";

  return 0;
}
```
