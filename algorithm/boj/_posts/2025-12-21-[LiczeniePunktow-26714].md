---
layout: single
title: "[백준 26714] Liczenie punktów (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 문자열을 10등분해 각 구간이 모두 T인지 확인하고 점수를 합산하는 문제
---

## 문제 링크
[26714번 - Liczenie punktów](https://www.acmicpc.net/problem/26714)

## 설명
길이 n의 결과 문자열을 10개 구간으로 나누어, 각 구간이 전부 T이면 1점을 주는 방식으로 총점을 구하는 문제입니다.

<br>

## 접근법
구간 길이는 n/10입니다. 각 구간의 모든 문자가 T인지 확인하고, 모두 T인 구간 수를 세어 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var len = n / 10;

    var score = 0;
    for (var g = 0; g < 10; g++) {
      var ok = true;
      for (var i = g * len; i < (g + 1) * len; i++) {
        if (s[i] != 'T') ok = false;
      }
      if (ok) score++;
    }

    Console.WriteLine(score);
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

  int n; cin >> n;
  string s; cin >> s;
  int len = n / 10;

  int score = 0;
  for (int g = 0; g < 10; g++) {
    bool ok = true;
    for (int i = g * len; i < (g + 1) * len; i++) {
      if (s[i] != 'T') ok = false;
    }
    if (ok) score++;
  }

  cout << score << "\n";

  return 0;
}
```
