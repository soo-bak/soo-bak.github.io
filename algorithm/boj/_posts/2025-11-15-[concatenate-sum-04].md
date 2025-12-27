---
layout: single
title: "[백준 10824] 네 수 (C#, C++) - soo:bak"
date: "2025-11-15 00:30:00 +0900"
description: 두 쌍의 자연수를 문자열로 이어 붙여 합을 구하는 백준 10824번 네 수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10824
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 문자열
  - arithmetic
keywords: "백준 10824, 백준 10824번, BOJ 10824, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10824번 - 네 수](https://www.acmicpc.net/problem/10824)

## 설명

네 자연수 `A`, `B`, `C`, `D`가 주어질 때, `A`와 `B`를 이어 붙인 수와 `C`와 `D`를 이어 붙인 수의 합을 구하는 문제입니다.<br>

예를 들어 `A = 10`, `B = 20`, `C = 30`, `D = 40`이면, `1020 + 3040 = 4060`을 출력합니다.<br>

이어 붙인 수는 매우 커질 수 있으므로 `long long` 범위로 처리해야 합니다.<br>

<br>

## 접근법

문자열 연결을 사용하여 해결합니다.

네 개의 숫자를 문자열로 입력받습니다. `A`와 `B`를 이어 붙여 하나의 문자열로 만든 뒤 정수로 변환하고, `C`와 `D`도 같은 방식으로 처리합니다.

<br>
두 정수의 합을 계산하여 출력합니다. C#에서는 문자열 보간 `$"{}{}"` 방식으로 이어 붙인 뒤 `long.Parse`로 변환하고, C++에서는 문자열 연결 후 `stoll` 함수로 변환합니다.

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
      var a = tokens[0];
      var b = tokens[1];
      var c = tokens[2];
      var d = tokens[3];

      var first = long.Parse($"{a}{b}");
      var second = long.Parse($"{c}{d}");
      Console.WriteLine(first + second);
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

  string a, b, c, d; cin >> a >> b >> c >> d;
  ll x = stoll(a + b);
  ll y = stoll(c + d);
  cout << x + y << "\n";

  return 0;
}
```

