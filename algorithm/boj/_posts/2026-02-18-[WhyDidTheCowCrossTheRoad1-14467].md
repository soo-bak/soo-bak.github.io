---
layout: single
title: "[백준 14467] 소가 길을 건너간 이유 1 (C#, C++) - soo:bak"
date: "2026-02-18 00:00:00 +0900"
description: "백준 14467번 C#, C++ 풀이 - 같은 소의 관찰 위치가 바뀐 횟수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 14467
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 14467, 백준 14467번, BOJ 14467, 소가 길을 건너간 이유 1, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14467번 - 소가 길을 건너간 이유 1](https://www.acmicpc.net/problem/14467)

## 설명
소 번호와 위치(0 또는 1)가 순서대로 관찰될 때, 같은 소의 위치가 이전 관찰과 달라진 횟수의 합을 구하는 문제입니다.

<br>

## 접근법
소 번호가 1~10으로 고정되어 있으므로, 각 소의 마지막 위치를 배열로 관리합니다.

어떤 소가 처음 등장하면 현재 위치만 기록하고, 같은 소가 다시 등장했을 때 이전 위치와 다르면 길을 한 번 건넌 것으로 세면 됩니다.

이후, 다음 관찰과 비교할 수 있도록 마지막 위치를 갱신합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var last = new int[11];
    for (int i = 1; i <= 10; i++)
      last[i] = -1;

    var answer = 0;
    for (int i = 0; i < n; i++) {
      var p = Console.ReadLine()!.Split();
      var id = int.Parse(p[0]);
      var side = int.Parse(p[1]);

      if (last[id] == -1) {
        last[id] = side;
      } else {
        if (last[id] != side)
          answer++;
        last[id] = side;
      }
    }

    Console.WriteLine(answer);
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
  int last[11];
  for (int i = 1; i <= 10; i++)
    last[i] = -1;

  int answer = 0;
  for (int i = 0; i < n; i++) {
    int id, side;
    cin >> id >> side;

    if (last[id] == -1) {
      last[id] = side;
    } else {
      if (last[id] != side)
        answer++;
      last[id] = side;
    }
  }

  cout << answer << "\n";

  return 0;
}
```
