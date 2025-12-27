---
layout: single
title: "[백준 27522] 카트라이더: 드리프트 (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 완주 기록을 정렬해 순위 점수를 합산하고 높은 팀을 출력하는 백준 27522번 카트라이더 드리프트 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 27522
  - C#
  - C++
  - 알고리즘
keywords: "백준 27522, 백준 27522번, BOJ 27522, KartriderDrift, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27522번 - 카트라이더: 드리프트](https://www.acmicpc.net/problem/27522)

## 설명
8명의 완주 기록과 팀 정보가 주어질 때, 순위 점수 합이 더 높은 팀을 출력하는 문제입니다.

순위별 점수는 1등부터 10, 8, 6, 5, 4, 3, 2, 1점입니다.

<br>

## 접근법
먼저 기록을 밀리초 단위 정수로 변환합니다.

이후 기록을 빠른 순으로 정렬하고, 순위에 따라 점수를 팀별로 합산합니다.

합이 더 큰 팀을 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static int Parse(string t) {
    var m = t[0] - '0';
    var s = (t[2] - '0') * 10 + (t[3] - '0');
    var ms = (t[5] - '0') * 100 + (t[6] - '0') * 10 + (t[7] - '0');
    return (m * 60 + s) * 1000 + ms;
  }

  static void Main() {
    var list = new List<(int time, char team)>();
    for (var i = 0; i < 8; i++) {
      var parts = Console.ReadLine()!.Split();
      list.Add((Parse(parts[0]), parts[1][0]));
    }
    list.Sort((a, b) => a.time.CompareTo(b.time));

    var score = new[] {10, 8, 6, 5, 4, 3, 2, 1};
    var r = 0;
    var b = 0;
    for (var i = 0; i < 8; i++) {
      if (list[i].team == 'R') r += score[i];
      else b += score[i];
    }
    Console.WriteLine(r > b ? "Red" : "Blue");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<pair<int, char>> vp;

int parse(const string& t) {
  int m = t[0] - '0';
  int s = (t[2] - '0') * 10 + (t[3] - '0');
  int ms = (t[5] - '0') * 100 + (t[6] - '0') * 10 + (t[7] - '0');
  return (m * 60 + s) * 1000 + ms;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vp v(8);
  for (int i = 0; i < 8; i++) {
    string t; char team;
    cin >> t >> team;
    v[i] = {parse(t), team};
  }
  sort(v.begin(), v.end());

  int score[8] = {10, 8, 6, 5, 4, 3, 2, 1};
  int r = 0, b = 0;
  for (int i = 0; i < 8; i++) {
    if (v[i].second == 'R') r += score[i];
    else b += score[i];
  }
  cout << (r > b ? "Red" : "Blue") << "\n";

  return 0;
}
```
