---
layout: single
title: "[백준 12813] 이진수 연산 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: 두 이진 문자열로 AND/OR/XOR/NOT을 계산하는 문제
---

## 문제 링크
[12813번 - 이진수 연산](https://www.acmicpc.net/problem/12813)

## 설명
두 이진수 A, B에 대해 AND, OR, XOR, NOT 결과를 출력하는 문제입니다.

<br>

## 접근법
각 비트를 순회하며 연산 결과를 문자열로 만듭니다.

NOT은 각각의 문자열에서 0과 1을 뒤집습니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var a = Console.ReadLine()!;
    var b = Console.ReadLine()!;
    var n = a.Length;

    var and = new StringBuilder();
    var or = new StringBuilder();
    var xor = new StringBuilder();
    var nota = new StringBuilder();
    var notb = new StringBuilder();

    for (var i = 0; i < n; i++) {
      var ca = a[i];
      var cb = b[i];

      and.Append(ca == '1' && cb == '1' ? '1' : '0');
      or.Append(ca == '1' || cb == '1' ? '1' : '0');
      xor.Append(ca != cb ? '1' : '0');
      nota.Append(ca == '1' ? '0' : '1');
      notb.Append(cb == '1' ? '0' : '1');
    }

    Console.WriteLine(and.ToString());
    Console.WriteLine(or.ToString());
    Console.WriteLine(xor.ToString());
    Console.WriteLine(nota.ToString());
    Console.WriteLine(notb.ToString());
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

  string a, b; cin >> a >> b;
  int n = a.size();

  string ands, ors, xors, nota, notb;
  ands.reserve(n);
  ors.reserve(n);
  xors.reserve(n);
  nota.reserve(n);
  notb.reserve(n);

  for (int i = 0; i < n; i++) {
    char ca = a[i];
    char cb = b[i];
    ands.push_back((ca == '1' && cb == '1') ? '1' : '0');
    ors.push_back((ca == '1' || cb == '1') ? '1' : '0');
    xors.push_back((ca != cb) ? '1' : '0');
    nota.push_back(ca == '1' ? '0' : '1');
    notb.push_back(cb == '1' ? '0' : '1');
  }

  cout << ands << "\n";
  cout << ors << "\n";
  cout << xors << "\n";
  cout << nota << "\n";
  cout << notb << "\n";

  return 0;
}
```
