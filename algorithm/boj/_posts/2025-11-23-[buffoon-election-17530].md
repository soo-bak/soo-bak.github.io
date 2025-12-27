---
layout: single
title: "[백준 17530] Buffoon (C#, C++) - soo:bak"
date: "2025-11-23 03:35:00 +0900"
description: 투표 결과에서 첫 번째로 등록한 카를로스가 최다 득표인지 확인해 동점이면 자동 당선이라는 규칙을 구현한 백준 17530번 Buffoon 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 17530
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 17530, 백준 17530번, BOJ 17530, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17530번 - Buffoon](https://www.acmicpc.net/problem/17530)

## 설명

여러 후보의 득표수가 등록 순서대로 주어지고, 첫 번째 후보가 카를로스인 상황에서 카를로스가 당선되는지 판단하는 문제입니다.

최다 득표자가 당선되며, 동점일 경우 먼저 등록한 사람이 당선됩니다.

<br>

## 접근법

첫 번째 득표수가 카를로스의 득표수이므로, 나머지 후보들의 득표수와 비교합니다.

카를로스보다 득표수가 많은 후보가 한 명이라도 있으면 카를로스는 탈락합니다.

<br>
동점인 경우 카를로스가 먼저 등록되었으므로 카를로스가 당선됩니다.

따라서 카를로스보다 **많은** 득표수를 가진 후보가 있는지만 확인하면 됩니다

 모든 후보를 확인한 후 카를로스보다 많은 득표수를 받은 후보가 없다면 `S`, 있다면 `N`을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var carlos = int.Parse(Console.ReadLine()!);

      var win = true;

      for (int i = 1; i < n; i++) {
        var vote = int.Parse(Console.ReadLine()!);
        if (vote > carlos) win = false;
      }

      Console.WriteLine(win ? "S" : "N");
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

  int n; cin >> n;
  int carlos; cin >> carlos;
  bool win = true;

  for (int i = 1; i < n; i++) {
    int vote; cin >> vote;
    if (vote > carlos) win = false;
  }

  cout << (win ? 'S' : 'N') << "\n";

  return 0;
}
```

