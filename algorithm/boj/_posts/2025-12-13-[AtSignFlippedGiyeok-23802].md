---
layout: single
title: "[백준 23802] 골뱅이 찍기 - 뒤집힌 ㄱ (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 위쪽 가로줄과 왼쪽 세로줄을 N배 확장해 뒤집힌 ㄱ자를 출력하는 백준 23802번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[23802번 - 골뱅이 찍기 - 뒤집힌 ㄱ](https://www.acmicpc.net/problem/23802)

## 설명
뒤집힌 ㄱ자 모양의 골뱅이 패턴을 출력하는 문제입니다.

<br>

## 접근법
전체 높이는 5n이 됩니다.

첫 n줄은 5n개의 골뱅이를 출력합니다.

나머지 4n줄은 왼쪽 n칸만 골뱅이로 채웁니다.

<br>

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    var full = new string('@', 5 * n);
    var col = new string('@', n);

    for (var i = 0; i < n; i++)
      sb.AppendLine(full);
    for (var i = 0; i < 4 * n; i++)
      sb.AppendLine(col);

    Console.Write(sb.ToString());
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

  int n;
  if (!(cin >> n)) return 0;
  string full(5 * n, '@');
  string col(n, '@');

  for (int i = 0; i < n; i++)
    cout << full << "\n";
  for (int i = 0; i < 4 * n; i++)
    cout << col << "\n";

  return 0;
}
```
