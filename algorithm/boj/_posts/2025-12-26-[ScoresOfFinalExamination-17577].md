---
layout: single
title: "[백준 17577] Scores of Final Examination (C#, C++) - soo:bak"
date: "2025-12-26 03:08:00 +0900"
description: "백준 17577번 C#, C++ 풀이 - 학생별 총점을 계산해 최대값을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 17577
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 17577, 백준 17577번, BOJ 17577, ScoresOfFinalExamination, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17577번 - Scores of Final Examination](https://www.acmicpc.net/problem/17577)

## 설명
과목별 점수가 주어질 때 학생별 총점 중 최댓값을 구하는 문제입니다.

<br>

## 접근법
먼저 학생 수만큼 합계를 저장할 배열을 준비합니다.

다음으로 과목별 점수를 읽으며 학생별 합계를 누적합니다.

마지막으로 합계 배열에서 최댓값을 찾아 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var sb = new StringBuilder();

    while (true) {
      var n = int.Parse(parts[idx++]);
      var m = int.Parse(parts[idx++]);
      if (n == 0 && m == 0) break;

      var sum = new int[n];
      for (var i = 0; i < m; i++) {
        for (var j = 0; j < n; j++)
          sum[j] += int.Parse(parts[idx++]);
      }

      var best = 0;
      for (var i = 0; i < n; i++)
        if (sum[i] > best) best = sum[i];

      sb.AppendLine(best.ToString());
    }

    Console.Write(sb);
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

  while (true) {
    int n, m; cin >> n >> m;
    if (n == 0 && m == 0) break;

    vi sum(n, 0);
    for (int i = 0; i < m; i++) {
      for (int j = 0; j < n; j++) {
        int v; cin >> v;
        sum[j] += v;
      }
    }

    int best = 0;
    for (int i = 0; i < n; i++) {
      if (sum[i] > best) best = sum[i];
    }

    cout << best << "\n";
  }

  return 0;
}
```
