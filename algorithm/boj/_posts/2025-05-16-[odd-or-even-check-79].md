---
layout: single
title: "[백준 5988] 홀수일까 짝수일까 (C#, C++) - soo:bak"
date: "2025-05-16 22:07:00 +0900"
description: 큰 수의 마지막 자리를 이용해 홀수인지 짝수인지 판별하는 백준 5988번 홀수일까 짝수일까 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5988
  - C#
  - C++
  - 알고리즘
  - 수학
  - 문자열
  - arithmetic
  - arbitrary_precision
keywords: "백준 5988, 백준 5988번, BOJ 5988, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5988번 - 홀수일까 짝수일까](https://www.acmicpc.net/problem/5988)

## 설명

**길이가 매우 긴 수가 주어졌을 때, 해당 수가 홀수인지 짝수인지 판별하는 간단한 문제입니다.**

입력으로 주어지는 수는 `최대 60자리의 자연수`로, 일반적인 정수 타입으로는 처리할 수 없습니다.

<br>
하지만 **홀수인지 짝수인지를 판단하는 기준은 가장 마지막 자리**이기 때문에,

전체 숫자를 파싱할 필요 없이 문자열의 마지막 문자만 확인하면 됩니다.

- `1`, `3`, `5`, `7`, `9` → 홀수 (`odd`)
- `0`, `2`, `4`, `6`, `8` → 짝수 (`even`)

<br>

## 접근법

문자열로 주어진 수가 아무리 길더라도, 그 수가 홀수인지 짝수인지를 판단하는 데에는 전체 수를 볼 필요가 없습니다.

정수의 홀짝 여부는 **항상 마지막 자리 숫자 하나만으로 결정**되기 때문입니다.

<br>
예를 들어, `104`나 `12234567890` 같은 수는 끝자리가 `0`이므로 짝수이고,
`777`, `123`처럼 끝자리가 `3`이나 `7`인 경우는 홀수입니다.

<br>
따라서 입력으로 주어진 문자열의 마지막 문자를 확인하여,

그 문자가 짝수 숫자이면 `"even"`, 홀수 숫자이면 `"odd"`라고 출력하면 됩니다.

숫자를 직접 계산할 필요 없이, 끝자리만 읽는 방식으로도 정확하고 빠르게 판별이 가능하다는 점이 이 문제의 핵심입니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    while (n-- > 0) {
      string s = Console.ReadLine();
      char last = s[s.Length - 1];
      Console.WriteLine((last - '0') % 2 == 0 ? "even" : "odd");
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
  while (n--) {
    string s; cin >> s;
    cout << (s.back() % 2 ? "odd" : "even") << "\n";
  }

  return 0;
}
```
