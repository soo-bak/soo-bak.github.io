---
layout: single
title: "[백준 5367] Target Practice (C#, C++) - soo:bak"
date: "2026-04-14 16:30:00 +0900"
description: "백준 5367번 C#, C++ 풀이 - 테두리와 대각선 위치에 맞춰 표적 모양을 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 5367
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 5367, 백준 5367번, BOJ 5367, Target Practice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5367번 - Target Practice](https://www.acmicpc.net/problem/5367)

## 설명
크기가 주어졌을 때, 바깥은 사각형이고 안쪽에는 X 모양이 있는 표적을 출력하는 문제입니다.

<br>

## 접근법
첫 줄과 마지막 줄은 양 끝이 `|`이고 가운데가 `-`로 채워진 형태입니다.

가운데 줄들은 양 끝을 `|`로 두고, 내부에서 두 대각선 위치에만 `*`를 놓으면 됩니다. 즉 `i`번째 줄에서는 왼쪽에서 `i`번째와 오른쪽에서 `i`번째 위치에 `*`를 찍고, 나머지는 공백으로 채웁니다.

이 규칙대로 위에서부터 아래까지 한 줄씩 출력하면 원하는 모양이 만들어집니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    sb.Append('|').Append(new string('-', n - 2)).AppendLine("|");

    for (int i = 1; i <= n - 2; i++) {
      char[] line = new string(' ', n).ToCharArray();
      line[0] = '|';
      line[n - 1] = '|';
      line[i] = '*';
      line[n - 1 - i] = '*';
      sb.AppendLine(new string(line));
    }

    sb.Append('|').Append(new string('-', n - 2)).AppendLine("|");

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
  cin >> n;

  cout << "|" << string(n - 2, '-') << "|\n";

  for (int i = 1; i <= n - 2; i++) {
    string line(n, ' ');
    line[0] = '|';
    line[n - 1] = '|';
    line[i] = '*';
    line[n - 1 - i] = '*';
    cout << line << "\n";
  }

  cout << "|" << string(n - 2, '-') << "|\n";

  return 0;
}
```
