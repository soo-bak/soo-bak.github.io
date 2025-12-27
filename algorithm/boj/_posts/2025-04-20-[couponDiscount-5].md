---
layout: single
title: "[백준 10179] 쿠폰 (C#, C++) - soo:bak"
date: "2025-04-20 04:01:00 +0900"
description: 입력된 금액에 대해 20% 할인된 값을 소수점 둘째 자리까지 출력하는 백준 10179번 쿠폰 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10179
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 10179, 백준 10179번, BOJ 10179, couponDiscount, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10179번 - 쿠폰](https://www.acmicpc.net/problem/10179)

## 설명
**입력된 금액에 대해** `20%` **할인을 적용한 뒤, 소수점 둘째 자리까지 반올림하여 출력하는 문제입니다.**
<br>

- 테스트케이스 수가 주어지고, 그만큼의 실수가 입력됩니다.
- 각 가격에 대해 `80%`**의 금액만 지불**하는 셈이므로, `입력값 * 0.8`을 계산합니다.
- 출력은 항상 **소수점 둘째 자리**까지 고정되어야 합니다.


## 접근법

1. 먼저 테스트케이스 개수를 입력받습니다.
2. 각 테스트케이스마다 실수를 하나 입력받습니다.
3. 입력받은 값에 `0.8`을 곱하여 할인된 금액을 계산합니다.
4. `$` 기호를 붙여 **소수점 둘째 자리까지** 출력합니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int cases = int.Parse(Console.ReadLine());
    while (cases-- > 0) {
      double price = double.Parse(Console.ReadLine());
      Console.WriteLine($"${(price * 0.8):F2}");
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
    double price; cin >> price;
    cout.setf(ios::fixed); cout.precision(2);
    cout << "$" << 0.8 * price << "\n";
  }

  return 0;
}
```
