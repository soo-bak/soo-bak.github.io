---
layout: single
title: "[백준 29991] Fatigue-Fighting Vacation (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 29991번 C#, C++ 풀이 - 피로도 조건에 따라 활동을 순서대로 수행하며 가능한 총 개수를 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 29991
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 29991, 백준 29991번, BOJ 29991, FatigueFightingVacation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29991번 - Fatigue-Fighting Vacation](https://www.acmicpc.net/problem/29991)

## 설명
피로도가 충분하면 피로 활동을, 아니면 회복 활동을 수행하는 규칙에 따라 가능한 활동 수를 계산하는 문제입니다.

<br>

## 접근법
피로 활동과 회복 활동은 각각 순서가 고정되어 있으므로 두 인덱스를 관리하며 시뮬레이션합니다.

이후 피로도가 부족한 순간에 회복 활동이 남아 있지 않으면 종료하고, 수행한 활동 수를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var data = Console.In.ReadToEnd();
    var parts = data.Split();
    var idx = 0;

    var d = int.Parse(parts[idx++]);
    var c = int.Parse(parts[idx++]);
    var r = int.Parse(parts[idx++]);

    var tired = new int[c];
    var rest = new int[r];
    for (var i = 0; i < c; i++) tired[i] = int.Parse(parts[idx++]);
    for (var i = 0; i < r; i++) rest[i] = int.Parse(parts[idx++]);

    var iT = 0;
    var iR = 0;
    var done = 0;

    while (true) {
      if (iT < c && d >= tired[iT]) {
        d -= tired[iT++];
        done++;
      } else if (iR < r) {
        d += rest[iR++];
        done++;
      } else break;
    }

    Console.WriteLine(done);
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

  int d, c, r; cin >> d >> c >> r;
  vector<int> tired(c), rest(r);
  for (int i = 0; i < c; i++)
    cin >> tired[i];
  for (int i = 0; i < r; i++)
    cin >> rest[i];

  int iT = 0, iR = 0, done = 0;
  while (true) {
    if (iT < c && d >= tired[iT]) {
      d -= tired[iT++];
      done++;
    } else if (iR < r) {
      d += rest[iR++];
      done++;
    } else break;
  }

  cout << done << "\n";

  return 0;
}
```
