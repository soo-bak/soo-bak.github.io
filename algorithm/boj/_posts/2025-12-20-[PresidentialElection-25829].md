---
layout: single
title: "[백준 25829] Presidential Election (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 25829번 C#, C++ 풀이 - 주별 득표로 전체 득표와 선거인단 승자를 판정해 동일 승자인 경우를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 25829
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 25829, 백준 25829번, BOJ 25829, PresidentialElection, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25829번 - Presidential Election](https://www.acmicpc.net/problem/25829)

## 설명
각 주의 선거인단 수와 두 후보의 득표수가 주어질 때, 전체 득표수 승자와 선거인단 승자가 같은 후보인지 판정하는 문제입니다. 주에서 더 많이 득표한 후보가 그 주의 선거인단을 모두 가져가며, 두 기준 모두에서 승자가 같으면 해당 후보 번호를, 아니면 0을 출력합니다.

<br>

## 접근법
각 주를 순회하면서 두 후보의 총 득표수를 누적하고, 해당 주에서 더 많은 표를 얻은 후보에게 선거인단을 더합니다. 동률일 때는 후보 2에게 선거인단이 간다고 문제에서 정의합니다.

모든 주를 처리한 후 득표수 기준 승자와 선거인단 기준 승자를 각각 구합니다. 두 승자가 같은 후보면 그 번호를, 다르거나 어느 쪽이든 동률이면 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var votes1 = 0;
    var votes2 = 0;
    var elec1 = 0;
    var elec2 = 0;

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var e = int.Parse(parts[0]);
      var v1 = int.Parse(parts[1]);
      var v2 = int.Parse(parts[2]);

      votes1 += v1;
      votes2 += v2;

      if (v1 > v2) elec1 += e;
      else elec2 += e;
    }

    var maj = votes1 == votes2 ? 0 : (votes1 > votes2 ? 1 : 2);
    var elec = elec1 == elec2 ? 0 : (elec1 > elec2 ? 1 : 2);

    var ans = (maj == 1 && elec == 1) ? 1
            : (maj == 2 && elec == 2) ? 2
            : 0;

    Console.WriteLine(ans);
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

  int n; cin >> n;

  int votes1 = 0, votes2 = 0;
  int elec1 = 0, elec2 = 0;

  for (int i = 0; i < n; i++) {
    int e, v1, v2; cin >> e >> v1 >> v2;
    votes1 += v1;
    votes2 += v2;
    if (v1 > v2) elec1 += e;
    else elec2 += e;
  }

  int maj = (votes1 == votes2) ? 0 : (votes1 > votes2 ? 1 : 2);
  int elec = (elec1 == elec2) ? 0 : (elec1 > elec2 ? 1 : 2);

  int ans = (maj == 1 && elec == 1) ? 1 : (maj == 2 && elec == 2 ? 2 : 0);
  cout << ans << "\n";

  return 0;
}
```
