---
layout: single
title: "[백준 10822] 더하기 (C#, C++) - soo:bak"
date: "2025-04-20 03:02:00 +0900"
description: 콤마(,)로 구분된 문자열을 숫자로 분리한 뒤 합을 계산하는 백준 10822번 더하기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10822
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 문자열
  - arithmetic
  - 파싱
keywords: "백준 10822, 백준 10822번, BOJ 10822, commaAddition, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10822번 - 더하기](https://www.acmicpc.net/problem/10822)

## 설명
**콤마(,)로 구분된 여러 숫자들을 입력받아, 이를 모두 더한 값을 출력하는 문제입니다.**
<br>

- 한 줄에 콤마로 구분된 정수들이 문자열 형태로 입력됩니다.
- 이 문자열을 **정수 리스트로 분리**한 뒤, **모든 수의 합을 출력**하면 됩니다.

예시:
- 입력: `"10,20,30,50"` → 출력: `110`

## 접근법

1. 한 줄의 문자열을 입력받습니다.
2. 콤마를 기준으로 문자열을 분리합니다.
3. 각 항목을 정수로 변환한 뒤, 누적 합을 계산합니다.
4. 결과를 출력합니다.

- 문자열 파싱이 핵심인 문제입니다.
- 시간 복잡도는 `O(n)`입니다.

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var sum = Console.ReadLine()
      .Split(',')
      .Select(int.Parse)
      .Sum();
    Console.WriteLine(sum);
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

  string s, num;
  while (getline(cin, num)) s += num;

  int sum = 0;
  stringstream ss(s);
  while (getline(ss, num, ',')) sum += stoi(num);

  cout << sum << "\n";

  return 0;
}
```
