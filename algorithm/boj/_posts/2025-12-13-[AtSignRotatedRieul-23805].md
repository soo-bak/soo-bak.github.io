---
layout: single
title: "[백준 23805] 골뱅이 찍기 - 돌아간 ㄹ (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 세 블록을 N배 확장해 돌아간 ㄹ 모양을 출력하는 백준 23805번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23805
  - C#
  - C++
  - 알고리즘
keywords: "백준 23805, 백준 23805번, BOJ 23805, AtSignRotatedRieul, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23805번 - 골뱅이 찍기 - 돌아간 ㄹ](https://www.acmicpc.net/problem/23805)

## 설명
돌아간 ㄹ자 모양의 골뱅이 패턴을 출력하는 문제입니다.

<br>

## 접근법
전체 크기는 5n x 5n이며, 세 부분으로 나누어 출력합니다.

윗부분 n줄은 골뱅이 3n개, 공백 n개, 골뱅이 n개로 구성됩니다.

중간 3n줄은 골뱅이와 공백이 n개씩 번갈아 나타나는 패턴입니다.

아랫부분 n줄은 골뱅이 n개, 공백 n개, 골뱅이 3n개로 구성됩니다.

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

    var top = new string('@', 3 * n) + new string(' ', n) + new string('@', n);
    var mid = new string('@', n) + new string(' ', n) + new string('@', n) + new string(' ', n) + new string('@', n);
    var bot = new string('@', n) + new string(' ', n) + new string('@', 3 * n);

    for (var i = 0; i < n; i++)
      sb.AppendLine(top);
    for (var i = 0; i < 3 * n; i++)
      sb.AppendLine(mid);
    for (var i = 0; i < n; i++)
      sb.AppendLine(bot);

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
  string top = string(3 * n, '@') + string(n, ' ') + string(n, '@');
  string mid = string(n, '@') + string(n, ' ') + string(n, '@') + string(n, ' ') + string(n, '@');
  string bot = string(n, '@') + string(n, ' ') + string(3 * n, '@');

  for (int i = 0; i < n; i++)
    cout << top << "\n";
  for (int i = 0; i < 3 * n; i++)
    cout << mid << "\n";
  for (int i = 0; i < n; i++)
    cout << bot << "\n";

  return 0;
}
```
