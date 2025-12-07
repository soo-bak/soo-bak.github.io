---
layout: single
title: "[백준 14956] Philosopher’s Walk (C#, C++) - soo:bak"
date: "2025-12-08 00:22:00 +0900"
description: 힐베르트 커브 성질을 이용해 n=2^k 격자에서 m번째 위치의 좌표를 구하는 백준 14956번 Philosopher’s Walk 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[14956번 - Philosopher’s Walk](https://www.acmicpc.net/problem/14956)

## 설명
한 변의 길이가 2의 거듭제곱인 격자에서 힐베르트 커브를 따라 걸을 때, 특정 번째 걸음의 좌표를 구하는 문제입니다.

<br>

## 접근법
힐베르트 커브는 재귀적인 구조를 가지고 있습니다. 가장 작은 2×2 격자에서는 왼쪽 아래에서 시작해 위로, 오른쪽으로, 아래로 이동하는 4칸짜리 패턴이 기본이 됩니다.

더 큰 격자는 4개의 사분면으로 나뉘고, 각 사분면에 작은 힐베르트 커브가 회전하거나 대칭되어 배치됩니다. 몇 번째 걸음인지에 따라 어느 사분면에 속하는지 결정하고, 그 사분면 내에서의 상대적인 위치를 재귀적으로 구합니다.

사분면에 따라 좌표 변환 방식이 다릅니다. 왼쪽 아래 사분면은 좌표를 뒤집고, 오른쪽 아래 사분면은 뒤집은 뒤 반대 방향으로 이동합니다. 위쪽 두 사분면은 그대로 위치만 이동시킵니다.

입력이 1부터 시작하므로 내부에서는 0부터 시작하는 인덱스로 계산한 뒤 결과를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static (long x, long y) Hilbert(long n, long m) {
    if (n == 2) {
      return m switch {
        0 => (1, 1),
        1 => (1, 2),
        2 => (2, 2),
        _ => (2, 1)
      };
    }

    var half = n / 2;
    var block = half * half;
    var quad = m / block;
    var p = Hilbert(half, m % block);

    return quad switch {
      0 => (p.y, p.x),
      1 => (p.x, p.y + half),
      2 => (p.x + half, p.y + half),
      _ => (2 * half - p.y + 1, half - p.x + 1)
    };
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = long.Parse(parts[0]);
    var m = long.Parse(parts[1]) - 1;

    var res = Hilbert(n, m);
    Console.WriteLine($"{res.x} {res.y}");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<ll, ll> pll;

pll hilbert(ll n, ll m) {
  if (n == 2) {
    if (m == 0) return {1, 1};
    if (m == 1) return {1, 2};
    if (m == 2) return {2, 2};
    return {2, 1};
  }
  ll half = n / 2;
  ll block = half * half;
  ll quad = m / block;
  auto p = hilbert(half, m % block);
  if (quad == 0) return {p.second, p.first};
  if (quad == 1) return {p.first, p.second + half};
  if (quad == 2) return {p.first + half, p.second + half};
  return {2 * half - p.second + 1, half - p.first + 1};
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n, m; cin >> n >> m;
  auto ans = hilbert(n, m - 1);
  cout << ans.first << " " << ans.second << "\n";

  return 0;
}
```
