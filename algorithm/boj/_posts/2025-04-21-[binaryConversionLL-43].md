---
layout: single
title: "[백준 10829] 이진수 변환 (C#, C++) - soo:bak"
date: "2025-04-21 00:03:00 +0900"
description: long long 정수를 이진수로 변환하여 앞에서부터 출력하는 백준 10829번 이진수 변환 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10829번 - 이진수 변환](https://www.acmicpc.net/problem/10829)

## 설명
**10진수로 주어진 매우 큰 정수를 2진수(이진수)로 변환하여 출력하는 문제입니다.**
<br>

- 입력으로 하나의 정수가 주어지며, 이 정수는 $$(1 \leq N \leq 100,000,000,000,000)$$ 의 범위를 가집니다.
- 해당 수를 2진수로 바꾸어, **앞에서부터 차례대로 출력**해야 합니다.


## 접근법

- 주어진 수를 `2`로 계속 나누어가며 나머지를 앞에서부터 기록하면 이진수 표현이 완성됩니다.


## Code

### C#
```csharp
using System;
using System.Numerics;

class Program {
  static void Main() {
    BigInteger num = BigInteger.Parse(Console.ReadLine());
    Console.WriteLine(Convert.ToString((long)num, 2));
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

  ll num; cin >> num;

  if (num == 0) {
    cout << "0\n";
    return 0;
  }

  string binary;
  while (num > 0) {
    binary = char(num % 2 + '0') + binary;
    num /= 2;
  }

  cout << binary << "\n";

  return 0;
}
```
