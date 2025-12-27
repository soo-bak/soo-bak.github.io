---
layout: single
title: "[백준 23037] 5의 수난 (C#, C++) - soo:bak"
date: "2025-11-21 23:36:00 +0900"
description: 다섯 자리 수의 각 자릿수를 5제곱해 합산하는 백준 23037번 5의 수난 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23037
  - C#
  - C++
  - 알고리즘
keywords: "백준 23037, 백준 23037번, BOJ 23037, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23037번 - 5의 수난](https://www.acmicpc.net/problem/23037)

## 설명

다섯 자리 양의 정수가 주어지면, 각 자릿수를 `5`제곱하여 모두 더한 값을 출력하는 문제입니다.<br>

<br>

## 접근법

입력을 문자열로 받아 각 자릿수를 순회하며 `5`제곱 값을 누적합니다. 예를 들어 입력이 `10234`라면 `1^5 + 0^5 + 2^5 + 3^5 + 4^5 = 1 + 0 + 32 + 243 + 1024 = 1300`입니다.<br>

각 자릿수를 정수로 변환한 후 `5`제곱하여 합산하고 최종 결과를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var digits = Console.ReadLine()!;
      var sum = 0L;

      foreach (var ch in digits) {
        var d = ch - '0';
        sum += (long)Math.Pow(d, 5);
      }

      Console.WriteLine(sum);
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

  string digits; cin >> digits;

  ll sum = 0;
  for (char ch : digits) {
    int d = ch - '0';
    sum += (ll)pow(d, 5);
  }

  cout << sum << "\n";

  return 0;
}
```

