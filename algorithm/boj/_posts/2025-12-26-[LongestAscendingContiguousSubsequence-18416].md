---
layout: single
title: "[백준 18416] 最長昇順連続部分列 (Longest Ascending Contiguous Subsequence) (C#, C++) - soo:bak"
date: "2025-12-26 04:11:00 +0900"
description: "백준 18416번 C#, C++ 풀이 - 비내림 연속 부분수열의 최장 길이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 18416
  - C#
  - C++
  - 알고리즘
keywords: "백준 18416, 백준 18416번, BOJ 18416, LongestAscendingContiguousSubsequence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18416번 - 最長昇順連続部分列 (Longest Ascending Contiguous Subsequence)](https://www.acmicpc.net/problem/18416)

## 설명
수열에서 연속하면서 비내림인 부분수열의 최대 길이를 구하는 문제입니다.

<br>

## 접근법
먼저 현재 연속 길이를 1로 시작합니다.

다음으로 이전 값보다 작아지면 길이를 1로 초기화하고, 그렇지 않으면 1 늘립니다.

마지막으로 최댓값을 갱신하며 끝까지 확인한 뒤 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();

    var best = 1;
    var cur = 1;
    var prev = int.Parse(parts[0]);

    for (var i = 1; i < n; i++) {
      var v = int.Parse(parts[i]);
      if (v < prev) cur = 1;
      else cur++;
      if (cur > best) best = cur;
      prev = v;
    }

    Console.WriteLine(best);
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

  int best = 1;
  int cur = 1;
  int prev; cin >> prev;

  for (int i = 1; i < n; i++) {
    int v; cin >> v;
    
    if (v < prev) cur = 1;
    else cur++;
    if (cur > best) best = cur;
    prev = v;
  }

  cout << best << "\n";
  return 0;
}
```
