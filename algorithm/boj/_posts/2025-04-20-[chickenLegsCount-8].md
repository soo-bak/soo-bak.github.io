---
layout: single
title: "[백준 11006] 남욱이의 닭장 (C#, C++) - soo:bak"
date: "2025-04-20 03:08:00 +0900"
description: 닭과 닭다리의 총합이 주어졌을 때 두 다리를 가진 닭과 한 다리만 있는 닭의 수를 계산하는 백준 11006번 남욱이의 닭장 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11006
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 11006, 백준 11006번, BOJ 11006, chickenLegsCount, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11006번 - 남욱이의 닭장](https://www.acmicpc.net/problem/11006)

## 설명
**닭의 수와 다리의 총합이 주어졌을 때, 두 다리를 가진 정상 닭과 한 다리만 있는 닭의 수를 구하는 문제입니다.**
<br>

- `다리의 합`과 `닭의 수`가 주어집니다.
- 모든 닭은 한 마리당 다리를 `1`개 또는 `2`개 가질 수 있습니다.
- 두 가지 조건을 만족하는 닭의 수를 계산해야 합니다:
  - `총 닭 수` = `두 다리 닭 수` + `한 다리 닭 수`
  - `총 다리 수` = `2 * 두 다리 닭 수` + `1 * 한 다리 닭 수`

## 접근법

1. 입력으로 주어지는 다리의 수와 닭의 수를 변수로 저장합니다.
2. 두 변수에 대해 다음 수식을 유도합니다:
   - `한 다리 닭 수` : $$ 2 \times \text{닭 수} - \text{다리 수} $$
   - `두 다리 닭 수` : $$ \text{닭 수} - \text{한 다리 닭 수} $$
3. 위 수식을 그대로 계산하여 출력합니다.

- `O(1)` 계산만 수행됩니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var input = Console.ReadLine().Split();
      int legSum = int.Parse(input[0]);
      int chicken = int.Parse(input[1]);

      int oddLeg = 2 * chicken - legSum;
      Console.WriteLine($"{oddLeg} {chicken - oddLeg}");
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

  int t; cin >> t;
  while (t--) {
    int legSum, cntChicken; cin >> legSum >> cntChicken;
    int oddLeg = 2 * cntChicken - legSum;
    cout << oddLeg << " " << cntChicken - oddLeg << "\n";
  }

  return 0;
}
```
