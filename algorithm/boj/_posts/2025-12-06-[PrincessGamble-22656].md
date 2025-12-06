---
layout: single
title: "[백준 22656] Princess' Gamble (C#, C++) - soo:bak"
date: "2025-12-06 23:10:00 +0900"
description: 파리뮤추엘 방식으로 총 배팅 금액에서 차감률 P%를 제외한 금액을 당첨 티켓 수로 나눠 1장당 배당금을 구하는 백준 22656번 Princess' Gamble 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[22656번 - Princess' Gamble](https://www.acmicpc.net/problem/22656)

## 설명
각 경기 참가자별로 구매된 투표권 수 `X_i`가 주어집니다. 모든 투표권 가격은 동일하며, 총 금액에서 `P%`를 공제한 뒤 우승자에게 투표한 사람들에게 비율대로 나누어 줍니다.<br>
우승자의 번호 `M`에 대한 투표권이 하나도 없으면 배당은 0입니다. 배당금이 정수가 아니면 버림(정수 나눗셈)으로 처리합니다.<br>

## 접근법
- 전체 투표권 수 `total = Σ X_i`.
- 공제 후 풀에 남는 투표권 수는 `total * (100 - P)` (가격이 동일하므로 100을 곱했다가 상쇄됩니다).
- 우승자에게 투표한 `X_M`으로 나누어 1장당 배당금을 구합니다.
- `X_M == 0`이면 바로 0을 출력합니다.
<br>

- - -

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    while (true) {
      var first = Console.ReadLine()!.Split();
      int N = int.Parse(first[0]);
      int M = int.Parse(first[1]);
      int P = int.Parse(first[2]);
      if (N == 0 && M == 0 && P == 0) break;

      int[] x = new int[N];
      for (int i = 0; i < N; i++) x[i] = int.Parse(Console.ReadLine()!);

      int win = x[M - 1];
      if (win == 0) {
        Console.WriteLine(0);
        continue;
      }

      int total = x.Sum();
      int payout = total * (100 - P) / win;
      Console.WriteLine(payout);
    }
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

  while (true) {
    int N, M, P;
    cin >> N >> M >> P;
    if (N == 0 && M == 0 && P == 0) break;

    vector<int> x(N);
    for (int i = 0; i < N; i++) cin >> x[i];

    int win = x[M - 1];
    if (win == 0) {
      cout << 0 << "\n";
      continue;
    }

    int total = accumulate(x.begin(), x.end(), 0);
    int payout = total * (100 - P) / win;
    cout << payout << "\n";
  }
  return 0;
}
```
