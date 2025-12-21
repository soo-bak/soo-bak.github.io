---
layout: single
title: "[백준 25774] Simplified Calendar System (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: 단순 달력에서 두 날짜의 일수 차로 요일을 계산하는 문제
---

## 문제 링크
[25774번 - Simplified Calendar System](https://www.acmicpc.net/problem/25774)

## 설명
1년 360일(12개월, 각 30일)인 달력에서 두 날짜가 주어질 때, 두 번째 날짜의 요일을 구하는 문제입니다.

<br>

## 접근법
각 날짜를 연도, 월, 일을 기반으로 절대 일수로 변환한 뒤 두 날짜의 차이를 구합니다.

이후 첫 번째 날짜의 요일에 일수 차이를 더하고 7로 나눈 나머지를 이용해 두 번째 날짜의 요일을 계산합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int ToDays(int d, int m, int y) {
    return y * 360 + (m - 1) * 30 + (d - 1);
  }

  static void Main() {
    var first = Console.ReadLine()!.Split();
    var d1 = int.Parse(first[0]);
    var m1 = int.Parse(first[1]);
    var y1 = int.Parse(first[2]);
    var n = int.Parse(first[3]);

    var second = Console.ReadLine()!.Split();
    var d2 = int.Parse(second[0]);
    var m2 = int.Parse(second[1]);
    var y2 = int.Parse(second[2]);

    var diff = ToDays(d2, m2, y2) - ToDays(d1, m1, y1);
    var ans = (n - 1 + diff) % 7 + 1;

    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int toDays(int d, int m, int y) {
  return y * 360 + (m - 1) * 30 + (d - 1);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int d1, m1, y1, n; cin >> d1 >> m1 >> y1 >> n;
  int d2, m2, y2; cin >> d2 >> m2 >> y2;

  int diff = toDays(d2, m2, y2) - toDays(d1, m1, y1);
  int ans = (n - 1 + diff) % 7 + 1;

  cout << ans << "\n";

  return 0;
}
```
