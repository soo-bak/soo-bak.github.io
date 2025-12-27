---
layout: single
title: "[백준 31789] 모험의 시작 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 31789번 C#, C++ 풀이 - 예산 X 이내에서 공격력 S보다 큰 무기가 있는지 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 31789
  - C#
  - C++
  - 알고리즘
keywords: "백준 31789, 백준 31789번, BOJ 31789, AdventureStart, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31789번 - 모험의 시작](https://www.acmicpc.net/problem/31789)

## 설명
상점의 무기 목록에서 가격이 X 이하면서 공격력이 S보다 큰 무기가 있는지 확인하는 문제입니다.

<br>

## 접근법
모든 무기를 순회하며 가격이 예산 이하이고 공격력이 기준보다 큰 무기가 있는지 확인합니다.

하나라도 있으면 YES, 없으면 NO를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();
    var x = long.Parse(parts[0]);
    var s = long.Parse(parts[1]);

    var ok = false;
    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!.Split();
      var c = long.Parse(line[0]);
      var p = long.Parse(line[1]);
      if (c <= x && p > s) ok = true;
    }

    Console.WriteLine(ok ? "YES" : "NO");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  ll x, s; cin >> x >> s;

  bool ok = false;
  for (int i = 0; i < n; i++) {
    ll c, p; cin >> c >> p;
    if (c <= x && p > s) ok = true;
  }

  cout << (ok ? "YES" : "NO") << "\n";

  return 0;
}
```
