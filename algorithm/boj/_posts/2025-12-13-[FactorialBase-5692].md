---
layout: single
title: "[백준 5692] 팩토리얼 진법 (C#, C++) - soo:bak"
date: "2025-12-13 22:20:00 +0900"
description: 각 자리수를 (위치)!와 곱해 합산해 10진값을 구하는 백준 5692번 팩토리얼 진법 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 5692
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 5692, 백준 5692번, BOJ 5692, FactorialBase, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5692번 - 팩토리얼 진법](https://www.acmicpc.net/problem/5692)

## 설명
팩토리얼 진법으로 표현된 수를 10진수로 변환하는 문제입니다.

0이 입력되면 종료합니다.

<br>

## 접근법
10진법에서 각 자리가 10의 거듭제곱을 자릿값으로 갖듯이, 팩토리얼 진법에서는 팩토리얼을 자릿값으로 갖습니다.

오른쪽부터 첫 번째 자리는 1!, 두 번째 자리는 2!, 세 번째 자리는 3!입니다.

예를 들어 341을 변환하면 3×3! + 4×2! + 1×1! = 18 + 8 + 1 = 27이 됩니다.

따라서 문자열을 순회하며 각 자릿수에 해당 자릿값을 곱해 합산하면 10진수 값을 얻을 수 있습니다.

<br>

## Code

### C#
```csharp
using System;
using System.IO;

class Program {
  static void Main() {
    var reader = new StreamReader(Console.OpenStandardInput());
    var writer = new StreamWriter(Console.OpenStandardOutput());

    var fact = new[] { 0, 1, 2, 6, 24, 120 };
    string line;
    while ((line = reader.ReadLine()) != null && line != "0") {
      var len = line.Length;
      var sum = 0;
      for (var i = 0; i < len; i++) {
        var digit = line[i] - '0';
        sum += digit * fact[len - i];
      }
      writer.WriteLine(sum);
    }

    writer.Flush();
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int fact[6] = {0, 1, 2, 6, 24, 120};
  string s;
  while (cin >> s) {
    if (s == "0") break;
    int len = (int)s.size();
    int sum = 0;
    for (int i = 0; i < len; i++) {
      int digit = s[i] - '0';
      sum += digit * fact[len - i];
    }
    cout << sum << "\n";
  }

  return 0;
}
```
