---
layout: single
title: "[백준 14551] Card Game Contest (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 14551번 C#, C++ 풀이 - 각 게임의 선택 개수를 곱해 참여 방법 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 14551
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
  - 조합론
keywords: "백준 14551, 백준 14551번, BOJ 14551, CardGameContest, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14551번 - Card Game Contest](https://www.acmicpc.net/problem/14551)

## 설명
각 게임에서 선택 가능한 카드 덱의 수가 주어질 때, 서로 다른 참여 방법의 수를 구하는 문제입니다.

<br>

## 접근법
각 게임에서 선택 가능한 덱 수는 `Ai`가 0이면 1, 아니면 `Ai`입니다.  
모든 게임의 선택은 독립이므로 곱한 뒤 `M`으로 나눈 나머지를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var mod = int.Parse(parts[idx++]);

    var ans = 1 % mod;
    for (var i = 0; i < n; i++) {
      var a = int.Parse(parts[idx++]);
      var choices = a == 0 ? 1 : a;
      ans = (ans * choices) % mod;
    }

    Console.WriteLine(ans);
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

  int n, mod; cin >> n >> mod;
  int ans = 1 % mod;
  for (int i = 0; i < n; i++) {
    int a; cin >> a;
    int choices = (a == 0 ? 1 : a);
    ans = (ans * choices) % mod;
  }

  cout << ans << "\n";

  return 0;
}
```
