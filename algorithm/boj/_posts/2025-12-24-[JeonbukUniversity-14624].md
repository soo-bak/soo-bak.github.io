---
layout: single
title: "[백준 14624] 전북대학교 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 14624번 C#, C++ 풀이 - 홀수면 심볼 패턴을, 짝수면 문구를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 14624
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 14624, 백준 14624번, BOJ 14624, JeonbukUniversity, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14624번 - 전북대학교](https://www.acmicpc.net/problem/14624)

## 설명
N이 홀수면 별 패턴을 출력하고, 짝수면 지정 문구를 출력하는 문제입니다.

<br>

## 접근법
짝수면 `I LOVE CBNU`를 출력합니다.

홀수면 첫 줄은 길이 N의 별로 출력하고, 이후 줄은 중앙에서 시작해 양쪽으로 벌어지는 형태로 별을 찍습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    if (n % 2 == 0) {
      Console.WriteLine("I LOVE CBNU");
      return;
    }

    Console.WriteLine(new string('*', n));
    var rows = n / 2 + 1;
    for (var i = 1; i <= rows; i++) {
      var lead = rows - i;
      if (i == 1) Console.WriteLine(new string(' ', lead) + "*");
      else {
        var inner = 2 * i - 3;
        Console.WriteLine(new string(' ', lead) + "*" + new string(' ', inner) + "*");
      }
    }
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
  if (n % 2 == 0) {
    cout << "I LOVE CBNU\n";
    return 0;
  }

  cout << string(n, '*') << "\n";
  int rows = n / 2 + 1;
  for (int i = 1; i <= rows; i++) {
    int lead = rows - i;
    if (i == 1) cout << string(lead, ' ') << "*\n";
    else {
      int inner = 2 * i - 3;
      cout << string(lead, ' ') << "*" << string(inner, ' ') << "*\n";
    }
  }

  return 0;
}
```
