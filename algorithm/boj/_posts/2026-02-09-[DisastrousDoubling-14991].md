---
layout: single
title: "[백준 14991] Disastrous Doubling (C#, C++) - soo:bak"
date: "2026-02-09 21:51:00 +0900"
description: "백준 14991번 C#, C++ 풀이 - 시간마다 두 배로 늘어나는 박테리아를 실험에 소모한 뒤 남는 개수(또는 error)를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 14991
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 14991, 백준 14991번, BOJ 14991, Disastrous Doubling, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14991번 - Disastrous Doubling](https://www.acmicpc.net/problem/14991)

## 설명
시간마다 두 배로 늘어나는 박테리아를 실험에 사용하면서, 끝까지 진행했을 때 남는 개수를 구하는 문제입니다.

중간에 박테리아가 모자라면 error를 출력하고, 끝까지 진행되면 남은 개수를 1,000,000,007로 나눈 값을 출력합니다.

<br>

## 접근법
먼저 실제 개수는 너무 커지므로, 부족 여부만 보는 상한값과 출력용 나머지 값만 두고 진행합니다.

다음으로 매 시간 상한값을 두 배로 키운 뒤 그 시간에 쓸 만큼 뺍니다. 상한값이 필요한 양보다 작아지면 그 시점에서 error를 출력하고 끝냅니다.

이후 나머지도 같은 식으로 두 배 후 빼기를 반복해, 1,000,000,007로 나눈 나머지를 유지합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
 
class Program {
  const long mod = 1_000_000_007L;
  const long capMax = 1L << 61;

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();

    long cap = 1;
    long rem = 1;
    for (var i = 0; i < n; i++) {
      var need = long.Parse(parts[i]);

      cap = cap >= (capMax >> 1) ? capMax : cap * 2;
      rem = (rem * 2) % mod;

      if (cap < need) {
        Console.WriteLine("error");
        return;
      }

      cap -= need;
      rem = (rem - (need % mod) + mod) % mod;
      if (rem < 0) {
        rem += mod;
      }
    }

    Console.WriteLine(rem);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
 
const ll mod = 1'000'000'007LL;
const ll capMax = 1LL << 61;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<ll> b(n);
  for (int i = 0; i < n; i++) {
    cin >> b[i];
  }

  ll cap = 1, rem = 1;
  for (int i = 0; i < n; i++) {
    cap = cap >= (capMax >> 1) ? capMax : cap * 2;
    rem = (rem * 2) % mod;

    if (cap < b[i]) {
      cout << "error\n";
      return 0;
    }

    cap -= b[i];
    rem = (rem - (ll)(b[i] % mod) + mod) % mod;
  }

  cout << rem << "\n";

  return 0;
}
```
