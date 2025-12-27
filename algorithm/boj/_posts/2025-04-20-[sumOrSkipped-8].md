---
layout: single
title: "[백준 5026] P=NP? (C#, C++) - soo:bak"
date: "2025-04-20 03:18:00 +0900"
description: 주어진 문자열이 P=NP인지 덧셈 문제인지 판별하여 처리하는 백준 5026번 P=NP? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5026
  - C#
  - C++
  - 알고리즘
keywords: "백준 5026, 백준 5026번, BOJ 5026, sumOrSkipped, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5026번 - P=NP?](https://www.acmicpc.net/problem/5026)

## 설명
**문자열로 주어진 입력에 대하여, 컴퓨터 과학 문제인지, 덧셈 문제인지 판별하여 각각 다른 출력을 하는 조건 분기 문제입니다.**
<br>

- 먼저 테스트케이스의 개수가 주어지고, 이어서 각 테스트케이스마다 하나의 문자열이 입력됩니다.
- 각 문자열은 두 가지 중 하나입니다:
  - `P=NP`인 경우 → `"skipped"` 출력
  - `a+b` 형태인 경우 → 정수 덧셈으로 `a + b` 를 계산하여 출력


## 접근법

1. 테스트케이스의 개수를 입력받습니다.
2. 각 테스트케이스에 대해 문자열을 입력받고 조건에 따라 처리합니다.
3. 문자열이 `"P=NP"`인지 비교합니다.
   - 맞으면 `"skipped"` 출력
   - 아니면 `+` 기호를 기준으로 나눈 뒤, 각각 정수로 변환하여 합을 출력합니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      string s = Console.ReadLine();
      if (s == "P=NP") Console.WriteLine("skipped");
      else {
        var parts = s.Split('+');
        Console.WriteLine(int.Parse(parts[0]) + int.Parse(parts[1]));
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

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;
    if (s == "P=NP") cout << "skipped\n";
    else {
      int pos = s.find('+');
      cout << stoi(s.substr(0, pos)) + stoi(s.substr(pos + 1)) << "\n";
    }
  }

  return 0;
}
```
