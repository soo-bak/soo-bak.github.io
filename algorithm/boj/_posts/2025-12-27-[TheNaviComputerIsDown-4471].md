---
layout: single
title: "[백준 4471] The Navi-Computer is Down! (C#, C++) - soo:bak"
date: "2025-12-27 09:45:00 +0900"
description: "백준 4471번 C#, C++ 풀이 - 두 성계의 3차원 좌표로 거리를 구해 포맷에 맞춰 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 4471
  - C#
  - C++
  - 알고리즘
  - 수학
  - 문자열
  - 기하학
  - geometry_3d
keywords: "백준 4471, 백준 4471번, BOJ 4471, TheNaviComputerIsDown, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4471번 - The Navi-Computer is Down!](https://www.acmicpc.net/problem/4471)

## 설명
두 성계의 이름과 3차원 좌표가 주어질 때, 두 점 사이의 거리를 구하는 문제입니다. 소수 둘째 자리까지 출력합니다.

<br>

## 접근법
두 좌표 사이의 유클리드 거리를 계산합니다. 성계 이름에 공백이 포함될 수 있으므로 줄 단위로 읽습니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Globalization;

class Program {
  static void Main() {
    var nLine = Console.ReadLine();
    if (nLine == null) return;
    var t = int.Parse(nLine);

    for (var cs = 0; cs < t; cs++) {
      var name1 = Console.ReadLine()!;
      var coord1 = Console.ReadLine()!.Split();
      var x1 = double.Parse(coord1[0], CultureInfo.InvariantCulture);
      var y1 = double.Parse(coord1[1], CultureInfo.InvariantCulture);
      var z1 = double.Parse(coord1[2], CultureInfo.InvariantCulture);

      var name2 = Console.ReadLine()!;
      var coord2 = Console.ReadLine()!.Split();
      var x2 = double.Parse(coord2[0], CultureInfo.InvariantCulture);
      var y2 = double.Parse(coord2[1], CultureInfo.InvariantCulture);
      var z2 = double.Parse(coord2[2], CultureInfo.InvariantCulture);

      var dx = x2 - x1;
      var dy = y2 - y1;
      var dz = z2 - z1;
      var dist = Math.Sqrt(dx * dx + dy * dy + dz * dz);

      Console.WriteLine($"{name1} to {name2}: {dist:F2}");
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
  string dummy;
  getline(cin, dummy);

  for (int cs = 0; cs < t; cs++) {
    string name1, name2;
    
    getline(cin, name1);
    double x1, y1, z1; cin >> x1 >> y1 >> z1;
    getline(cin, dummy);

    getline(cin, name2);
    double x2, y2, z2; cin >> x2 >> y2 >> z2;
    getline(cin, dummy);

    double dx = x2 - x1;
    double dy = y2 - y1;
    double dz = z2 - z1;
    double dist = sqrt(dx * dx + dy * dy + dz * dz);

    cout << fixed << setprecision(2);
    cout << name1 << " to " << name2 << ": " << dist << "\n";
  }

  return 0;
}
```
