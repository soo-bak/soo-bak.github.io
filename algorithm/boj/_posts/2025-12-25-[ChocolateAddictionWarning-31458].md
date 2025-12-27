---
layout: single
title: "[백준 31458] !!초콜릿 중독 주의!! (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 31458번 C#, C++ 풀이 - 0/1과 느낌표만 있는 수식을 규칙대로 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 31458
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 31458, 백준 31458번, BOJ 31458, ChocolateAddictionWarning, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31458번 - !!초콜릿 중독 주의!!](https://www.acmicpc.net/problem/31458)

## 설명
느낌표와 0/1로만 이루어진 수식이 주어질 때 규칙에 따라 값을 계산하는 문제입니다.

<br>

## 접근법
팩토리얼은 0과 1 모두 1이므로, 숫자 뒤의 `!`는 있으면 값이 1로 고정됩니다.  
앞의 `!`는 논리 반전이므로 개수의 홀짝으로 최종 값을 뒤집으면 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    for (var tc = 0; tc < t; tc++) {
      var s = Console.ReadLine()!;
      var n = s.Contains('1') ? 1 : 0;
      var pos = s.IndexOf('0');
      if (pos == -1) pos = s.IndexOf('1');

      var left = pos;
      var right = s.Length - pos - 1;

      if (right > 0) n = 1;
      if ((left & 1) == 1) n = 1 - n;

      sb.AppendLine(n.ToString());
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

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;
    int n = s.find('1') != string::npos ? 1 : 0;
    int pos = s.find('0');
    if (pos == (int)string::npos) pos = s.find('1');

    int left = pos;
    int right = (int)s.size() - pos - 1;

    if (right > 0) n = 1;
    if (left % 2 == 1) n = 1 - n;

    cout << n << "\n";
  }

  return 0;
}
```
