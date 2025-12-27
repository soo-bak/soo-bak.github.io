---
layout: single
title: "[백준 23825] SASA 모형을 만들어보자 (C#, C++) - soo:bak"
date: "2025-11-23 02:33:00 +0900"
description: S 2개와 A 2개로 이루어진 SASA 모형을 최대 몇 개 만들 수 있는지 계산하는 백준 23825번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23825
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 23825, 백준 23825번, BOJ 23825, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23825번 - SASA 모형을 만들어보자](https://www.acmicpc.net/problem/23825)

## 설명

S 블록 `N`개와 A 블록 `M`개가 주어집니다. SASA 모형 하나를 만들려면 S 블록 2개와 A 블록 2개가 필요합니다.

이때 최대 몇 개의 SASA 모형을 만들 수 있는지 구하는 문제입니다.

<br>

## 접근법

S 블록으로는 최대 `N / 2`개의 모형을 만들 수 있고, A 블록으로는 최대 `M / 2`개의 모형을 만들 수 있습니다.

두 종류의 블록이 모두 필요하므로 최종 개수는 두 값 중 작은 값으로 제한됩니다.

따라서 `min(N / 2, M / 2)`를 계산하면 됩니다.

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
      var n = long.Parse(tokens[0]);
      var m = long.Parse(tokens[1]);

      Console.WriteLine(Math.Min(n / 2, m / 2));
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

  ll n, m; cin >> n >> m;

  cout << min(n / 2, m / 2) << "\n";

  return 0;
}
```

