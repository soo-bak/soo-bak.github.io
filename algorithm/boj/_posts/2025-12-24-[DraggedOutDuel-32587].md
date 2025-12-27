---
layout: single
title: "[백준 32587] Dragged-out Duel (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32587번 C#, C++ 풀이 - 가위바위보 결과를 라운드별로 비교해 승패를 결정하는 문제"
tags:
  - 백준
  - BOJ
  - 32587
  - C#
  - C++
  - 알고리즘
keywords: "백준 32587, 백준 32587번, BOJ 32587, DraggedOutDuel, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32587번 - Dragged-out Duel](https://www.acmicpc.net/problem/32587)

## 설명
두 사람이 낸 가위바위보 결과를 순서대로 비교해 승리 횟수가 더 많은 쪽을 출력하는 문제입니다.

<br>

## 접근법
각 라운드를 순회하며 같은 손이면 건너뛰고, 바위는 가위를, 가위는 보를, 보는 바위를 이기는 규칙으로 승패를 판정합니다.

이후 승리 횟수를 비교해 더 많이 이긴 쪽의 결과를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var me = Console.ReadLine()!;
    var guile = Console.ReadLine()!;

    var winMe = 0;
    var winGuile = 0;
    for (var i = 0; i < n; i++) {
      var a = me[i];
      var b = guile[i];
      if (a == b) continue;
      var win = (a == 'R' && b == 'S') ||
                (a == 'S' && b == 'P') ||
                (a == 'P' && b == 'R');
      if (win) winMe++;
      else winGuile++;
    }

    Console.WriteLine(winMe > winGuile ? "victory" : "defeat");
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
  string me, guile; cin >> me >> guile;

  int winMe = 0;
  int winGuile = 0;
  for (int i = 0; i < n; i++) {
    char a = me[i];
    char b = guile[i];
    if (a == b) continue;
    bool win = (a == 'R' && b == 'S') ||
               (a == 'S' && b == 'P') ||
               (a == 'P' && b == 'R');
    if (win) winMe++;
    else winGuile++;
  }

  cout << (winMe > winGuile ? "victory" : "defeat") << "\n";

  return 0;
}
```
