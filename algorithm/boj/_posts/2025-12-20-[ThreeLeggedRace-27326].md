---
layout: single
title: "[백준 27326] 二人三脚 (Three-Legged Race) (C#, C++) - soo:bak"
date: "2025-12-20 12:12:00 +0900"
description: "백준 27326번 C#, C++ 풀이 - 2N-1명의 소속 팀 정보가 주어질 때 마지막 학생의 팀 번호를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 27326
  - C#
  - C++
  - 알고리즘
keywords: "백준 27326, 백준 27326번, BOJ 27326, ThreeLeggedRace, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27326번 - 二人三脚 (Three-Legged Race)](https://www.acmicpc.net/problem/27326)

## 설명
각 팀에 정확히 두 명씩 속하는 상황에서, 마지막 학생을 제외한 모든 학생의 팀 정보가 주어질 때 마지막 학생의 팀 번호를 찾는 문제입니다.

<br>

## 접근법
각 팀에는 정확히 두 명이 속하므로, 모든 팀 번호는 정확히 2번씩 등장해야 합니다.

마지막 학생의 정보가 빠져있으므로, 주어진 목록에서 1번만 등장하는 팀이 마지막 학생의 팀입니다.

각 팀 번호의 등장 횟수를 세고, 2회 미만인 팀 번호를 찾아 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var freq = new int[n + 1];
    var parts = Console.ReadLine()!.Split();

    for (var i = 0; i < 2 * n - 1; i++) {
      var team = int.Parse(parts[i]);
      freq[team]++;
    }

    for (var t = 1; t <= n; t++) {
      if (freq[t] < 2) {
        Console.WriteLine(t);
        break;
      }
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi freq(n + 1, 0);

  for (int i = 0; i < 2 * n - 1; i++) {
    int team; cin >> team;
    freq[team]++;
  }

  for (int t = 1; t <= n; t++) {
    if (freq[t] < 2) {
      cout << t << "\n";
      break;
    }
  }

  return 0;
}
```
