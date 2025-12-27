---
layout: single
title: "[백준 2440] 별 찍기 - 3 (C#, C++) - soo:bak"
date: "2025-04-14 05:21:16 +0900"
description: 간단한 반복문을 통해 역삼각형 형태의 별 출력을 구현하는 백준 2440번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2440
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 2440, 백준 2440번, BOJ 2440, reverseStarPatternThree, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2440번 - 별 찍기 - 3](https://www.acmicpc.net/problem/2440)

## 설명
이 문제는 `N`이 주어졌을 때, `N`**줄에 걸쳐 역삼각형 형태로 별(*)을 출력하는 간단한 구현 문제**입니다.<br>

출력은 첫 줄에 `N`개의 별부터 시작해서 한 줄씩 별의 개수를 하나씩 줄여  <br>
마지막 줄에는 `1`개의 별이 출력되도록 구성해야 합니다.

---

## 접근법
- 입력으로 주어진 `N`을 기준으로 반복문을 수행합니다.
- `i`번째 줄에서는 `N - i + 1`개의 별을 출력합니다.
- 반복문과 문자열 출력 조합을 통해 쉽게 구현할 수 있습니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int n = int.Parse(Console.ReadLine()!);
      for (int i = n; i >= 1; i--)
        Console.WriteLine(new string('*', i));
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int num; cin >> num;
  while (num--) {
    for (int i = 0; i <= num; i++) cout << "*";
    cout << "\n";
  }

  return 0;
}
```
