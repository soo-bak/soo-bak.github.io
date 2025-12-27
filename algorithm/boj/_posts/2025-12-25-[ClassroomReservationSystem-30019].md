---
layout: single
title: "[백준 30019] 강의실 예약 시스템 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 30019번 C#, C++ 풀이 - 강의실별 마지막 종료 시각으로 예약 수락 여부를 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 30019
  - C#
  - C++
  - 알고리즘
  - 구현
  - 그리디
keywords: "백준 30019, 백준 30019번, BOJ 30019, ClassroomReservationSystem, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30019번 - 강의실 예약 시스템](https://www.acmicpc.net/problem/30019)

## 설명
예약 요청이 시작 시각 오름차순으로 주어질 때, 각 요청의 수락 여부를 판단하는 문제입니다.

<br>

## 접근법
요청이 시작 시각 순서로 주어지므로, 강의실마다 마지막으로 수락한 예약의 종료 시각만 저장하면 됩니다.  
시작 시각이 마지막 종료 시각 이상이면 YES로 수락하고 종료 시각을 갱신합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var m = int.Parse(parts[idx++]);

    var last = new int[n + 1];
    var sb = new StringBuilder();
    for (var i = 0; i < m; i++) {
      var k = int.Parse(parts[idx++]);
      var s = int.Parse(parts[idx++]);
      var e = int.Parse(parts[idx++]);

      if (s >= last[k]) {
        last[k] = e;
        sb.AppendLine("YES");
      } else sb.AppendLine("NO");
    }

    Console.Write(sb);
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

  int n, m; cin >> n >> m;
  vector<int> last(n + 1, 0);
  for (int i = 0; i < m; i++) {
    int k, s, e; cin >> k >> s >> e;
    if (s >= last[k]) {
      last[k] = e;
      cout << "YES\n";
    } else cout << "NO\n";
  }

  return 0;
}
```
