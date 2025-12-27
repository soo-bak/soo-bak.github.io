---
layout: single
title: "[백준 5347] LCM (C#, C++) - soo:bak"
date: "2025-04-19 01:12:43 +0900"
description: 두 정수의 최소공배수를 계산하는 수학적 알고리즘을 구현한 백준 5347번 LCM 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5347
  - C#
  - C++
  - 알고리즘
keywords: "백준 5347, 백준 5347번, BOJ 5347, lcmMultiple, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5347번 - LCM](https://www.acmicpc.net/problem/5347)

## 설명
**여러 쌍의 정수가 주어졌을 때, 각 쌍의 최소공배수(LCM)를 구하는 문제입니다.**<br>
<br>

- 입력으로 두 정수 `a`, `b`가 주어지고, 각각의 쌍에 대해 `LCM(a, b)` 값을 구해야 합니다.<br>
- 단, 정수의 범위가 크기 때문에 오버플로를 주의하여, 적절한 크기의 자료형을 사용해야 합니다.<br>
- 문제의 핵심은 **최대공약수(GCD)**를 이용하여 **최소공배수(LCM)**를 빠르게 계산하는 것입니다.<br>

### GCD와 LCM의 관계
- **최대공약수(Greatest Common Divisor, GCD)**는 두 수가 공통으로 가지는 가장 큰 약수입니다.
- **최소공배수(Least Common Multiple, LCM)**는 두 수의 공통 배수 중 가장 작은 값입니다.
- 두 수 `a`, `b`에 대해 다음과 같은 관계가 있습니다:

\[
\text{LCM}(a, b) = \frac{a \times b}{\text{GCD}(a, b)}
\]

- `GCD`는 `유클리드 호제법`을 사용하여 빠르게 구할 수 있습니다:

\[
\text{GCD}(a, b) = \text{GCD}(b, a \bmod b)
\]

### 접근법
- 테스트케이스 수를 입력받고, 각 쌍의 두 정수 `a`, `b`를 입력받습니다.<br>
- 유클리드 호제법으로 `GCD`를 계산하고, 위 공식을 통해 `LCM`을 출력합니다.<br>

> 참고 : [GCD(최대공약수)와 유클리드 호제법의 원리 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

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
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var input = Console.ReadLine().Split();
      long a = long.Parse(input[0]);
      long b = long.Parse(input[1]);

      long lcm = a * b / Gcd(a, b);
      Console.WriteLine(lcm);
    }
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

  int cntCases; cin >> cntCases;
  while (cntCases--) {
    ll a, b; cin >> a >> b;
    ll lcm = a * b / getGcd(a, b);
    cout << lcm << "\n";
  }

  return 0;
}
```
