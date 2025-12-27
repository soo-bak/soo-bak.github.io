---
layout: single
title: "[백준 30979] 유치원생 파댕이 돌보기 (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 30979번 C#, C++ 풀이 - 사탕 효과 시간 합이 돌봐야 하는 시간 이상인지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 30979
  - C#
  - C++
  - 알고리즘
keywords: "백준 30979, 백준 30979번, BOJ 30979, TakeCarePadaeng, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30979번 - 유치원생 파댕이 돌보기](https://www.acmicpc.net/problem/30979)

## 설명
파댕이를 T분 동안 돌봐야 하고, 각 사탕은 먹으면 일정 시간 동안 울음을 멈추게 합니다. 모든 사탕의 효과 시간을 합쳐 T분 이상이면 파댕이가 울지 않는지 판별하는 문제입니다.

<br>

## 접근법
사탕을 모두 사용하면 최대 효과를 얻을 수 있으므로, 모든 사탕의 효과 시간을 합산합니다. 합이 돌봐야 하는 시간 T 이상이면 파댕이는 울지 않고, 그렇지 않으면 웁니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var n = int.Parse(Console.ReadLine()!);
    var candies = Console.ReadLine()!.Split().Select(int.Parse);

    var total = 0;
    foreach (var f in candies)
      total += f;

    Console.WriteLine(total >= t ? "Padaeng_i Happy" : "Padaeng_i Cry");
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

  int t, n; cin >> t >> n;

  int total = 0;
  for (int i = 0; i < n; i++) {
    int f; cin >> f;
    total += f;
  }

  cout << (total >= t ? "Padaeng_i Happy" : "Padaeng_i Cry") << "\n";

  return 0;
}
```
