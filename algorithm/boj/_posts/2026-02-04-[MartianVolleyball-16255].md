---
layout: single
title: "[백준 16255] Martian Volleyball (C#, C++) - soo:bak"
date: "2026-02-04 22:00:00 +0900"
description: "백준 16255번 C#, C++ 풀이 - 현재 점수에서 승부가 끝날 때까지 필요한 최소 공 개수 구하기"
tags:
  - 백준
  - BOJ
  - 16255
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 16255, 백준 16255번, BOJ 16255, Martian Volleyball, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16255번 - Martian Volleyball](https://www.acmicpc.net/problem/16255)

## 설명
한 팀이 점수 k 이상이면서 상대보다 2점 이상 앞서면 경기가 끝납니다. 현재 점수가 x:y일 때 경기 종료까지 필요한 최소 공의 개수를 구하는 문제입니다.

<br>

## 접근법
큰 점수 a, 작은 점수 b로 두고 a가 앞서 있다고 보면, a가 그대로 이기는 경우가 최소 공입니다.

- 아직 a가 k에 못 미치면 k까지 k−a공이 필요합니다. k에 도달한 뒤에도 리드가 2점이 안 되면 부족한 만큼만 더 점수를 얻으면 됩니다.
- 이미 a ≥ k라면 점수 차가 2점이 될 때까지 a만 연속 득점시키면 끝입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine()!);
    for (int _ = 0; _ < t; _++) {
      var p = Console.ReadLine()!.Split();
      int k = int.Parse(p[0]);
      int x = int.Parse(p[1]);
      int y = int.Parse(p[2]);

      int a = Math.Max(x, y);
      int b = Math.Min(x, y);
      int diff = a - b;
      int ans;

      if (a < k) {
        int toK = k - a;
        int lead = diff + toK;
        int extra = Math.Max(0, 2 - lead);
        ans = toK + extra;
      } else {
        ans = 2 - diff;
      }

      Console.WriteLine(ans);
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

  int t; cin >> t;
  while (t--) {
    int k, x, y;
    cin >> k >> x >> y;
    int a = max(x, y);
    int b = min(x, y);
    int diff = a - b;
    int ans;
    if (a < k) {
      int toK = k - a;
      int lead = diff + toK;
      int extra = max(0, 2 - lead);
      ans = toK + extra;
    } else {
      ans = 2 - diff;
    }
    cout << ans << "\n";
  }

  return 0;
}
```
