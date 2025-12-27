---
layout: single
title: "[백준 16175] General Election (C#, C++) - soo:bak"
date: "2025-12-20 12:12:00 +0900"
description: "백준 16175번 C#, C++ 풀이 - 지역별 득표수를 합산해 최다 득표 후보를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 16175
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 16175, 백준 16175번, BOJ 16175, GeneralElection, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16175번 - General Election](https://www.acmicpc.net/problem/16175)

## 설명
각 지역별 득표수가 주어질 때, 모든 지역 득표를 합산하여 최다 득표 후보 번호를 출력하는 문제입니다.

<br>

## 접근법
먼저 각 후보의 총 득표를 배열에 누적합니다.

이후 최댓값을 가진 인덱스를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 0; tc < t; tc++) {
      var first = Console.ReadLine()!.Split();
      var n = int.Parse(first[0]);
      var m = int.Parse(first[1]);
      var sum = new int[n];

      for (var i = 0; i < m; i++) {
        var parts = Console.ReadLine()!.Split();
        for (var j = 0; j < n; j++)
          sum[j] += int.Parse(parts[j]);
      }

      var best = 0;
      for (var i = 1; i < n; i++) {
        if (sum[i] > sum[best]) best = i;
      }

      Console.WriteLine(best + 1);
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

  int t; cin >> t;
  while (t--) {
    int n, m; cin >> n >> m;
    vi sum(n, 0);

    for (int i = 0; i < m; i++) {
      for (int j = 0; j < n; j++) {
        int v; cin >> v;
        sum[j] += v;
      }
    }

    int best = 0;
    for (int i = 1; i < n; i++) {
      if (sum[i] > sum[best]) best = i;
    }

    cout << best + 1 << "\n";
  }

  return 0;
}
```
