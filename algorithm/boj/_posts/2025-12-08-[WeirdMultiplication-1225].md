---
layout: single
title: "[백준 1225] 이상한 곱셈 (C#, C++) - soo:bak"
date: "2025-12-08 04:30:00 +0900"
description: 두 수의 각 자리를 모두 곱해 더한 값을 구하는 백준 1225번 이상한 곱셈 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1225번 - 이상한 곱셈](https://www.acmicpc.net/problem/1225)

## 설명
두 수의 각 자릿수끼리 모두 곱한 값을 더하는 문제입니다. 예를 들어 123과 45라면 1×4 + 1×5 + 2×4 + 2×5 + 3×4 + 3×5를 계산합니다.

<br>

## 접근법
모든 자릿수 쌍을 곱해서 더하는 것은 결국 첫 번째 수의 자릿수 합과 두 번째 수의 자릿수 합을 곱한 것과 같습니다. 123과 45의 경우 (1+2+3) × (4+5) = 6 × 9 = 54입니다. 각 수를 문자열로 읽어 자릿수 합을 구한 뒤 곱하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = parts[0];
    var b = parts[1];
    var sumA = 0L;
    var sumB = 0L;
    foreach (var ch in a) sumA += ch - '0';
    foreach (var ch in b) sumB += ch - '0';
    Console.WriteLine(sumA * sumB);
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

  string a, b; cin >> a >> b;
  ll sa = 0, sb = 0;
  for (char c : a) sa += c - '0';
  for (char c : b) sb += c - '0';
  cout << sa * sb << "\n";

  return 0;
}
```
