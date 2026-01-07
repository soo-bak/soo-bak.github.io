---
layout: single
title: "[백준 15296] Sum Squared Digits Function (C#, C++) - soo:bak"
date: "2026-01-07 21:40:00 +0900"
description: "백준 15296번 C#, C++ 풀이 - 주어진 진법에서 수를 표현했을 때 각 자릿수 제곱의 합을 구하는 SSD 함수 값을 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 15296
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 15296, 백준 15296번, BOJ 15296, Sum Squared Digits Function, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15296번 - Sum Squared Digits Function](https://www.acmicpc.net/problem/15296)

## 설명
진법 b에서 양의 정수 n의 각 자릿수를 제곱하여 더한 값을 SSD(b, n)이라 합니다. P개의 테스트 케이스에 대해 데이터셋 번호 K와 함께 SSD 값을 출력하는 문제입니다.

<br>

## 접근법
먼저 진법 b로 n을 나누며 나머지를 자릿수로 얻습니다.

다음으로 각 나머지를 제곱하여 누적 합을 구합니다. 몫이 0이 될 때까지 반복합니다.

이후 데이터셋 번호 K와 합을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var p = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    for (var _ = 0; _ < p; _++) {
      var parts = Console.ReadLine()!.Split();
      var k = int.Parse(parts[0]);
      var b = int.Parse(parts[1]);
      var n = uint.Parse(parts[2]);

      ulong sum = 0;
      uint x = n;
      while (x > 0) {
        uint d = x % (uint)b;
        sum += (ulong)d * d;
        x /= (uint)b;
      }

      sb.Append(k).Append(' ').Append(sum).Append('\n');
    }
    Console.Write(sb);
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

  int p; cin >> p;
  while (p--) {
    int k, b, n; cin >> k >> b >> n;
    ll sum = 0;
    int x = n;
    while (x > 0) {
      int d = x % b;
      sum += 1ULL * d * d;
      x /= b;
    }
    cout << k << ' ' << sum << "\n";
  }

  return 0;
}
```
