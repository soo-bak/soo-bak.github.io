---
layout: single
title: "[백준 12184] GBus count (Small) (C#, C++) - soo:bak"
date: "2026-02-06 22:33:00 +0900"
description: "백준 12184번 C#, C++ 풀이 - 관심 도시별로 운행하는 GBus 개수를 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 12184
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 12184, 백준 12184번, BOJ 12184, GBus count, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12184번 - GBus count (Small)](https://www.acmicpc.net/problem/12184)

## 설명
N개의 버스 구간 [Ai, Bi]가 주어질 때, 관심 있는 P개 도시마다 해당 구간에 포함되는 버스 개수를 구하는 문제입니다.

입력 사이에 공백 줄이 있어도 공백 기준 토큰화하면 됩니다.

<br>

## 접근법
도시 번호는 1~500이므로 구간마다 배열을 누적하거나, 각 질의에 대해 모든 구간을 확인해도 됩니다.

N, P ≤ 50이니 단순하게 각 도시를 모든 구간과 비교하여 포함 여부를 세면 충분합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var tokens = Console.In.ReadToEnd().Split((char[])null!, StringSplitOptions.RemoveEmptyEntries);
    int idx = 0;
    int t = int.Parse(tokens[idx++]);
    var sb = new StringBuilder();
    for (int tc = 1; tc <= t; tc++) {
      int n = int.Parse(tokens[idx++]);
      var a = new int[n];
      var b = new int[n];
      for (int i = 0; i < n; i++) {
        a[i] = int.Parse(tokens[idx++]);
        b[i] = int.Parse(tokens[idx++]);
      }
      int p = int.Parse(tokens[idx++]);
      sb.Append("Case #").Append(tc).Append(":");
      for (int i = 0; i < p; i++) {
        int c = int.Parse(tokens[idx++]);
        int cnt = 0;
        for (int j = 0; j < n; j++)
          if (a[j] <= c && c <= b[j]) cnt++;
        sb.Append(' ').Append(cnt);
      }
      sb.Append('\n');
    }
    Console.Write(sb.ToString());
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

  vi tok;
  tok.reserve(10000);
  string s;
  while (cin >> s) tok.push_back(stoi(s));
  int idx = 0;
  int T = tok[idx++];
  for (int tc = 1; tc <= T; tc++) {
    int n = tok[idx++];
    vi a(n), b(n);
    for (int i = 0; i < n; i++) {
      a[i] = tok[idx++];
      b[i] = tok[idx++];
    }
    int p = tok[idx++];
    cout << "Case #" << tc << ":";
    for (int i = 0; i < p; i++) {
      int c = tok[idx++];
      int cnt = 0;
      for (int j = 0; j < n; j++)
        if (a[j] <= c && c <= b[j]) cnt++;
      cout << ' ' << cnt;
    }
    cout << "\n";
  }
  return 0;
}
```
