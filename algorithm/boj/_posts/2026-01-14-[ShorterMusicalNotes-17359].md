---
layout: single
title: "[백준 17359] Shorter Musical Notes (C#, C++) - soo:bak"
date: "2026-01-14 20:25:00 +0900"
description: "백준 17359번 C#, C++ 풀이 - 누적 길이 배열을 만든 뒤 질의를 이분 탐색으로 처리해 각 비트에서 연주할 음을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 17359
  - C#
  - C++
  - 알고리즘
  - 구현
  - 이분 탐색
keywords: "백준 17359, 백준 17359번, BOJ 17359, Shorter Musical Notes, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17359번 - Shorter Musical Notes](https://www.acmicpc.net/problem/17359)

## 설명
N개의 음표로 구성된 노래가 시간 0부터 시작하며 i번째 음표는 B_i 비트 동안 지속되는 경우,

시간 T가 주어질 때 그 시간에 연주되는 음표의 번호를 출력하는 문제입니다.

<br>

## 접근법
각 음표의 시작 시각을 누적하여 저장한 후, 각 질의 T에 대해 이분 탐색으로 T가 속하는 구간을 찾습니다.

T보다 큰 시작 시각이 처음 나타나는 위치가 해당 음표의 번호입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;
using System.Text;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    var n = first[0];
    var q = first[1];

    var b = new int[n];
    var pref = new long[n + 1];
    for (var i = 0; i < n; i++) {
      b[i] = int.Parse(Console.ReadLine()!);
      pref[i + 1] = pref[i] + b[i];
    }

    var sb = new StringBuilder();
    for (var qi = 0; qi < q; qi++) {
      var t = long.Parse(Console.ReadLine()!);
      var idx = Array.BinarySearch(pref, t + 1);
      if (idx < 0)
        idx = ~idx;
      sb.Append(idx).Append('\n');
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
typedef vector<int> vi;
typedef vector<ll> vl;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, q; cin >> n >> q;
  vi b(n);
  vl pref(n + 1, 0);
  for (int i = 0; i < n; i++) {
    cin >> b[i];
    pref[i + 1] = pref[i] + b[i];
  }

  while (q--) {
    ll t; cin >> t;
    auto it = lower_bound(pref.begin() + 1, pref.end(), t + 1);
    int idx = int(it - pref.begin());
    cout << idx << "\n";
  }

  return 0;
}
```
