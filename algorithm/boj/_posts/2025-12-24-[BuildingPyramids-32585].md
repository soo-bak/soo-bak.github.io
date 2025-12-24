---
layout: single
title: "[백준 32585] Building Pyramids (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 한 변 길이 n인 정사면체 구슬 수를 계산하는 문제
---

## 문제 링크
[32585번 - Building Pyramids](https://www.acmicpc.net/problem/32585)

## 설명
한 변에 구슬 n개가 있는 정사면체를 이루는 전체 구슬 수를 구하는 문제입니다.

<br>

## 접근법
정사면체의 맨 위층에는 구슬 1개, 그 아래층에는 1+2=3개, 그 다음에는 1+2+3=6개처럼 삼각형 모양으로 구슬이 늘어납니다.

이 값들을 모두 더하면 전체 구슬 수가 되고, 한 변 길이 n에 대해 n × (n+1) × (n+2) / 6 공식으로 계산할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = long.Parse(Console.ReadLine()!);
    var ans = n * (n + 1) * (n + 2) / 6;
    Console.WriteLine(ans);
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

  ll n; cin >> n;
  ll ans = n * (n + 1) * (n + 2) / 6;
  cout << ans << "\n";

  return 0;
}
```
