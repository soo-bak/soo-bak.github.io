---
layout: single
title: "[백준 10474] 분수좋아해? (C#, C++) - soo:bak"
date: "2025-04-20 02:52:00 +0900"
description: 기약분수를 혼합형 분수로 표현하는 과정을 반복적으로 수행하는 백준 10474번 분수좋아해? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10474
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 10474, 백준 10474번, BOJ 10474, mixedFraction, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10474번 - 분수좋아해?](https://www.acmicpc.net/problem/10474)

## 설명
**주어진 진분수를 정수 부분과 분수 부분으로 나누어 대분수 형태로 출력하는 문제입니다.**
<br>

- 각 줄마다 두 개의 정수 `분자`와 `분모`가 주어지며, 이는 항상 진분수를 구성합니다
  (분자가 분모보다 작거나 같지 않을 수 있음).
- 입력은 `(0, 0)` 쌍이 주어질 때까지 반복되며, 이를 만나면 종료합니다.
- 각 분수는 다음 형태로 변환하여 출력합니다:<br>
  $$ a \div b = q \quad r \ / \ b $$<br>
  (`q = a / b` (정수 몫), `r = a % b` (나머지))

예시 :
- 입력: `27 12` → 출력: `2 3 / 12`
- 입력: `6 3` → 출력: `2 0 / 3`

## 접근법

1. 반복적으로 두 정수를 입력받습니다.
2. 입력된 두 값이 모두 `0`이면 종료합니다.
3. 정수 나눗셈과 나머지를 이용해 분수를 변환합니다.
4. `정수 몫`, `나머지 / 분모` 형태로 출력합니다.

- `분자 < 분모`일 경우 `0 a / b` 형태로 출력합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      var input = Console.ReadLine().Split();
      int a = int.Parse(input[0]), b = int.Parse(input[1]);
      if (a == 0 && b == 0) break;
      Console.WriteLine($"{a / b} {a % b} / {b}");
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

  while (true) {
    int numer, denomi; cin >> numer >> denomi;
    if (!numer && !denomi) break ;
    cout << numer / denomi << " " << numer % denomi << " / " << denomi << "\n";
  }

  return 0;
}
```
