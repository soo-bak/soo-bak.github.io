---
layout: single
title: "[백준 11340] Making the Grade? (C#, C++) - soo:bak"
date: "2025-12-26 01:12:47 +0900"
description: "백준 11340번 C#, C++ 풀이 - 가중 평균이 90 이상이 되기 위한 최소 기말 점수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 11340
  - C#
  - C++
  - 알고리즘
keywords: "백준 11340, 백준 11340번, BOJ 11340, MakingTheGrade, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11340번 - Making the Grade?](https://www.acmicpc.net/problem/11340)

## 설명
세 과목 점수가 주어질 때 평균 90 이상을 만들기 위한 최소 기말 점수를 구하는 문제입니다.

<br>

## 접근법
먼저 기존 세 점수의 가중 합을 계산합니다.

다음으로 기말 점수에 대한 식을 정리해 필요한 최소 정수를 구합니다.

이후 0~100 범위에 들어오지 않으면 불가능으로 판단합니다.

마지막으로 가능하면 최소 점수를 출력하고, 아니면 impossible을 출력합니다.

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
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var i = 0; i < t; i++) {
      var p = int.Parse(parts[idx++]);
      var t1 = int.Parse(parts[idx++]);
      var m = int.Parse(parts[idx++]);

      var sum = 15 * p + 20 * t1 + 25 * m;
      var need = 9000 - sum;
      var f = (need + 39) / 40;

      if (f < 0) f = 0;
      if (f > 100) sb.AppendLine("impossible");
      else sb.AppendLine(f.ToString());
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
    int p, t1, m; cin >> p >> t1 >> m;

    int sum = 15 * p + 20 * t1 + 25 * m;
    int need = 9000 - sum;
    int f = (need + 39) / 40;

    if (f < 0) f = 0;
    if (f > 100) cout << "impossible\n";
    else cout << f << "\n";
  }

  return 0;
}
```
