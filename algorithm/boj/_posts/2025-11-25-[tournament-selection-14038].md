---
layout: single
title: "[백준 14038] Tournament Selection (C#, C++) - soo:bak"
date: "2025-11-25 00:15:00 +0900"
description: 6경기 결과에서 승리 수를 세어 그룹을 결정하는 단순 분기 문제인 백준 14038번 Tournament Selection의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 14038
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 14038, 백준 14038번, BOJ 14038, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14038번 - Tournament Selection](https://www.acmicpc.net/problem/14038)

## 설명

토너먼트에서 6경기를 치른 결과가 주어집니다.

각 경기의 승패 결과가 주어질 때, 승리 횟수에 따라 소속 그룹을 결정하는 문제입니다.

승리가 5개 이상이면 그룹 1, 3개 이상이면 그룹 2, 1개 이상이면 그룹 3이고, 승리가 없으면 -1을 출력합니다.

<br>

## 접근법

6개의 경기 결과를 하나씩 읽으면서 승리 횟수를 셉니다.

예를 들어, W, L, W, W, L, W가 주어지면 승리는 4번이므로 그룹 2에 속합니다.

<br>
모든 경기 결과를 확인한 후, 승리 횟수에 따라 그룹을 결정합니다.

승리가 5개 이상이면 1, 3개 이상이면 2, 1개 이상이면 3, 없으면 -1을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var wins = 0;

      for (var i = 0; i < 6; i++) {
        var r = Console.ReadLine()![0];
        if (r == 'W') wins++;
      }

      if (wins >= 5) Console.WriteLine(1);
      else if (wins >= 3) Console.WriteLine(2);
      else if (wins >= 1) Console.WriteLine(3);
      else Console.WriteLine(-1);
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

  int wins = 0;

  for (int i = 0; i < 6; i++) {
    char r; cin >> r;
    if (r == 'W') ++wins;
  }

  if (wins >= 5) cout << 1 << "\n";
  else if (wins >= 3) cout << 2 << "\n";
  else if (wins >= 1) cout << 3 << "\n";
  else cout << -1 << "\n";

  return 0;
}
```

