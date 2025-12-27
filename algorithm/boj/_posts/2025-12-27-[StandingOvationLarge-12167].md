---
layout: single
title: "[백준 12167] Standing Ovation (Large) (C#, C++) - soo:bak"
date: "2025-12-27 07:15:00 +0900"
description: "백준 12167번 C#, C++ 풀이 - 큰 Smax에서도 최소 친구 수를 구해 모두 기립박수하게 만드는 문제"
tags:
  - 백준
  - BOJ
  - 12167
  - C#
  - C++
  - 알고리즘
keywords: "백준 12167, 백준 12167번, BOJ 12167, StandingOvationLarge, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12167번 - Standing Ovation (Large)](https://www.acmicpc.net/problem/12167)

## 설명
부끄러움 수치가 k인 관객은 최소 k명이 이미 서 있어야 일어납니다. 모든 관객이 기립박수를 하도록 초대해야 할 친구의 최소 수를 구하는 문제입니다.

<br>

## 접근법
부끄러움 수치 0부터 순서대로 순회하며 현재 서 있는 인원을 관리합니다.

수치 k인 관객이 일어나려면 k명이 이미 서 있어야 합니다. 현재 인원이 부족하면 그 차이만큼 친구를 추가합니다. 이후 해당 수치의 관객을 기립 인원에 더합니다.

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
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var cs = 1; cs <= t; cs++) {
      var smax = int.Parse(parts[idx++]);
      var s = parts[idx++];

      var standing = 0;
      var added = 0;
      for (var i = 0; i <= smax; i++) {
        var cnt = s[i] - '0';
        if (standing < i) {
          var need = i - standing;
          added += need;
          standing += need;
        }
        standing += cnt;
      }

      sb.AppendLine($"Case #{cs}: {added}");
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

  int t; cin >> t;
  for (int cs = 1; cs <= t; cs++) {
    int smax; string s;
    cin >> smax >> s;

    int standing = 0, added = 0;
    for (int i = 0; i <= smax; i++) {
      int cnt = s[i] - '0';
      if (standing < i) {
        int need = i - standing;
        added += need;
        standing += need;
      }
      standing += cnt;
    }

    cout << "Case #" << cs << ": " << added << "\n";
  }

  return 0;
}
```
