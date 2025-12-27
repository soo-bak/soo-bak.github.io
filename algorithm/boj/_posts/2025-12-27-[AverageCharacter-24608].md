---
layout: single
title: "[백준 24608] Average Character (C#, C++) - soo:bak"
date: "2025-12-27 09:35:00 +0900"
description: 문자열의 ASCII 코드 평균을 계산해 해당 문자로 출력하는 문제
---

## 문제 링크
[24608번 - Average Character](https://www.acmicpc.net/problem/24608)

## 설명
문자열의 각 문자 코드값의 평균을 구하고, 그 값에 해당하는 문자를 출력하는 문제입니다. 평균이 소수면 내림합니다.

<br>

## 접근법
모든 문자의 코드값을 더한 뒤 길이로 나누면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var sum = 0;
    foreach (var ch in s)
      sum += ch;
    var avg = sum / s.Length;
    Console.WriteLine((char)avg);
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

  string s; getline(cin, s);

  ll sum = 0;
  for (char c : s)
    sum += (unsigned char)c;
  int avg = sum / s.size();
  cout << (char)avg << "\n";

  return 0;
}
```
