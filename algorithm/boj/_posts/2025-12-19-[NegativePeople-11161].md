---
layout: single
title: "[백준 11161] Negative People in Da House (C#, C++) - soo:bak"
date: "2025-12-19 22:47:00 +0900"
description: "백준 11161번 C#, C++ 풀이 - 출입 기록을 순서대로 누적하며 최저 인원수를 확인해 초기 인원을 최소로 만드는 문제"
tags:
  - 백준
  - BOJ
  - 11161
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 11161, 백준 11161번, BOJ 11161, NegativePeople, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11161번 - Negative People in Da House](https://www.acmicpc.net/problem/11161)

## 설명
출입 기록이 주어질 때, 진행 중 인원이 음수가 되지 않도록 하는 초기 인원의 최솟값을 구하는 문제입니다.

각 기록은 먼저 들어오는 인원과 나가는 인원으로 구성됩니다.

<br>

## 접근법
초기 0명으로 가정하고 순서대로 누적하며 최솟값을 추적합니다.

최솟값이 음수라면 그만큼의 초기 인원이 필요하고, 아니면 0명으로 충분합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);

    for (var tc = 0; tc < t; tc++) {
      var m = int.Parse(Console.ReadLine()!);

      var cur = 0;
      var minCur = 0;
      for (var i = 0; i < m; i++) {
        var p = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
        cur += p[0];
        cur -= p[1];
        if (cur < minCur) minCur = cur;
      }

      var need = Math.Max(0, -minCur);
      Console.WriteLine(need);
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

  int t; cin >> t;

  while (t--) {
    int m; cin >> m;

    int cur = 0, minCur = 0;
    for (int i = 0; i < m; i++) {
      int in, out; cin >> in >> out;
      cur += in;
      cur -= out;
      if (cur < minCur) minCur = cur;
    }

    int need = max(0, -minCur);
    cout << need << "\n";
  }

  return 0;
}
```
