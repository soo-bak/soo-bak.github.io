---
layout: single
title: "[백준 12572] Rope Intranet (Large) (C#, C++) - soo:bak"
date: "2025-12-27 00:12:00 +0900"
description: 전선을 정렬한 뒤 역순 쌍을 세어 교차 개수를 구하는 백준 12572번 Rope Intranet (Large) 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 12572
  - C#
  - C++
  - 알고리즘
  - 구현
  - 브루트포스
keywords: "백준 12572, 백준 12572번, BOJ 12572, RopeIntranetLarge, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12572번 - Rope Intranet (Large)](https://www.acmicpc.net/problem/12572)

## 설명
왼쪽 건물과 오른쪽 건물의 창문을 잇는 전선들이 주어질 때, 서로 교차하는 지점의 개수를 구하는 문제입니다.

<br>

## 접근법
두 전선이 교차하려면 한쪽 건물에서의 순서와 다른 쪽 건물에서의 순서가 뒤바뀌어야 합니다.

전선을 왼쪽 건물 기준으로 정렬한 뒤, 오른쪽 건물 값들 중 앞에 있는데 더 큰 쌍의 개수를 세면 됩니다.



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
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var tc = 1; tc <= t; tc++) {
      var n = int.Parse(parts[idx++]);
      var wires = new (int a, int b)[n];
      for (var i = 0; i < n; i++) {
        var a = int.Parse(parts[idx++]);
        var b = int.Parse(parts[idx++]);
        wires[i] = (a, b);
      }

      Array.Sort(wires, (x, y) => x.a.CompareTo(y.a));

      var count = 0L;
      for (var i = 0; i < n; i++) {
        for (var j = i + 1; j < n; j++) {
          if (wires[i].b > wires[j].b)
            count++;
        }
      }

      sb.AppendLine($"Case #{tc}: {count}");
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int T; cin >> T;
  for (int tc = 1; tc <= T; tc++) {
    int n; cin >> n;
    vector<pii> wires(n);
    for (int i = 0; i < n; i++)
      cin >> wires[i].first >> wires[i].second;

    sort(wires.begin(), wires.end());

    ll count = 0;
    for (int i = 0; i < n; i++) {
      for (int j = i + 1; j < n; j++) {
        if (wires[i].second > wires[j].second)
          count++;
      }
    }

    cout << "Case #" << tc << ": " << count << "\n";
  }

  return 0;
}
```
