---
layout: single
title: "[백준 23663] Deja vu of Go Players (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 23663번 C#, C++ 풀이 - 선공이 가진 더미 수가 상대 이하인지로 승리 가능 여부를 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 23663
  - C#
  - C++
  - 알고리즘
keywords: "백준 23663, 백준 23663번, BOJ 23663, DejaVuOfGoPlayers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23663번 - Deja vu of Go Players](https://www.acmicpc.net/problem/23663)

## 설명
빨간 플레이어가 먼저 시작할 때, 반드시 이길 수 있는지 판별하는 문제입니다.

<br>

## 접근법
두 플레이어는 자신의 더미에서만 제거하므로 서로 영향을 주지 않습니다. 한 번에 한 더미만 줄일 수 있으므로, 모든 더미를 비우는 데 필요한 턴 수는 더미 개수와 같습니다.

빨간 플레이어의 더미 수가 흰 플레이어 이하이면 먼저 끝낼 수 있으므로 Yes, 아니면 No입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 0; tc < t; tc++) {
      var parts = Console.ReadLine()!.Split();
      var n = int.Parse(parts[0]);
      var m = int.Parse(parts[1]);

      Console.ReadLine();
      Console.ReadLine();

      Console.WriteLine(n <= m ? "Yes" : "No");
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
  for (int tc = 0; tc < t; tc++) {
    int n, m; cin >> n >> m;
    for (int i = 0; i < n; i++) {
      int x; cin >> x;
    }
    for (int i = 0; i < m; i++) {
      int x; cin >> x;
    }

    cout << (n <= m ? "Yes" : "No") << "\n";
  }

  return 0;
}
```
