---
layout: single
title: "[백준 1356] 유진수 (C++, C#) - soo:bak"
date: "2025-05-18 17:59:21 +0900"
description: 숫자를 두 부분으로 나누어 곱이 같은지 판별하는 백준 1356번 유진수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1356
  - C#
  - C++
  - 알고리즘
keywords: "백준 1356, 백준 1356번, BOJ 1356, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1356번 - 유진수](https://www.acmicpc.net/problem/1356)

## 설명

**주어진 수를 앞뒤로 나누었을 때, 각 부분의 자리수 곱이 같다면 '유진수'로 판단하는 문제입니다.**

입력으로 주어진 수는 문자열로 받아 처리하며,

적어도 한 자리씩 나누어야 하므로 전체 문자열의 가능한 분할 위치를 모두 시도합니다.

<br>
각 분할마다 앞부분과 뒷부분의 곱을 계산하고,

**같은 곱을 만드는 경우가 하나라도 있다면 유진수로 판단합니다.**

<br>

## 접근법

문제의 핵심은 주어진 수를 연속된 두 구간으로 나누었을 때,

**각 구간의 모든 자릿수를 곱한 값이 같은 경우가 존재하는지를 판단하는 것**입니다.

<br>
이를 위해 먼저 입력값을 문자열로 받아 처리합니다.

문자열로 처리하면, 숫자를 자릿수 단위로 분리하여 곱을 계산하는 과정이 편리하기 때문입니다.

<br>
다음으로, 문자열의 가능한 모든 분할 위치를 탐색합니다.<br>

- 분할 지점은 반드시 양쪽에 하나 이상의 자릿수가 있어야 하므로,
- 유효한 분할은 `1`부터 `문자열의 길이 - 1`까지입니다.

<br>
각 분할에 대해 다음을 수행합니다:
- 앞부분과 뒷부분의 자릿수 곱을 각각 계산합니다.
- 곱이 일치하는 경우가 하나라도 발견되면 조건을 만족하는 유진수입니다.

<br>
모든 분할을 검사한 뒤에도 일치하는 경우가 없다면 해당 수는 유진수가 아닙니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string num = Console.ReadLine();
    bool found = false;

    for (int d = 1; d < num.Length; ++d) {
      string left = num.Substring(0, d);
      string right = num.Substring(d);

      int prod1 = 1, prod2 = 1;
      foreach (char c in left)
        prod1 *= c - '0';
      foreach (char c in right)
        prod2 *= c - '0';

      if (prod1 == prod2) {
        found = true;
        break;
      }
    }

    Console.WriteLine(found ? "YES" : "NO");
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

  string num; cin >> num;
  bool found = false;

  for (int d = 1; d < num.size(); ++d) {
    string s1 = num.substr(0, d), s2 = num.substr(d);
    int prod1 = 1, prod2 = 1;
    for (char c : s1) prod1 *= c - '0';
    for (char c : s2) prod2 *= c - '0';

    if (prod1 == prod2) {
      found = true;
      break;
    }
  }

  cout << (found ? "YES" : "NO") << "\n";

  return 0;
}
```
