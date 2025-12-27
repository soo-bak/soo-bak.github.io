---
layout: single
title: "[백준 1837] 암호제작 (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 큰 수 문자열 P에 대해 K 미만의 소수로 나누어 떨어지는지 검사해 GOOD/BAD를 판정하는 백준 1837번 암호제작 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1837
  - C#
  - C++
  - 알고리즘
keywords: "백준 1837, 백준 1837번, BOJ 1837, PrimePassword, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1837번 - 암호제작](https://www.acmicpc.net/problem/1837)

## 설명
두 소수의 곱으로 이루어진 암호가 안전한지 판별하는 문제입니다.

<br>

## 접근법
먼저 k 미만의 소수를 에라토스테네스의 체로 구합니다.

각 소수에 대해 문자열 p를 자릿수 순회하며 나머지를 계산합니다.

어떤 소수로든 나누어떨어지면 BAD와 해당 소수를 출력하고, 끝까지 없으면 GOOD을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var num = line[0];
    var k = int.Parse(line[1]);

    var isComposite = new bool[k];
    for (var i = 2; i * i < k; i++) {
      if (isComposite[i]) continue;
      for (var j = i * i; j < k; j += i)
        isComposite[j] = true;
    }

    foreach (var p in PrimesUpTo(k, isComposite)) {
      var rem = 0;
      for (var i = 0; i < num.Length; i++)
        rem = (rem * 10 + (num[i] - '0')) % p;
      if (rem == 0) {
        Console.WriteLine($"BAD {p}");
        return;
      }
    }
    Console.WriteLine("GOOD");
  }

  static System.Collections.Generic.IEnumerable<int> PrimesUpTo(int k, bool[] isComposite) {
    for (var i = 2; i < k; i++)
      if (!isComposite[i]) yield return i;
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string num; int k;
  if (!(cin >> num >> k)) return 0;

  vb comp(k, false);
  for (int i = 2; i * i < k; i++)
    if (!comp[i])
      for (int j = i * i; j < k; j += i)
        comp[j] = true;

  for (int p = 2; p < k; p++) {
    if (comp[p]) continue;
    int rem = 0;
    for (char c : num)
      rem = (rem * 10 + (c - '0')) % p;
    if (rem == 0) {
      cout << "BAD " << p << "\n";
      return 0;
    }
  }
  cout << "GOOD\n";

  return 0;
}
```
