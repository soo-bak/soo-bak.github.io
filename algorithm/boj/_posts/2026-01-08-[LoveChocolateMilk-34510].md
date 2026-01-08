---
layout: single
title: "[백준 34510] 초콜릿 우유가 좋아 (C#, C++) - soo:bak"
date: "2026-01-08 15:00:00 +0900"
description: 우유갑을 정/역 방향으로 교대로 쌓을 때의 전체 높이를 수식으로 계산하는 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 34510
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 34510, 백준 34510번, BOJ 34510, 초콜릿 우유가 좋아, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[34510번 - 초콜릿 우유가 좋아](https://www.acmicpc.net/problem/34510)

## 설명
우유갑 높이는 꼭지 H1, 머리 H2, 몸통 H3이며 H1 ≤ H2 ≤ H3입니다. 1층은 정방향, 그 위는 정방향과 역방향이 교대로 쌓입니다. 아래층이 정방향이면 역방향을 올릴 때 높이가 H3 - H1만 늘고, 아래층이 역방향이면 정방향을 올릴 때 H1 + H2 + H3만 늘어납니다. 전체 높이를 닫힌 식으로 계산하는 문제입니다.

<br>

## 접근법
먼저 한 층을 그대로 올릴 때 증가량을 A = H1 + H2 + H3로 두고, 뒤집혀 맞닿을 때 증가량을 B = H3 - H1로 둡니다.

다음으로 층수가 짝수인 경우 A와 B가 같은 횟수로 더해집니다. N = 2k이면 높이는 k × (A + B)가 됩니다. 층수가 홀수인 경우 A가 한 번 더 사용되므로 N = 2k + 1이면 높이는 (k + 1) × A + k × B가 됩니다.

이후 N이 최대 10^12이므로 64비트 정수로 계산하면 충분합니다.

시간 복잡도는 O(1)입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var h1 = long.Parse(parts[0]);
    var h2 = long.Parse(parts[1]);
    var h3 = long.Parse(parts[2]);
    var n = long.Parse(Console.ReadLine()!);

    var a = h1 + h2 + h3;
    var b = h3 - h1;

    long result;
    if (n % 2 == 0) {
      var k = n / 2;
      result = k * (a + b);
    } else {
      var k = n / 2;
      result = (k + 1) * a + k * b;
    }

    Console.WriteLine(result);
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

  ll h1, h2, h3, n;
  cin >> h1 >> h2 >> h3 >> n;

  ll a = h1 + h2 + h3;
  ll b = h3 - h1;

  ll ans;
  if (n % 2 == 0) {
    ll k = n / 2;
    ans = k * (a + b);
  } else {
    ll k = n / 2;
    ans = (k + 1) * a + k * b;
  }

  cout << ans << "\n";

  return 0;
}
```
