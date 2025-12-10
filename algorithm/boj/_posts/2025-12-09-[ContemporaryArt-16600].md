---
layout: single
title: "[백준 16600] Contemporary Art (C#, C++) - soo:bak"
date: "2025-12-09 13:05:00 +0900"
description: 정사각형 넓이 a가 주어질 때 둘레 4√a를 구해 소수점 이하 6자리로 출력하는 백준 16600번 Contemporary Art 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[16600번 - Contemporary Art](https://www.acmicpc.net/problem/16600)

## 설명
정사각형 액자의 넓이가 주어질 때, 액자 테두리에 두를 필라멘트의 길이를 구하는 문제입니다.

<br>

## 접근법
정사각형의 넓이가 a이면 한 변의 길이는 a의 제곱근입니다.

둘레는 한 변의 네 배이므로, 제곱근을 구한 뒤 4를 곱하면 됩니다.

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
    var ans = 4 * Math.Sqrt(a);
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
  double ans = 4.0L * sqrt(a);
  cout.setf(ios::fixed);
  cout.precision(6);
  cout << ans << "\n";

  return 0;
}
```
