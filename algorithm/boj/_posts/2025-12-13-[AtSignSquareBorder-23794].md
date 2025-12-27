---
layout: single
title: "[백준 23794] 골뱅이 찍기 - 정사각형 (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 위아래는 @를 N+2개, 가운데는 양쪽 @와 가운데 공백으로 정사각형 테두리를 출력하는 백준 23794번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23794
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 23794, 백준 23794번, BOJ 23794, AtSignSquareBorder, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23794번 - 골뱅이 찍기 - 정사각형](https://www.acmicpc.net/problem/23794)

## 설명
정사각형 테두리 모양의 골뱅이 패턴을 출력하는 문제입니다.

<br>

## 접근법
전체 크기는 (n + 2) x (n + 2)가 됩니다.

첫 줄과 마지막 줄은 골뱅이를 n + 2개 출력합니다.

중간 n줄은 양쪽에 골뱅이 하나씩, 가운데 n칸은 공백으로 채웁니다.

<br>

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var len = n + 2;
    var sb = new StringBuilder();
    var full = new string('@', len);
    var mid = "@" + new string(' ', n) + "@";

    sb.AppendLine(full);
    for (var i = 0; i < n; i++)
      sb.AppendLine(mid);
    sb.AppendLine(full);

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
  int len = n + 2;
  string full(len, '@');
  string mid = "@" + string(n, ' ') + "@";

  cout << full << "\n";
  for (int i = 0; i < n; i++)
    cout << mid << "\n";
  cout << full << "\n";

  return 0;
}
```
