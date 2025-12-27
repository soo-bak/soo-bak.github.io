---
layout: single
title: "[백준 24736] Football Scoring (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: 각 팀의 터치다운·필드골·세이프티·PAT·2점 전환 개수를 받아 미식축구 점수를 계산하는 백준 24736번 Football Scoring 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 24736
  - C#
  - C++
  - 알고리즘
keywords: "백준 24736, 백준 24736번, BOJ 24736, FootballScoring, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24736번 - Football Scoring](https://www.acmicpc.net/problem/24736)

## 설명
두 팀의 미식축구 득점 항목이 주어질 때, 각 팀의 총점을 계산하는 문제입니다.

<br>

## 접근법
터치다운은 6점, 필드골은 3점, 세이프티와 2점 전환은 각각 2점, PAT은 1점입니다.

각 항목의 개수에 점수를 곱해서 더하면 총점이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Score(int t, int f, int s, int p, int c) => 6 * t + 3 * f + 2 * s + p + 2 * c;

  static void Main() {
    for (var i = 0; i < 2; i++) {
      var line = Console.ReadLine()!.Split();
      var t = int.Parse(line[0]);
      var f = int.Parse(line[1]);
      var s = int.Parse(line[2]);
      var p = int.Parse(line[3]);
      var c = int.Parse(line[4]);
      Console.Write(Score(t, f, s, p, c));
      Console.Write(i == 0 ? " " : "\n");
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

  auto score = [](int t, int f, int s, int p, int c) {
    return 6 * t + 3 * f + 2 * s + p + 2 * c;
  };

  for (int i = 0; i < 2; i++) {
    int t, f, s, p, c; cin >> t >> f >> s >> p >> c;
    cout << score(t, f, s, p, c);
    cout << (i == 0 ? ' ' : '\n');
  }

  return 0;
}
```
