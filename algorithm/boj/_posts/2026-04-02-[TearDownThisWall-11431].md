---
layout: single
title: "[백준 11431] Mr. Gorbachev, Tear Down This Wall! (C#, C++) - soo:bak"
date: "2026-04-02 22:30:00 +0900"
description: "백준 11431번 C#, C++ 풀이 - 벽의 전체 길이를 구한 뒤 사람 수로 나눈 작업 시간을 올림하는 문제"
tags:
  - 백준
  - BOJ
  - 11431
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 11431, 백준 11431번, BOJ 11431, Mr. Gorbachev Tear Down This Wall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11431번 - Mr. Gorbachev, Tear Down This Wall!](https://www.acmicpc.net/problem/11431)

## 설명
여러 점으로 표현된 벽이 주어질 때, 벽 전체 길이를 구한 뒤 주어진 인원으로 철거하는 데 걸리는 시간을 구하는 문제입니다.

<br>

## 접근법
벽은 가로 또는 세로 선분으로만 이루어져 있으므로, 연속한 두 점 사이의 길이는 `|x1 - x2| + |y1 - y2|`로 구할 수 있습니다.

모든 선분 길이를 더하면 벽 전체 길이가 됩니다. 여기에 한 사람이 1미터를 철거하는 데 걸리는 시간 `s`를 곱하면 전체 작업량이 나오고, 이를 사람 수 `p`로 나눈 값을 올림하면 필요한 시간이 됩니다.

출력은 데이터셋 번호와 정답 사이에 빈 줄까지 포함해 문제 형식에 맞춰 그대로 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine()!);

    for (int tc = 1; tc <= t; tc++) {
      string[] first = Console.ReadLine()!.Split();
      int n = int.Parse(first[0]);
      int s = int.Parse(first[1]);
      int p = int.Parse(first[2]);

      string[] point = Console.ReadLine()!.Split();
      int prevX = int.Parse(point[0]);
      int prevY = int.Parse(point[1]);

      long length = 0;

      for (int i = 0; i < n; i++) {
        point = Console.ReadLine()!.Split();
        int x = int.Parse(point[0]);
        int y = int.Parse(point[1]);

        length += Math.Abs(x - prevX) + Math.Abs(y - prevY);
        prevX = x;
        prevY = y;
      }

      long totalWork = length * s;
      long answer = (totalWork + p - 1) / p;

      Console.WriteLine($"Data Set {tc}:");
      Console.WriteLine(answer);
      Console.WriteLine();
    }
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

  int t;
  cin >> t;

  for (int tc = 1; tc <= t; tc++) {
    int n, s, p;
    cin >> n >> s >> p;

    int prevX, prevY;
    cin >> prevX >> prevY;

    long long length = 0;

    for (int i = 0; i < n; i++) {
      int x, y;
      cin >> x >> y;

      length += abs(x - prevX) + abs(y - prevY);
      prevX = x;
      prevY = y;
    }

    long long totalWork = length * s;
    long long answer = (totalWork + p - 1) / p;

    cout << "Data Set " << tc << ":\n";
    cout << answer << "\n\n";
  }

  return 0;
}
```
