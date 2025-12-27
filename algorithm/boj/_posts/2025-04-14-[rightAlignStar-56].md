---
layout: single
title: "[백준 2441] 별 찍기 - 4 (C#, C++) - soo:bak"
date: "2025-04-14 05:51:27 +0900"
description: 오른쪽 정렬된 역삼각형 모양의 별 출력 패턴을 구현하는 백준 2441번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2441
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 2441, 백준 2441번, BOJ 2441, rightAlignStar, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2441번 - 별 찍기 - 4](https://www.acmicpc.net/problem/2441)

## 설명
이 문제는 `N`이 주어졌을 때, **오른쪽 정렬된 역삼각형 형태의 별 패턴을 출력**하는 문제입니다.  <br>
각 줄의 왼쪽에 공백을 먼저 출력하고, 이후 별을 출력합니다.

---

## 접근법
- `i`번째 줄에는 `i`개의 공백과 `N - i`개의 별이 출력되어야 합니다.
- 반복문을 두 개 사용하여:
  - 먼저 공백을 출력하고,
  - 이후에 별을 출력하는 구조를 만들면 됩니다.

출력 형식에만 주의하면 되는 간단한 반복문 구현 문제입니다.

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
      for (int i = 0; i < n; i++) {
        Console.Write(new string(' ', i));
        Console.WriteLine(new string('*', n - i));
      }
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
  for (int i = 0; i < num; i++) {
    for (int j = 0; j < i; j++) cout << " ";
    for (int j = 0; j < num - i; j++) cout << "*";
    cout << "\n";
  }

  return 0;
}
```
