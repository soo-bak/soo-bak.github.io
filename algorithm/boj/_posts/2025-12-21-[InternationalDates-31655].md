---
layout: single
title: "[백준 31655] International Dates (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 31655번 C#, C++ 풀이 - 월/일/연도 혹은 일/월/연도 표현인지 판별해 지역을 구분하는 문제"
tags:
  - 백준
  - BOJ
  - 31655
  - C#
  - C++
  - 알고리즘
keywords: "백준 31655, 백준 31655번, BOJ 31655, InternationalDates, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31655번 - International Dates](https://www.acmicpc.net/problem/31655)

## 설명
날짜 표기가 미국식인지 유럽식인지 판별하는 문제입니다.

<br>

## 접근법
미국식은 월/일/연도 순서이고, 유럽식은 일/월/연도 순서입니다. 첫 번째 숫자가 1부터 12 사이이면 미국식으로 해석 가능하고, 두 번째 숫자가 1부터 12 사이이면 유럽식으로 해석 가능합니다.

둘 다 가능하면 either, 미국식만 가능하면 US, 유럽식만 가능하면 EU를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split('/');
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);

    var us = a >= 1 && a <= 12;
    var eu = b >= 1 && b <= 12;

    if (us && eu) Console.WriteLine("either");
    else if (us) Console.WriteLine("US");
    else Console.WriteLine("EU");
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

  string s; cin >> s;
  int a, b, y; char slash;
  stringstream ss(s);
  ss >> a >> slash >> b >> slash >> y;

  bool us = (1 <= a && a <= 12);
  bool eu = (1 <= b && b <= 12);

  if (us && eu) cout << "either\n";
  else if (us) cout << "US\n";
  else cout << "EU\n";

  return 0;
}
```
