---
layout: single
title: "[백준 22656] Princess' Gamble (C#, C++) - soo:bak"
date: "2025-12-06 23:10:00 +0900"
description: 파리뮤추엘 방식으로 총 배팅 금액에서 차감률을 제외한 금액을 당첨 티켓 수로 나눠 배당금을 구하는 백준 22656번 Princess' Gamble 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 22656
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 22656, 백준 22656번, BOJ 22656, PrincessGamble, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[22656번 - Princess' Gamble](https://www.acmicpc.net/problem/22656)

## 설명
각 경기 참가자별로 구매된 투표권 수가 주어집니다. 모든 투표권 가격은 동일하며, 총 금액에서 P%를 공제한 뒤 우승자에게 투표한 사람들에게 비율대로 나누어 줍니다.

우승자의 번호 M에 대한 투표권이 하나도 없으면 배당은 0입니다. 배당금이 정수가 아니면 버림으로 처리합니다.

<br>

## 접근법
먼저, 전체 투표권 수의 합을 구합니다.

다음으로, 공제 후 남는 금액은 전체 합에 100에서 P를 뺀 값을 곱한 것입니다. 이를 우승자에게 투표한 수로 나누면 1장당 배당금이 됩니다.

이후, 우승자에게 투표한 수가 0이면 바로 0을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      while (true) {
        var first = Console.ReadLine()!.Split();
        var n = int.Parse(first[0]);
        var m = int.Parse(first[1]);
        var p = int.Parse(first[2]);
        if (n == 0)
          break;

        var v = new int[n + 1];
        for (var i = 1; i <= n; i++)
          v[i] = int.Parse(Console.ReadLine()!);

        if (v[m] == 0) {
          Console.WriteLine(0);
          continue;
        }

        Console.WriteLine(v.Sum() * (100 - p) / v[m]);
      }
    }
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

  int n, m, p;
  while (cin >> n >> m >> p) {
    if (!n)
      break;

    vi v(n + 1);
    for (int i = 1; i <= n; i++)
      cin >> v[i];

    if (!v[m]) {
      cout << "0\n";
      continue;
    }

    cout << accumulate(v.begin(), v.end(), 0) * (100 - p) / v[m] << "\n";
  }

  return 0;
}
```
