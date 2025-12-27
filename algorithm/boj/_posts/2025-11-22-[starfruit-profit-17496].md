---
layout: single
title: "[백준 17496] 스타후르츠 (C#, C++) - soo:bak"
date: "2025-11-22 03:00:00 +0900"
description: 여름 기간 N일 동안 길이 T의 성장 주기를 가지는 스타후르츠 수확 횟수를 계산해 총 수익을 구하는 백준 17496번 스타후르츠 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17496
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 17496, 백준 17496번, BOJ 17496, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17496번 - 스타후르츠](https://www.acmicpc.net/problem/17496)

## 설명

여름이 `N`일 동안 지속됩니다. 스타후르츠를 심으면 `T`일 후에 수확할 수 있으며, 수확한 당일에 다시 심을 수 있습니다.

밭에는 총 `C`개의 칸이 있고, 각 칸마다 스타후르츠를 하나씩 심을 수 있습니다.

스타후르츠 한 개의 가격이 `P`원일 때, 여름 동안 벌 수 있는 최대 수익을 구해야 합니다.

<br>

## 접근법

1일차에 심으면 `1 + T`일차에 첫 수확을 할 수 있습니다.

수확한 당일에 다시 심을 수 있으므로, `1 + T`일차에 수확 후 바로 심으면 `1 + 2T`일차에 두 번째 수확을, `1 + 3T`일차에 세 번째 수확을 할 수 있습니다.

따라서, 수확 시점은 `1 + T`, `1 + 2T`, `1 + 3T`, `...` 형태가 됩니다.

여름이 `N`일까지이므로, 마지막 수확은 `N`일 이전이어야 합니다. 따라서 `1 + kT ≤ N`을 만족하는 최대 정수 `k`를 구하면 되고, 이를 정리하면 `k ≤ (N - 1) / T`가 됩니다.

따라서 수확 횟수는 `⌊(N - 1) / T⌋`번입니다.

한 번 수확할 때마다 `C`개의 칸에서 각각 하나씩 총 `C`개를 수확하고, 각 개당 `P`원이므로, 총 수익은 `⌊(N - 1) / T⌋ × C × P`입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var N = long.Parse(tokens[0]);
      var T = long.Parse(tokens[1]);
      var C = long.Parse(tokens[2]);
      var P = long.Parse(tokens[3]);

      var harvests = (N - 1) / T;

      Console.WriteLine(harvests * C * P);
    }
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

  ll N, T, C, P; cin >> N >> T >> C >> P;

  ll harvests = (N - 1) / T;

  cout << harvests * C * P << "\n";

  return 0;
}
```

