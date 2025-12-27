---
layout: single
title: "[백준 27880] Gahui and Soongsil University station (C#, C++) - soo:bak"
date: "2025-12-27 15:05:00 +0900"
description: 계단과 에스컬레이터 정보로 역의 깊이를 계산하는 문제
---

## 문제 링크
[27880번 - Gahui and Soongsil University station](https://www.acmicpc.net/problem/27880)

## 설명
출구에서 승강장까지 계단과 에스컬레이터 정보가 주어질 때, 총 깊이를 센티미터 단위로 구하는 문제입니다.

<br>

## 접근법
각 층간 이동 정보를 읽어 계단이면 단 수에 17을 곱하고, 에스컬레이터면 21을 곱해 모두 더합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var d = 0;
    for (var i = 0; i < 4; i++) {
      var parts = Console.ReadLine()!.Split();
      var type = parts[0];
      var steps = int.Parse(parts[1]);

      if (type == "Stair") d += 17 * steps;
      else if (type == "Es") d += 21 * steps;
    }
    Console.WriteLine(d);
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

  int d = 0;
  for (int i = 0; i < 4; i++) {
    string type; int steps;
    cin >> type >> steps;

    if (type == "Stair") d += 17 * steps;
    else if (type == "Es") d += 21 * steps;
  }

  cout << d << "\n";

  return 0;
}
```

