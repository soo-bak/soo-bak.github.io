---
layout: single
title: "[백준 15962] 새로운 시작 (C#, C++) - soo:bak"
date: "2025-11-21 23:34:00 +0900"
description: 입력 없이 \"파이팅!!\"을 그대로 출력하는 백준 15962번 새로운 시작 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15962
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 15962, 백준 15962번, BOJ 15962, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15962번 - 새로운 시작](https://www.acmicpc.net/problem/15962)

## 설명

입력 없이 응원의 문구 “파이팅!!”을 출력합니다.

<br>

## 접근법

문자열을 그대로 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("파이팅!!");
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

  cout << "파이팅!!";
  return 0;
}
```

