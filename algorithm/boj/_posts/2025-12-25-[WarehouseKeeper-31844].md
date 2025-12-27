---
layout: single
title: "[백준 31844] 창고지기 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 로봇, 박스, 목표의 위치 관계를 이용하여 최소 이동 횟수를 구하는 백준 31844번 창고지기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 31844
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 31844, 백준 31844번, BOJ 31844, WarehouseKeeper, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31844번 - 창고지기](https://www.acmicpc.net/problem/31844)

## 설명
길이 10의 일렬 창고에서 로봇과 박스의 위치가 주어질 때, 박스를 목표 칸으로 옮기기 위한 최소 명령 횟수를 구하는 문제입니다.

<br>

## 접근법
먼저, 로봇이 박스를 밀어서 목표까지 보내려면 로봇, 박스, 목표가 일직선상에 순서대로 있어야 합니다.

로봇이 박스보다 왼쪽에 있고 목표가 박스보다 오른쪽에 있으면 오른쪽으로 밀어서 도달할 수 있습니다. 반대의 경우도 마찬가지입니다.

이 경우 최소 이동 횟수는 로봇에서 목표까지의 거리에서 1을 뺀 값입니다. 박스가 중간에 있어 한 칸을 차지하기 때문입니다.

이후, 위 조건을 만족하지 않으면 박스를 목표까지 옮길 수 없으므로 -1을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;

    var st = 0;
    var fin = 0;
    var box = 0;
    for (var i = 0; i < 10; i++) {
      if (s[i] == '@') st = i;
      else if (s[i] == '#') box = i;
      else if (s[i] == '!') fin = i;
    }

    if (st < box && box < fin) Console.WriteLine(fin - st - 1);
    else if (fin < box && box < st) Console.WriteLine(st - fin - 1);
    else Console.WriteLine(-1);
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

  string s; cin >> s;

  int st = 0, fin = 0, box = 0;
  for (int i = 0; i < 10; i++) {
    if (s[i] == '@') st = i;
    else if (s[i] == '#') box = i;
    else if (s[i] == '!') fin = i;
  }

  if (st < box && box < fin) cout << fin - st - 1;
  else if (fin < box && box < st) cout << st - fin - 1;
  else cout << -1;
  cout << "\n";

  return 0;
}
```
