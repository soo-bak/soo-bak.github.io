---
layout: single
title: "[백준 14803] Steed 2: Cruise Control (Small) (C#, C++) - soo:bak"
date: "2026-01-22 16:33:00 +0900"
description: "백준 14803번 C#, C++ 풀이 - 다른 말들을 추월하지 않으면서 목적지에 도달할 수 있는 최대 일정 속도를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 14803
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 14803, 백준 14803번, BOJ 14803, Steed 2: Cruise Control, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14803번 - Steed 2: Cruise Control (Small)](https://www.acmicpc.net/problem/14803)

## 설명
다른 말들을 추월하지 않으면서 목적지에 도달할 수 있는 최대 일정 속도를 구하는 문제입니다.

다른 말들은 앞지르지 못하므로, 가장 늦게 도착하는 말보다 빨리 갈 수 없습니다. 따라서 도착까지 걸리는 시간이 가장 큰 말을 찾으면, Annie의 최대 속도는 목적지 거리를 그 시간으로 나눈 값입니다.

<br>

## 접근법
먼저 각 말에 대해 목적지까지 남은 거리와 속도를 이용해 도착 시간을 계산합니다.

다음으로 모든 말의 도착 시간 중 최댓값을 찾습니다. Annie의 최대 속도는 목적지 거리를 이 최댓값으로 나눈 값입니다.

시간 복잡도는 O(N)입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;
using System.Globalization;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    for (var tc = 1; tc <= t; tc++) {
      var first = Console.ReadLine()!.Split();
      var d = double.Parse(first[0]);
      var n = int.Parse(first[1]);

      var maxTime = 0.0;
      for (var i = 0; i < n; i++) {
        var parts = Console.ReadLine()!.Split();
        var k = double.Parse(parts[0]);
        var s = double.Parse(parts[1]);
        var time = (d - k) / s;
        if (time > maxTime)
          maxTime = time;
      }

      var speed = d / maxTime;
      sb.Append("Case #").Append(tc).Append(": ")
        .Append(speed.ToString("F6", CultureInfo.InvariantCulture))
        .Append('\n');
    }
    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  cout << fixed << setprecision(6);
  for (int tc = 1; tc <= t; tc++) {
    double d;
    int n;
    cin >> d >> n;
    double maxTime = 0.0;
    for (int i = 0; i < n; i++) {
      double k, s;
      cin >> k >> s;
      double time = (d - k) / s;
      if (time > maxTime)
        maxTime = time;
    }
    double speed = d / maxTime;
    cout << "Case #" << tc << ": " << speed << "\n";
  }

  return 0;
}
```
