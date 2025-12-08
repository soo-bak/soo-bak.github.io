---
layout: single
title: "[백준 2875] 대회 or 인턴 (C#, C++) - soo:bak"
date: "2025-12-08 03:15:00 +0900"
description: 여2 남1 팀 구성과 인턴 K명을 고려해 최대 팀 수를 구하는 백준 2875번 대회 or 인턴 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[2875번 - 대회 or 인턴](https://www.acmicpc.net/problem/2875)

## 설명
여학생 2명과 남학생 1명으로 한 팀을 구성할 때, 인턴으로 빠져야 하는 인원을 고려하여 만들 수 있는 팀의 최대 개수를 구하는 문제입니다.

<br>

## 접근법
먼저 인턴을 고려하지 않고 만들 수 있는 최대 팀 수를 구합니다. 여학생 수를 2로 나눈 값과 남학생 수 중 작은 값이 됩니다.

이때 팀에 참여하는 인원은 팀 수의 3배이고, 남는 인원은 전체 인원에서 이를 뺀 값입니다. 남는 인원이 인턴 수 이상이면 팀을 줄일 필요가 없습니다.

남는 인원이 인턴 수보다 적으면 부족한 만큼 팀에서 인원을 빼야 합니다. 팀 하나를 줄이면 3명이 빠지므로, 부족한 인원을 3으로 나눈 값만큼 팀을 줄입니다. 나머지가 있으면 팀을 하나 더 줄여야 합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var m = int.Parse(parts[1]);
    var k = int.Parse(parts[2]);

    var teams = Math.Min(n / 2, m);
    var leftover = n + m - 3 * teams;
    var need = k - leftover;
    if (need > 0) {
      teams -= (need + 2) / 3;
      if (teams < 0) teams = 0;
    }
    Console.WriteLine(teams);
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

  int n, m, k; cin >> n >> m >> k;
  int teams = min(n / 2, m);
  int leftover = n + m - 3 * teams;
  int need = k - leftover;
  if (need > 0) {
    teams -= (need + 2) / 3;
    if (teams < 0) teams = 0;
  }
  cout << teams << "\n";

  return 0;
}
```
