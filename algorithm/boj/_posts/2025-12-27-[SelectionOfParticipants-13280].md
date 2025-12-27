---
layout: single
title: "[백준 13280] Selection of Participants of an Experiment (C#, C++) - soo:bak"
date: "2025-12-27 03:05:00 +0900"
description: "백준 13280번 C#, C++ 풀이 - 점수 차이가 가장 작은 두 학생을 찾아 차이를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 13280
  - C#
  - C++
  - 알고리즘
  - 브루트포스
  - 정렬
keywords: "백준 13280, 백준 13280번, BOJ 13280, SelectionOfParticipants, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13280번 - Selection of Participants of an Experiment](https://www.acmicpc.net/problem/13280)

## 설명
여러 데이터셋에서 학생 점수 목록이 주어질 때, 점수 차이가 가장 작은 두 학생을 찾아 그 차이를 출력하는 문제입니다.

입력이 0을 만나면 종료합니다.

<br>

## 접근법
각 데이터셋마다 점수를 정렬한 뒤, 인접한 값들의 차이 중 최소값을 구하면 됩니다.

정렬은 O(n log n), 인접 비교는 O(n)입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var sb = new StringBuilder();

    while (idx < parts.Length) {
      var n = int.Parse(parts[idx++]);
      if (n == 0) break;

      var arr = new int[n];
      for (var i = 0; i < n; i++)
        arr[i] = int.Parse(parts[idx++]);

      Array.Sort(arr);
      var best = int.MaxValue;
      for (var i = 1; i < n; i++) {
        var diff = arr[i] - arr[i - 1];
        if (diff < best) best = diff;
      }

      sb.AppendLine(best.ToString());
    }

    Console.Write(sb);
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
  while (cin >> n && n) {
    vi a(n);
    for (int i = 0; i < n; i++)
      cin >> a[i];

    sort(a.begin(), a.end());
    int best = INT_MAX;
    for (int i = 1; i < n; i++) {
      int diff = a[i] - a[i - 1];
      if (diff < best) best = diff;
    }

    cout << best << "\n";
  }

  return 0;
}
```
