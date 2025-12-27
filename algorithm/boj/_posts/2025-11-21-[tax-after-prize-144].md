---
layout: single
title: "[백준 20492] 세금 (C#, C++) - soo:bak"
date: "2025-11-21 23:49:00 +0900"
description: 상금에서 22%를 뗀 경우와 20%만 과세했을 때의 실수령액을 계산하는 백준 20492번 세금 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 20492
  - C#
  - C++
  - 알고리즘
keywords: "백준 20492, 백준 20492번, BOJ 20492, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20492번 - 세금](https://www.acmicpc.net/problem/20492)

## 설명

상금 `N`원이 주어집니다. `N`은 `1000`의 배수입니다.<br>

두 가지 세금 납부 방식에 따른 실수령액을 각각 계산하여 출력하는 문제입니다.<br>

<br>

## 접근법

첫 번째 방식은 전체 상금의 `22%`를 세금으로 납부하므로 실수령액은 `N × 0.78`입니다. 정수 연산으로는 `N × 78 / 100`으로 계산합니다.<br>

두 번째 방식은 상금의 `80%`를 필요 경비로 인정받아 나머지 `20%`에만 `22%`를 과세합니다. 실수령액은 `N × (1 - 0.2 × 0.22) = N × 0.956`입니다. 정수 연산으로는 `N × 956 / 1000`으로 계산합니다.<br>

예를 들어 상금이 `10000`원이면 첫 번째 방식은 `7800`원, 두 번째 방식은 `9560`원을 받습니다. 두 값을 공백으로 구분하여 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = long.Parse(Console.ReadLine()!);

      var first = n * 78 / 100;
      var second = n * 956 / 1000;

      Console.WriteLine($"{first} {second}");
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

  ll n; cin >> n;

  ll first = n * 78 / 100;
  ll second = n * 956 / 1000;

  cout << first << " " << second << "\n";

  return 0;
}
```

