---
layout: single
title: "[백준 17273] 카드 공장 (Small) (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 17273번 C#, C++ 풀이 - 조건에 따라 카드의 앞뒷면을 뒤집고 합을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 17273
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 17273, 백준 17273번, BOJ 17273, CardFactorySmall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17273번 - 카드 공장 (Small)](https://www.acmicpc.net/problem/17273)

## 설명
명령마다 보이는 면이 K 이하인 카드를 뒤집은 뒤, 최종 보이는 면의 합을 구하는 문제입니다.

<br>

## 접근법
카드의 현재 보이는 값 배열을 유지하고, 각 명령마다 조건을 만족하는 카드의 값을 뒤집습니다.  
N과 M이 작으므로 그대로 시뮬레이션하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var m = int.Parse(parts[idx++]);

    var front = new int[n];
    var back = new int[n];
    var cur = new int[n];
    for (var i = 0; i < n; i++) {
      front[i] = int.Parse(parts[idx++]);
      back[i] = int.Parse(parts[idx++]);
      cur[i] = front[i];
    }

    for (var i = 0; i < m; i++) {
      var k = int.Parse(parts[idx++]);
      for (var j = 0; j < n; j++) {
        if (cur[j] <= k) {
          cur[j] = (cur[j] == front[j]) ? back[j] : front[j];
        }
      }
    }

    var sum = 0;
    for (var i = 0; i < n; i++) sum += cur[i];
    Console.WriteLine(sum);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vi front(n), back(n), cur(n);
  for (int i = 0; i < n; i++) {
    cin >> front[i] >> back[i];
    cur[i] = front[i];
  }

  for (int i = 0; i < m; i++) {
    int k; cin >> k;
    for (int j = 0; j < n; j++) {
      if (cur[j] <= k) {
        cur[j] = (cur[j] == front[j]) ? back[j] : front[j];
      }
    }
  }

  int sum = 0;
  for (int i = 0; i < n; i++) sum += cur[i];
  cout << sum << "\n";

  return 0;
}
```
