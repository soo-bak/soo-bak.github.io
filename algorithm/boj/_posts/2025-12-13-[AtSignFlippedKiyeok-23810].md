---
layout: single
title: "[백준 23810] 골뱅이 찍기 - 뒤집힌 ㅋ (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 위·가운데 가로줄과 왼쪽 세로줄을 N배 확장해 뒤집힌 ㅋ 모양을 출력하는 백준 23810번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23810
  - C#
  - C++
  - 알고리즘
keywords: "백준 23810, 백준 23810번, BOJ 23810, AtSignFlippedKiyeok, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23810번 - 골뱅이 찍기 - 뒤집힌 ㅋ](https://www.acmicpc.net/problem/23810)

## 설명
뒤집힌 ㅋ자 모양의 골뱅이 패턴을 출력하는 문제입니다.

<br>

## 접근법
전체 크기는 5n x 5n이 됩니다.

위쪽 가로줄은 첫 n줄, 가운데 가로줄은 2n번째부터 3n번째 행 직전까지입니다.

왼쪽 세로줄은 열 인덱스가 n 미만인 경우입니다.

이후, 위 조건 중 하나라도 만족하면 골뱅이를 출력하고, 그 외에는 출력하지 않습니다.

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
    for (var i = 0; i < 5 * n; i++) {
      for (var j = 0; j < 5 * n; j++) {
        if (i < n) sb.Append('@');
        else if (i > 2 * n - 1 && i < 3 * n) sb.Append('@');
        else if (j < n) sb.Append('@');
      }
      sb.Append('\n');
    }
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
  for (int i = 0; i < 5 * n; i++) {
    for (int j = 0; j < 5 * n; j++) {
      if (i < n) cout << "@";
      else if (i > 2 * n - 1 && i < 3 * n) cout << "@";
      else if (j < n) cout << "@";
    }
    cout << "\n";
  }

  return 0;
}
```
