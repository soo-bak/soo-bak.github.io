---
layout: single
title: "[백준 14683] Exactly Electrical (C#, C++) - soo:bak"
date: "2025-12-06 20:15:00 +0900"
description: 맨해튼 거리와 배터리 잔량으로 정확히 도착 가능 여부를 판별하는 백준 14683번 Exactly Electrical 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[14683번 - Exactly Electrical](https://www.acmicpc.net/problem/14683)

## 설명
격자 도시에서 시작 좌표에서 도착 좌표까지 이동합니다. 인접 교차로로 한 칸 이동할 때마다 배터리 1을 소모하며, 방향 전환은 자유롭습니다.

배터리 잔량이 정확히 0이 되는 상태로 도착할 수 있으면 Y, 불가능하면 N을 출력하는 문제입니다.

<br>

## 접근법
먼저, 최단 이동 거리는 두 좌표 사이의 맨해튼 거리입니다.

다음으로, 배터리가 이 거리보다 적으면 도달할 수 없습니다. 또한 남는 배터리를 소모하려면 왕복 이동이 필요하므로, 배터리에서 거리를 뺀 값이 짝수여야 합니다.

이후, 두 조건을 모두 만족하면 Y, 아니면 N을 출력합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var start = Console.ReadLine()!.Split();
      var dest = Console.ReadLine()!.Split();
      var a = int.Parse(start[0]);
      var b = int.Parse(start[1]);
      var c = int.Parse(dest[0]);
      var d = int.Parse(dest[1]);
      var t = int.Parse(Console.ReadLine()!);

      var dist = Math.Abs(a - c) + Math.Abs(b - d);
      var ok = t >= dist && (t - dist) % 2 == 0;
      Console.WriteLine(ok ? "Y" : "N");
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

  int a, b, c, d, t; cin >> a >> b >> c >> d >> t;

  int dist = abs(a - c) + abs(b - d);
  bool ok = t >= dist && (t - dist) % 2 == 0;
  cout << (ok ? "Y" : "N") << "\n";

  return 0;
}
```
