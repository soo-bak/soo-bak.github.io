---
layout: single
title: "[백준 24830] Broken Calculator (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 이전 결과를 이용해 연산 규칙이 바뀐 계산기의 결과를 순서대로 출력하는 문제
---

## 문제 링크
[24830번 - Broken Calculator](https://www.acmicpc.net/problem/24830)

## 설명
이상한 규칙으로 동작하는 계산기에 대해 각 명령의 결과를 출력하는 문제입니다.

<br>

## 접근법
이전 결과를 저장해두고, 각 연산마다 문제의 규칙대로 새 값을 계산합니다. 덧셈은 두 수의 합에서 이전 결과를 빼고, 뺄셈은 두 수의 차에 이전 결과를 곱합니다.

곱셈은 두 수의 곱을 제곱하고, 나눗셈은 첫 번째 수가 짝수면 절반을, 홀수면 1을 더한 뒤 절반을 취합니다. 모든 연산 결과를 저장한 후 순서대로 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    long prev = 1;
    var res = new List<long>();

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var a = long.Parse(parts[0]);
      var op = parts[1];
      var b = long.Parse(parts[2]);

      if (op == "+") prev = a + b - prev;
      else if (op == "-") prev = (a - b) * prev;
      else if (op == "*") {
        prev = a * b;
        prev *= prev;
      } else if (op == "/") {
        if (a % 2 == 0) prev = a / 2;
        else prev = (a + 1) / 2;
      }

      res.Add(prev);
    }

    foreach (var r in res)
      Console.WriteLine(r);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<ll> vll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  ll prev = 1;
  vll res;

  for (int i = 0; i < n; i++) {
    ll a, b; char op; cin >> a >> op >> b;

    if (op == '+') prev = a + b - prev;
    else if (op == '-') prev = (a - b) * prev;
    else if (op == '*') {
      prev = a * b;
      prev *= prev;
    } else if (op == '/') {
      if (a % 2 == 0) prev = a / 2;
      else prev = (a + 1) / 2;
    }

    res.push_back(prev);
  }

  for (ll r : res)
    cout << r << "\n";

  return 0;
}
```
