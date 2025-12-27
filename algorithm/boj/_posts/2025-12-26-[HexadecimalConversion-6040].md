---
layout: single
title: "[백준 6040] Hexadecimal Conversion (C#, C++) - soo:bak"
date: "2025-12-26 02:24:00 +0900"
description: "백준 6040번 C#, C++ 풀이 - 16진수를 8진수로 변환하는 문제"
tags:
  - 백준
  - BOJ
  - 6040
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arbitrary_precision
keywords: "백준 6040, 백준 6040번, BOJ 6040, HexadecimalConversion, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6040번 - Hexadecimal Conversion](https://www.acmicpc.net/problem/6040)

## 설명
주어진 16진수를 8진수로 변환해 출력하는 문제입니다.

<br>

## 접근법
먼저 각 16진 자리를 대응하는 2진수로 펼쳐 하나의 문자열을 만듭니다.

다음으로 앞쪽의 불필요한 0을 제거하고, 3자리씩 묶을 수 있도록 앞에 0을 채웁니다.

마지막으로 3자리씩 묶어 8진수 자리로 바꿔 이어 붙여 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var hex = Console.ReadLine()!.Trim();
    if (hex == "0") {
      Console.WriteLine("0");
      return;
    }

    var binSb = new StringBuilder(hex.Length * 4);
    for (var i = 0; i < hex.Length; i++) {
      var c = hex[i];
      var v = c <= '9' ? c - '0' : c - 'A' + 10;
      for (var b = 3; b >= 0; b--)
        binSb.Append(((v >> b) & 1) == 1 ? '1' : '0');
    }

    var bin = binSb.ToString();
    var first = 0;
    while (first < bin.Length && bin[first] == '0')
      first++;

    if (first == bin.Length) {
      Console.WriteLine("0");
      return;
    }

    bin = bin.Substring(first);
    var mod = bin.Length % 3;
    if (mod != 0) bin = new string('0', 3 - mod) + bin;

    var outSb = new StringBuilder(bin.Length / 3);
    for (var i = 0; i < bin.Length; i += 3) {
      var val = (bin[i] - '0') * 4 + (bin[i + 1] - '0') * 2 + (bin[i + 2] - '0');
      outSb.Append((char)('0' + val));
    }

    Console.WriteLine(outSb.ToString());
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

  string hex; cin >> hex;

  if (hex == "0") {
    cout << "0\n";
    return 0;
  }

  string bin;
  bin.reserve((int)hex.size() * 4);
  for (int i = 0; i < (int)hex.size(); i++) {
    char c = hex[i];
    int v = c <= '9' ? c - '0' : c - 'A' + 10;
    for (int b = 3; b >= 0; b--)
      bin.push_back(((v >> b) & 1) ? '1' : '0');
  }

  int first = 0;
  while (first < (int)bin.size() && bin[first] == '0')
    first++;

  if (first == (int)bin.size()) {
    cout << "0\n";
    return 0;
  }

  bin = bin.substr(first);
  int mod = (int)bin.size() % 3;
  if (mod != 0) bin = string(3 - mod, '0') + bin;

  string out;
  out.reserve((int)bin.size() / 3);
  for (int i = 0; i < (int)bin.size(); i += 3) {
    int val = (bin[i] - '0') * 4 + (bin[i + 1] - '0') * 2 + (bin[i + 2] - '0');
    out.push_back(char('0' + val));
  }

  cout << out << "\n";
  return 0;
}
```
