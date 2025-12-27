---
layout: single
title: "[백준 6060] Wheel Rotation (C#, C++) - soo:bak"
date: "2025-12-26 01:19:48 +0900"
description: "백준 6060번 C#, C++ 풀이 - 벨트 연결 정보를 따라 마지막 풀리의 회전 방향을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 6060
  - C#
  - C++
  - 알고리즘
keywords: "백준 6060, 백준 6060번, BOJ 6060, WheelRotation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6060번 - Wheel Rotation](https://www.acmicpc.net/problem/6060)

## 설명
벨트 연결이 주어질 때 1번 풀리로부터 N번 풀리의 회전 방향을 구하는 문제입니다.

<br>

## 접근법
먼저 각 풀리에서 다음 풀리로 이어지는 벨트를 기록합니다.

다음으로 1번 풀리에서 시작해 연결을 따라가며 방향을 갱신합니다.

이후 직선 연결이면 같은 방향, 교차 연결이면 방향을 반전합니다.

마지막으로 N번 풀리의 방향을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var next = new int[n + 1];
    var type = new int[n + 1];

    for (var i = 0; i < n - 1; i++) {
      var parts = Console.ReadLine()!.Split();
      var s = int.Parse(parts[0]);
      var d = int.Parse(parts[1]);
      var c = int.Parse(parts[2]);
      next[s] = d;
      type[s] = c;
    }

    var dir = 0;
    var cur = 1;
    while (cur != n) {
      if (type[cur] == 1) dir ^= 1;
      cur = next[cur];
    }

    Console.WriteLine(dir);
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
  vi next(n + 1, 0);
  vi type(n + 1, 0);

  for (int i = 0; i < n - 1; i++) {
    int s, d, c; cin >> s >> d >> c;
    next[s] = d;
    type[s] = c;
  }

  int dir = 0;
  int cur = 1;
  while (cur != n) {
    if (type[cur] == 1) dir ^= 1;
    cur = next[cur];
  }

  cout << dir << "\n";
  return 0;
}
```
