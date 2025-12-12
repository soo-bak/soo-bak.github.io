---
layout: single
title: "[백준 21335] Another Eruption (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 넓이 a인 원형 가스 확산 영역의 둘레 2π√(a/π)를 구해 소수점 6자리로 출력하는 백준 21335번 Another Eruption 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[21335번 - Another Eruption](https://www.acmicpc.net/problem/21335)

## 설명
가스가 원형으로 퍼진 영역의 넓이가 주어질 때, 경계를 둘러싸는 테이프의 길이를 구하는 문제입니다.

<br>

## 접근법
원의 넓이가 a이면, 반지름 r은 a를 π로 나눈 값의 제곱근입니다.

둘레는 2πr이므로, 반지름을 구한 뒤 2π를 곱하면 됩니다.

결과는 소수점 아래 여섯 자리까지 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = double.Parse(Console.ReadLine()!);
    var ans = 2 * Math.PI * Math.Sqrt(a / Math.PI);
    Console.WriteLine($"{ans:F6}");
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

  double a; cin >> a;
  double ans = 2.0 * M_PI * sqrt(a / M_PI);
  cout.setf(ios::fixed);
  cout.precision(6);
  cout << ans << "\n";

  return 0;
}
```
