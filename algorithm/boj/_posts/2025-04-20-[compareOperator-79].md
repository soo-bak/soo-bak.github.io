---
layout: single
title: "[백준 5656] 비교 연산자 (C#, C++) - soo:bak"
date: "2025-04-20 01:05:00 +0900"
description: 두 수와 비교 연산자를 받아 조건을 판별하는 백준 5656번 비교 연산자 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5656
  - C#
  - C++
  - 알고리즘
keywords: "백준 5656, 백준 5656번, BOJ 5656, compareOperator, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5656번 - 비교 연산자](https://www.acmicpc.net/problem/5656)

## 설명
**두 정수와 하나의 비교 연산자가 주어졌을 때, 그 조건이 참인지 거짓인지를 판별하는 단순한 시뮬레이션 문제**입니다.
<br>

- 입력은 반복적으로 주어지며, 각 줄마다 `정수1`, `연산자`, `정수2`의 형태로 구성됩니다.
- 입력의 연산자 부분이 문자 `E`라면 시뮬레이션을 종료합니다.
- 사용 가능한 연산자는 다음과 같습니다:
  - `>` , `>=` , `<` , `<=` , `==` , `!=`
<br>

- 각 비교 연산의 결과가 참이면 `true`, 거짓이면 `false`를 출력합니다.
- 출력 형식은 `"Case x: 결과"` 형태이며, `x`는 `1`부터 시작하는 케이스 번호입니다.

## 접근법

1. 반복문을 통해 계속해서 입력을 읽어들입니다.
2. 각 줄에서 정수 하나, 문자열 연산자, 정수 하나를 차례로 읽습니다.
3. 연산자가 `E`인 경우 반복문을 종료합니다.
4. 그 외에는 각각의 연산자에 따라 조건식을 판단하고 결과를 출력합니다.
5. 출력 형식 `"Case x: true/false"`를 맞추기 위해 케이스 번호를 `1`부터 증가시키며 사용합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int caseNum = 1;

    while (true) {
      var input = Console.ReadLine().Split();
      int l = int.Parse(input[0]);
      string op = input[1];
      int r = int.Parse(input[2]);

      if (op == "E") break;

      bool result = op switch {
        ">"  => l > r,
        ">=" => l >= r,
        "<"  => l < r,
        "<=" => l <= r,
        "==" => l == r,
        "!=" => l != r,
        _    => false
      };

      Console.WriteLine($"Case {caseNum++}: {(result ? "true" : "false")}");
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

  int caseNum = 1;
  while (true) {
    int l, r; string op;
    cin >> l >> op >> r;

    if (op == "E") break;

    bool result;
    if (op == ">") result = l > r;
    else if (op == ">=") result = l >= r;
    else if (op == "<") result = l < r;
    else if (op == "<=") result = l <= r;
    else if (op == "==") result = l == r;
    else if (op == "!=") result = l != r;

    cout << "Case " << caseNum++ << ": " << (result ? "true" : "false") << "\n";
  }

  return 0;
}
```
