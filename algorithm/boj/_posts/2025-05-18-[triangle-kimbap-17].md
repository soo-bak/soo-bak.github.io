---
layout: single
title: "[백준 2783] 삼각 김밥 (C#, C++) - soo:bak"
date: "2025-05-18 02:15:48 +0900"
description: 1000그램당 단가를 비교해 최저 가격을 계산하는 백준 2783번 삼각 김밥 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2783
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 2783, 백준 2783번, BOJ 2783, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2783번 - 삼각 김밥](https://www.acmicpc.net/problem/2783)

## 설명

**여러 편의점에서 판매하는 삼각 김밥의 가격 정보를 바탕으로,** `1000그램`**을 기준으로 했을 때 가장 저렴한 단가를 계산하는 문제입니다.**

각 편의점은 `삼각 김밥의 무게(그램)`와 `해당 가격`을 함께 표시하고 있으며,

이를 기반으로 `1,000g` 단위 가격을 환산해 가장 저렴한 값을 구해야 합니다.

<br>

## 접근법

- 가장 먼저, 가격 정보를 입력받아 `그램당 가격`을 계산하고, 이를 바탕으로 `1000그램당 가격`을 초기 기준값으로 설정합니다.
- 이후 다른 편의점들의 가격 정보를 입력받으며 각 편의점마다 다음을 수행합니다:
  - 입력된 가격과 무게로부터 `1000그램당 가격`을 계산합니다.
  - `현재까지의 최저 가격`과 비교하여 더 저렴한 경우 갱신합니다.

가격 계산 공식은 다음과 같습니다:

$$
\text{가격} = \frac{X}{Y} \times 1000
$$

정답 출력 시 소수 둘째 자리까지 정확하게 출력해야 하며,

입력 범위가 작아 단순 비교만으로도 충분히 처리할 수 있습니다.

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var baseInput = Console.ReadLine().Split();
    double p = double.Parse(baseInput[0]);
    double g = double.Parse(baseInput[1]);

    double minPrice = p / g * 1000;

    int n = int.Parse(Console.ReadLine());
    for (int i = 0; i < n; i++) {
      var parts = Console.ReadLine().Split();
      double pi = double.Parse(parts[0]);
      double gi = double.Parse(parts[1]);
      minPrice = Math.Min(minPrice, pi / gi * 1000);
    }

    Console.WriteLine($"{minPrice:F2}");
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

  double p, g; cin >> p >> g;
  double minPrice = p / g * 1000;

  int n; cin >> n;
  while (n--) {
    cin >> p >> g;
    minPrice = min(minPrice, p / g * 1000);
  }
  cout << fixed << setprecision(2) << minPrice << "\n";

  return 0;
}
```
