---
layout: single
title: "[백준 25527] Counting Peaks of Infection (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 25527번 C#, C++ 풀이 - 일일 확진자 수에서 양옆보다 큰 날의 개수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 25527
  - C#
  - C++
  - 알고리즘
keywords: "백준 25527, 백준 25527번, BOJ 25527, CountingPeaksOfInfection, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25527번 - Counting Peaks of Infection](https://www.acmicpc.net/problem/25527)

## 설명
여러 날의 확진자 수가 주어질 때, 전날과 다음 날보다 모두 큰 날을 피크로 정의하고 각 데이터셋마다 피크의 개수를 출력하는 문제입니다. 첫날은 0명이며 마지막 날은 피크에서 제외합니다.

<br>

## 접근법
피크는 양쪽 이웃보다 값이 큰 날입니다. 첫날과 마지막 날은 양쪽 이웃이 모두 존재하지 않으므로 피크가 될 수 없습니다.

두 번째 날부터 마지막 전날까지 순회하며 현재 날의 확진자 수가 전날과 다음 날보다 모두 크면 피크로 셉니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      var n = int.Parse(line);
      if (n == 0) break;

      var vals = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var cnt = 0;
      for (var i = 1; i < n - 1; i++) {
        if (vals[i] > vals[i - 1] && vals[i] > vals[i + 1]) cnt++;
      }
      Console.WriteLine(cnt);
    }
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

  int n;
  while (cin >> n) {
    if (n == 0) break;
    vi v(n);
    for (int i = 0; i < n; i++)
      cin >> v[i];

    int cnt = 0;
    for (int i = 1; i + 1 < n; i++) {
      if (v[i] > v[i - 1] && v[i] > v[i + 1]) cnt++;
    }

    cout << cnt << "\n";
  }

  return 0;
}
```
