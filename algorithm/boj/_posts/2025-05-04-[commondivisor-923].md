---
layout: single
title: "[백준 5618] 공약수 (C#, C++) - soo:bak"
date: "2025-05-04 09:23:00 +0900"
description: 주어진 2개 또는 3개의 자연수에 대해 모든 공약수를 계산하여 출력하는 백준 5618번 공약수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5618
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
  - 정수론
keywords: "백준 5618, 백준 5618번, BOJ 5618, commondivisor, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5618번 - 공약수](https://www.acmicpc.net/problem/5618)

## 설명
여러 개의 자연수가 주어졌을 때, **이 수들의 공약수를 모두 구해 오름차순으로 출력하는 문제**입니다.

입력으로는 `2`개 또는 `3`개의 자연수가 주어지며, 모든 수를 나누는 양의 정수(공약수)를 찾아 출력합니다.

<br>

## 접근법

- 먼저 수의 개수 `n`을 입력받고, `n`개의 자연수를 저장합니다.
- 이 모든 수들의 최대공약수(GCD)를 먼저 구합니다.
- 그 GCD의 모든 약수를 구하면, 해당 수들의 공약수를 얻을 수 있습니다.
- `1`부터 `GCD`까지의 수 중에서 나누어떨어지는 값들을 출력합니다.

> 참고 : [GCD(최대공약수)와 유클리드 호제법의 원리 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static int GCD(int a, int b) {
    return b == 0 ? a : GCD(b, a % b);
  }

  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var nums = Console.ReadLine().Split().Select(int.Parse).ToArray();

    int g = nums[0];
    for (int i = 1; i < n; i++)
      g = GCD(g, nums[i]);

    for (int i = 1; i <= g; i++)
      if (g % i == 0)
        Console.WriteLine(i);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int gcd(int a, int b) {
  return b ? gcd(b, a % b) : a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int g = a[0];
  for (int i = 1; i < n; i++)
    g = gcd(g, a[i]);

  for (int i = 1; i <= g / 2; i++)
    if (g % i == 0) cout << i << "\n";
  cout << g << "\n";

  return 0;
}
```
