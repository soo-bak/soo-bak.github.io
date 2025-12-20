---
layout: single
title: "[백준 13363] Jumbled Compass (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 나침반 바늘을 현재 각도에서 목표 각도로 최단 회전시키는 방향과 크기를 구하는 문제
---

## 문제 링크
[13363번 - Jumbled Compass](https://www.acmicpc.net/problem/13363)

## 설명
현재 각도에서 목표 각도로 나침반 바늘을 돌릴 때, 최단 회전 각도를 구하는 문제입니다. 시계 방향은 양수, 반시계 방향은 음수로 출력하며, 180도 차이일 때는 시계 방향을 선택합니다.

<br>

## 접근법
시계 방향으로 돌렸을 때의 각도 차이를 먼저 계산합니다. 목표에서 현재를 뺀 뒤 360을 더하고 360으로 나눈 나머지를 구하면 항상 0 이상 360 미만의 시계 방향 회전량이 됩니다.

이 값이 180이면 180을 출력하고, 180보다 작으면 시계 방향이 더 짧으므로 그대로 출력합니다. 180보다 크면 반시계 방향이 더 짧으므로 360을 빼서 음수로 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n1 = int.Parse(Console.ReadLine()!);
    var n2 = int.Parse(Console.ReadLine()!);

    var cw = (n2 - n1 + 360) % 360;
    var ans = 0;
    if (cw == 180) ans = 180;
    else if (cw < 180) ans = cw;
    else ans = cw - 360;

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

  int n1, n2; cin >> n1 >> n2;

  int cw = (n2 - n1 + 360) % 360;
  int ans;
  if (cw == 180) ans = 180;
  else if (cw < 180) ans = cw;
  else ans = cw - 360;

  cout << ans << "\n";

  return 0;
}
```
