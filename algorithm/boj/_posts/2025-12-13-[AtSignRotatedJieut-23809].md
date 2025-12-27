---
layout: single
title: "[백준 23809] 골뱅이 찍기 - 돌아간 ㅈ (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 다섯 블록을 N배 확장해 돌아간 ㅈ 모양을 출력하는 백준 23809번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23809
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 23809, 백준 23809번, BOJ 23809, AtSignRotatedJieut, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23809번 - 골뱅이 찍기 - 돌아간 ㅈ](https://www.acmicpc.net/problem/23809)

## 설명
돌아간 ㅈ자 모양의 골뱅이 패턴을 출력하는 문제입니다.

<br>

## 접근법
전체 크기는 5n x 5n이며, 다섯 블록으로 나누어 출력합니다.

첫 번째와 다섯 번째 블록은 양쪽 n개씩 골뱅이와 가운데 3n개 공백으로 구성됩니다.

두 번째와 네 번째 블록은 양쪽 n개씩 골뱅이와 가운데 2n개 공백으로 구성됩니다.

세 번째 블록은 3n개의 골뱅이로 채웁니다.

이후, 각 블록을 높이 n만큼 순서대로 출력합니다.

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
    var block1 = new string('@', n) + new string(' ', 3 * n) + new string('@', n);
    var block2 = new string('@', n) + new string(' ', 2 * n) + new string('@', n);
    var block3 = new string('@', 3 * n);

    void Print(string line) {
      for (var i = 0; i < n; i++)
        sb.AppendLine(line);
    }

    Print(block1);
    Print(block2);
    Print(block3);
    Print(block2);
    Print(block1);

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
  string block1 = string(n, '@') + string(3 * n, ' ') + string(n, '@');
  string block2 = string(n, '@') + string(2 * n, ' ') + string(n, '@');
  string block3 = string(3 * n, '@');

  auto print = [&](const string& line) {
    for (int i = 0; i < n; i++)
      cout << line << "\n";
  };

  print(block1);
  print(block2);
  print(block3);
  print(block2);
  print(block1);

  return 0;
}
```
