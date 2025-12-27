---
layout: single
title: "[백준 2480] 주사위 세개 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 세 개의 주사위 눈을 비교해 같은 눈의 개수에 따라 상금을 계산하는 백준 2480번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2480
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
  - 케이스분류
keywords: "백준 2480, 백준 2480번, BOJ 2480, dicePrizeThree, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2480번 - 주사위 세개](https://www.acmicpc.net/problem/2480)

## 설명

세 개의 주사위를 던진 결과가 주어지는 상황에서, 세 개의 주사위 눈(1~6)이 주어질 때, 같은 눈이 나온 개수에 따라 상금을 계산하여 출력하는 문제입니다.

상금 규칙은 다음과 같습니다:
- 세 눈이 모두 같은 경우: 10,000 + (같은 눈) × 1,000원
- 두 눈만 같은 경우: 1,000 + (같은 눈) × 100원
- 세 눈이 모두 다른 경우: (가장 큰 눈) × 100원

<br>

## 접근법

세 개의 주사위 눈의 조합을 확인하여 어떤 규칙에 해당하는지 판별합니다.

세 개가 모두 같은지, 두 개가 같은지, 모두 다른지를 순서대로 확인한 후 해당하는 상금 공식을 적용합니다.

두 개만 같은 경우는 어느 두 개가 같은지 확인하여 그 값으로 상금을 계산하고, 모두 다른 경우는 세 값 중 최댓값을 찾아 상금을 계산합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var dice = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var a = dice[0];
      var b = dice[1];
      var c = dice[2];

      int prize;
      if (a == b && b == c) prize = 10000 + a * 1000;
      else if (a == b || a == c) prize = 1000 + a * 100;
      else if (b == c) prize = 1000 + b * 100;
      else prize = Math.Max(a, Math.Max(b, c)) * 100;

      Console.WriteLine(prize);
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

  int a, b, c; cin >> a >> b >> c;

  int prize;
  if (a == b && b == c) prize = 10000 + a * 1000;
  else if (a == b || a == c) prize = 1000 + a * 100;
  else if (b == c) prize = 1000 + b * 100;
  else prize = max({a, b, c}) * 100;

  cout << prize << "\n";
  
  return 0;
}
```

