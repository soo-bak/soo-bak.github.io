---
layout: single
title: "[백준 12778] CTP공국으로 이민 가자 (C#, C++) - soo:bak"
date: "2025-05-16 21:23:00 +0900"
description: 숫자와 알파벳을 상호 변환하여 시험 문제를 채점하는 백준 12778번 CTP공국으로 이민 가자 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 12778
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 12778, 백준 12778번, BOJ 12778, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12778번 - CTP공국으로 이민 가자](https://www.acmicpc.net/problem/12778)

## 설명

**알파벳과 숫자 간의 상호 변환을 통해 주어진 문제를 채점하는 시뮬레이션 문제입니다.**

CTP공국에서는 알파벳을 사용할 때 A부터 Z까지를 각각 `1`부터 `26`까지의 숫자로 변환하여 사용합니다.

- 예를 들어 `'A' → 1`, `'B' → 2`, ..., `'Z' → 26`
- 반대로 숫자 `1`은 `'A'`, 숫자 `26`은 `'Z'`를 의미합니다.

각 테스트케이스는 다음 중 하나로 구성됩니다:

- `C` (Character → Number): 알파벳이 주어졌을 때 숫자로 바꾸기
- `N` (Number → Character): 숫자가 주어졌을 때 알파벳으로 바꾸기

입력된 방식에 따라 변환을 수행하여 결과를 공백으로 구분해 출력합니다.

<br>

## 접근법

각 테스트케이스마다 다음 흐름으로 처리합니다:

- 변환할 값의 개수 `n`과 변환 모드 `C` 또는 `N`을 입력받습니다.
- `C`인 경우는 알파벳을 숫자로:
  - `'A' → 1`은 `c - 'A' + 1`로 계산할 수 있습니다.
- `N`인 경우는 숫자를 알파벳으로:
  - `1 → 'A'`는 `(char)(x + 'A' - 1)`로 처리하면 됩니다.
- 변환 결과를 공백으로 구분해 출력합니다.

각 입력의 최대 길이는 `500`이므로, 단순한 반복문으로도 충분히 빠르게 처리됩니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var info = Console.ReadLine().Split();
      int n = int.Parse(info[0]);
      char mode = info[1][0];
      var tokens = Console.ReadLine().Split();

      for (int i = 0; i < n; i++) {
        if (mode == 'C')
          Console.Write((tokens[i][0] - 'A' + 1) + (i < n - 1 ? " " : "\n"));
        else
          Console.Write((char)('A' + int.Parse(tokens[i]) - 1) + (i < n - 1 ? " " : "\n"));
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
    int n; char mode; cin >> n >> mode;
    for (int i = 0; i < n; ++i) {
      if (mode == 'C') {
        char c; cin >> c;
        cout << (c - 'A' + 1);
      } else {
        int x; cin >> x;
        cout << (char)('A' + x - 1);
      }
      cout << (i < n - 1 ? " " : "\n");
    }
  }

  return 0;
}
```
