---
layout: single
title: "[백준 32432] Attention to the Meeting (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32432번 C#, C++ 풀이 - 회의 시간 제한에서 한 사람당 발언 시간을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 32432
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 32432, 백준 32432번, BOJ 32432, AttentionToTheMeeting, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32432번 - Attention to the Meeting](https://www.acmicpc.net/problem/32432)

## 설명
발언자 수와 전체 제한 시간으로 한 사람당 발언 시간을 구하는 문제입니다.

<br>

## 접근법
발언자들 사이에 1분씩 쉬는 시간이 있으므로 전체 제한 시간에서 휴식 시간을 뺍니다.

이후 남은 시간을 발언자 수로 나누면 한 사람당 발언 시간이 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var k = int.Parse(Console.ReadLine()!);
    var t = (k - (n - 1)) / n;
    Console.WriteLine(t);
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

  int n, k; cin >> n >> k;
  int t = (k - (n - 1)) / n;
  cout << t << "\n";

  return 0;
}
```
