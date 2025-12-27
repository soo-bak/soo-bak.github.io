---
layout: single
title: "[백준 1735] 분수 합 (C#, C++) - soo:bak"
date: "2025-04-19 01:52:25 +0900"
description: 두 분수를 더한 뒤 기약분수로 변환하는 수학 기반 구현 문제인 백준 1735번 분수 합 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1735
  - C#
  - C++
  - 알고리즘
keywords: "백준 1735, 백준 1735번, BOJ 1735, fractionSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1735번 - 분수 합](https://www.acmicpc.net/problem/1735)

## 설명
**두 분수를 더한 뒤, 기약분수 형태로 출력하는 수학적 구현 문제**입니다.<br>
<br>

- 입력으로 두 개의 분수가 주어집니다 (`a/b`, `c/d`).<br>
- 두 분수를 더한 값을 **기약분수(더 이상 약분할 수 없는 형태)**로 출력해야 합니다.<br>
- 기약분수로 만들기 위해서는 **분자와 분모의 최대공약수(GCD)**를 계산한 뒤 **약분**해야 합니다.<br>

> 참고 : [GCD(최대공약수)와 유클리드 호제법의 원리 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

> 참고 : [기약 분수(irreducible fraction)의 알고리듬적 접근 - soo:bak](https://soo-bak.github.io/algorithm/theory/irreducible-fraction/)

### 접근법
- 먼저 분수의 합을 계산하기 위해 통분을 수행합니다:<br>

$$
\frac{a}{b} + \frac{c}{d} = \frac{a \cdot d + c \cdot b}{b \cdot d}
$$

- 이후 `분자`와 `분모`의 최대공약수(GCD)를 계산해 각각 나누어 줍니다.<br>
- 출력은 `기약분자의 값`과 `기약분모의 값`을 공백으로 구분하여 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

class Program {
  static long Gcd(long a, long b) {
    return b == 0 ? a : Gcd(b, a % b);
  }

  static void Main() {
    var f1 = Array.ConvertAll(Console.ReadLine().Split(), long.Parse);
    var f2 = Array.ConvertAll(Console.ReadLine().Split(), long.Parse);

    long numerator = f1[0] * f2[1] + f2[0] * f1[1];
    long denominator = f1[1] * f2[1];
    long gcd = Gcd(numerator, denominator);

    Console.WriteLine($"{numerator / gcd} {denominator / gcd}");
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;

ll getGcd(ll a, ll b) {
  if (b == 0) return a;
  return getGcd(b, a % b);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll nmr1, dnm1; cin >> nmr1 >> dnm1;
  ll nmr2, dnm2; cin >> nmr2 >> dnm2;

  ll nmrA = nmr1 * dnm2 + nmr2 * dnm1;
  ll dnmA = dnm1 * dnm2;
  ll gcd = getGcd(nmrA, dnmA);

  cout << nmrA / gcd << " " << dnmA / gcd << "\n";

  return 0;
}
```
