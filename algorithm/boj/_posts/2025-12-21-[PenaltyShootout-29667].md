---
layout: single
title: "[백준 29667] Ответный матч (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 29667번 C#, C++ 풀이 - 두 경기의 현재 스코어에서 승부차기(총합 동점+원정골 동점) 가능 여부를 판정하는 문제"
tags:
  - 백준
  - BOJ
  - 29667
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 29667, 백준 29667번, BOJ 29667, PenaltyShootout, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29667번 - Ответный матч](https://www.acmicpc.net/problem/29667)

## 설명
두 경기의 합산 스코어와 원정 골이 모두 동점이 되어 승부차기로 갈 수 있는지 판정하는 문제입니다.

<br>

## 접근법
승부차기로 가려면 두 경기의 총합과 원정 골이 모두 동점이어야 합니다. 1차전 원정 골은 B팀이 넣은 골이고, 2차전 원정 골은 A팀이 넣은 골입니다.

A팀의 원정 골이 부족하면 2차전 남은 시간에 추가로 넣어야 하고, B팀도 마찬가지입니다. 추가로 넣어야 할 골이 음수가 되면 이미 초과한 것이므로 동점을 맞출 수 없습니다. 결국 1차전에서 B팀이 넣은 골이 2차전에서 A팀이 넣은 골 이상이고, 1차전에서 A팀이 넣은 골이 2차전에서 B팀이 넣은 골 이상이면 가능합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s1 = Console.ReadLine()!.Split(':');
    var s2 = Console.ReadLine()!.Split(':');
    var a = int.Parse(s1[0]);
    var b = int.Parse(s1[1]);
    var c = int.Parse(s2[0]);
    var d = int.Parse(s2[1]);

    var ok = b >= d && a >= c;
    Console.WriteLine(ok ? "YES" : "NO");
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

  string s1, s2; cin >> s1 >> s2;

  auto parse = [](const string& s, int &x, int &y) {
    int p = s.find(':');
    x = stoi(s.substr(0, p));
    y = stoi(s.substr(p + 1));
  };

  int a, b, c, d;
  parse(s1, a, b);
  parse(s2, c, d);

  bool ok = b >= d && a >= c;
  cout << (ok ? "YES" : "NO") << "\n";

  return 0;
}
```
