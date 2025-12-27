---
layout: single
title: "[백준 18301] Rats (C#, C++) - soo:bak"
date: "2025-11-22 03:09:00 +0900"
description: 표본재포획법을 이용한 총 개체 수 추정 공식을 계산하는 백준 18301번 Rats 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 18301
  - C#
  - C++
  - 알고리즘
keywords: "백준 18301, 백준 18301번, BOJ 18301, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18301번 - Rats](https://www.acmicpc.net/problem/18301)

## 설명

쥐의 총 개체 수를 추정하는 문제입니다. 첫째 날에 `n₁`마리를 포획하여 표시한 후 방류하고, 둘째 날에 다시 `n₂`마리를 포획합니다. 이때 둘째 날 포획한 개체 중 첫날 표시가 있는 개체 수가 `n₁₂`마리입니다.

이 세 값을 이용하여 전체 쥐의 개체 수를 추정해야 합니다.

<br>

## 접근법

주어진 공식 `N = ⌊(n₁ + 1)(n₂ + 1) / (n₁₂ + 1) - 1⌋`을 계산하여 총 개체 수를 구합니다.

모든 입력 값이 10,000 이하이므로 곱셈 결과가 약 10⁸을 넘지 않아 64비트 정수로 충분히 처리 가능합니다.

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
      var n1 = long.Parse(tokens[0]);
      var n2 = long.Parse(tokens[1]);
      var n12 = long.Parse(tokens[2]);

      var numerator = (n1 + 1) * (n2 + 1);
      var denominator = n12 + 1;
      var result = numerator / denominator - 1;

      Console.WriteLine(result);
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

  ll n1, n2, n12; cin >> n1 >> n2 >> n12;

  ll numerator = (n1 + 1) * (n2 + 1);
  ll denominator = n12 + 1;

  cout << (numerator / denominator - 1) << "\n";

  return 0;
}
```

