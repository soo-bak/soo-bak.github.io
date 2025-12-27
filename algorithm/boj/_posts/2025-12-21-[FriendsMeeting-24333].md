---
layout: single
title: "[백준 24333] СРЕЩА НА ПРИЯТЕЛИ (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 24333번 C#, C++ 풀이 - 두 사람의 가능한 시간 구간의 교집합 길이에서 k분을 제외한 대화 시간을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 24333
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
  - arithmetic
keywords: "백준 24333, 백준 24333번, BOJ 24333, FriendsMeeting, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24333번 - СРЕЩА НА ПРИЯТЕЛИ](https://www.acmicpc.net/problem/24333)

## 설명
두 사람이 가능한 시간 구간의 교집합 길이를 구하고, 그 안에 k분이 포함되면 1분을 빼서 대화 가능한 시간을 출력하는 문제입니다.

<br>

## 접근법
두 구간의 교집합은 각 시작점의 최댓값부터 끝점의 최솟값까지입니다. 교집합 길이를 구한 뒤, 제외해야 하는 시간이 그 안에 포함되면 1을 빼서 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var l1 = int.Parse(parts[0]);
    var r1 = int.Parse(parts[1]);
    var l2 = int.Parse(parts[2]);
    var r2 = int.Parse(parts[3]);
    var k = int.Parse(parts[4]);

    var left = Math.Max(l1, l2);
    var right = Math.Min(r1, r2);
    var overlap = Math.Max(0, right - left + 1);
    if (overlap > 0 && k >= left && k <= right) overlap--;

    Console.WriteLine(overlap);
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

  int l1, r1, l2, r2, k; cin >> l1 >> r1 >> l2 >> r2 >> k;

  int left = max(l1, l2);
  int right = min(r1, r2);
  int overlap = max(0, right - left + 1);
  if (overlap > 0 && k >= left && k <= right) overlap--;

  cout << overlap << "\n";

  return 0;
}
```
