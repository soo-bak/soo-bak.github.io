---
layout: single
title: "[백준 11368] A Serious Reading Problem (C#, C++) - soo:bak"
date: "2025-12-19 22:47:00 +0900"
description: C^(W×L×P) 개의 책이 존재한다는 사실로 큰 수 거듭제곱을 계산하는 문제
---

## 문제 링크
[11368번 - A Serious Reading Problem](https://www.acmicpc.net/problem/11368)

## 설명
문자 종류 c, 한 줄 글자 수 w, 한 페이지 줄 수 l, 한 권 페이지 수 p가 주어질 때, 가능한 책의 수를 구하는 문제입니다.

한 책의 총 글자 수는 w × l × p이고, 각 위치에 c개의 문자 중 하나를 쓰므로 c의 (w × l × p)제곱이 됩니다.

<br>

## 접근법
지수를 계산한 뒤 큰 정수로 거듭제곱을 수행합니다.

입력 크기가 작아 선형 반복으로 충분합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Numerics;

class Program {
  static void Main() {
    while (true) {
      var parts = Console.ReadLine()!.Split(' ', StringSplitOptions.RemoveEmptyEntries);
      var c = int.Parse(parts[0]);
      var w = int.Parse(parts[1]);
      var l = int.Parse(parts[2]);
      var p = int.Parse(parts[3]);

      if (c == 0 && w == 0 && l == 0 && p == 0) break;

      var exp = w * l * p;
      var res = BigInteger.One;
      for (var i = 0; i < exp; i++)
        res *= c;

      Console.WriteLine(res);
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

  ll c, w, l, p;
  while (cin >> c >> w >> l >> p) {
    if (c == 0 && w == 0 && l == 0 && p == 0) break;

    ll exp = w * l * p;
    ll res = 1;
    for (ll i = 0; i < exp; i++)
      res *= c;

    cout << res << "\n";
  }

  return 0;
}
```
