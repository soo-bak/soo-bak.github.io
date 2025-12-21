---
layout: single
title: "[백준 29918] Leiutaja number üks (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 10주 뒤 최대 경쟁자보다 1개 더 많기 위해 필요한 추가 개수를 계산하는 문제
---

## 문제 링크
[29918번 - Leiutaja number üks](https://www.acmicpc.net/problem/29918)

## 설명
10주 뒤 발명품 수가 가장 많아지기 위해 Adalbert가 추가로 주문해야 할 최소 개수를 구하는 문제입니다.

<br>

## 접근법
먼저 각 발명가의 10주 후 발명품 수를 현재 개수에 주당 증가량의 10배를 더해 계산합니다.

이후 경쟁자 5명 중 최댓값을 구하고, 그 값보다 1개 더 많아지기 위해 필요한 추가 개수를 계산합니다. 이미 더 많다면 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n0 = int.Parse(first[0]);
    var m0 = int.Parse(first[1]);

    var mine = n0 + 10 * m0;
    var best = 0;
    for (var i = 0; i < 5; i++) {
      var parts = Console.ReadLine()!.Split();
      var n = int.Parse(parts[0]);
      var m = int.Parse(parts[1]);
      var total = n + 10 * m;
      if (total > best) best = total;
    }

    var need = best + 1 - mine;
    if (need < 0) need = 0;
    Console.WriteLine(need);
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

  int n0, m0; cin >> n0 >> m0;
  int mine = n0 + 10 * m0;
  int best = 0;

  for (int i = 0; i < 5; i++) {
    int n, m; cin >> n >> m;
    int total = n + 10 * m;
    if (total > best) best = total;
  }

  int need = best + 1 - mine;
  if (need < 0) need = 0;
  cout << need << "\n";

  return 0;
}
```
