---
layout: single
title: "[백준 5585] 거스름돈 (C#, C++) - soo:bak"
date: "2025-05-02 05:17:00 +0900"
description: 가장 적은 개수의 동전으로 거스름돈을 줄 때 필요한 최소 동전 수를 계산하는 백준 5585번 거스름돈 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5585
  - C#
  - C++
  - 알고리즘
keywords: "백준 5585, 백준 5585번, BOJ 5585, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5585번 - 거스름돈](https://www.acmicpc.net/problem/5585)

## 설명
물건을 사고 난 뒤 `1,000엔` 지폐를 냈을 때,

잔돈을 가장 적은 개수의 동전으로 주기 위한 **최소 동전 수**를 구하는 문제입니다.

<br>
**JOI잡화점**에는 다음과 같은 동전이 무한히 있다고 가정합니다:
- `500엔`, `100엔`, `50엔`, `10엔`, `5엔`, `1엔`

<br>
예를 들어 `620엔`을 지불했다면 잔돈은 `380엔`이며,

`500엔 → 0`, `100엔 → 3`, `50엔 → 1`, `10엔 → 3` = 총 `7개` 동전이 필요합니다.

<br>

## 접근법

- 먼저 지불한 금액을 `1,000엔`에서 뺀 잔돈을 계산합니다.
- 큰 단위 동전부터 순서대로 사용하여 잔돈을 줄여나갑니다.
- 해당 동전으로 나눌 수 있는 만큼 최대한 사용한 뒤, 남은 금액에 대해 다음 동전을 사용합니다.
- 동전의 개수를 누적하여 출력합니다.

**그리디 알고리듬**의 대표적인 예로, 동전을 큰 단위부터 사용하는 방식으로 항상 최적의 해를 얻을 수 있습니다.

> 참고 : [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int pay = int.Parse(Console.ReadLine());
    int change = 1000 - pay;
    int[] coins = { 500, 100, 50, 10, 5, 1 };
    int count = 0;

    foreach (int coin in coins) {
      count += change / coin;
      change %= coin;
    }
    Console.WriteLine(count);
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

  int pay; cin >> pay;

  int cntCharge = 0, charge = 1000 - pay;
  int coins[] = {500, 100, 50, 10, 5, 1};
  for (int coin : coins) {
    if (!charge) break;

    cntCharge += charge / coin;
    charge %= coin;
  }
  cout << cntCharge << "\n";

  return 0;
}
```
