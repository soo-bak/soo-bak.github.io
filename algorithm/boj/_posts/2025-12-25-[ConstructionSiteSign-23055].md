---
layout: single
title: "[백준 23055] 공사장 표지판 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 23055번 C#, C++ 풀이 - 테두리와 대각선을 별로 채워 N×N 표지판을 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 23055
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 23055, 백준 23055번, BOJ 23055, ConstructionSiteSign, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23055번 - 공사장 표지판](https://www.acmicpc.net/problem/23055)

## 설명
크기 N×N의 출입제한 표지판을 규칙에 맞게 출력하는 문제입니다.

<br>

## 접근법
첫 줄과 마지막 줄은 전부 `*`로 채웁니다.  
나머지 줄은 양 끝과 두 대각선 위치에만 `*`을 놓고 나머지는 공백으로 채웁니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    for (var i = 0; i < n; i++) {
      if (i == 0 || i == n - 1) {
        sb.AppendLine(new string('*', n));
        continue;
      }

      var row = new char[n];
      for (var j = 0; j < n; j++) row[j] = ' ';
      row[0] = '*';
      row[n - 1] = '*';
      row[i] = '*';
      row[n - 1 - i] = '*';
      sb.AppendLine(new string(row));
    }

    Console.Write(sb);
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

  int n; cin >> n;
  for (int i = 0; i < n; i++) {
    if (i == 0 || i == n - 1) {
      cout << string(n, '*') << "\n";
      continue;
    }

    string row(n, ' ');
    row[0] = '*';
    row[n - 1] = '*';
    row[i] = '*';
    row[n - 1 - i] = '*';
    cout << row << "\n";
  }

  return 0;
}
```
