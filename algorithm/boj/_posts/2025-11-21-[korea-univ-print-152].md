---
layout: single
title: "[백준 11942] 고려대는 사랑입니다 (C#, C++) - soo:bak"
date: "2025-11-21 23:54:00 +0900"
description: 입력 없이 고려대학교를 출력하는 백준 11942번 고려대는 사랑입니다 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11942
  - C#
  - C++
  - 알고리즘
keywords: "백준 11942, 백준 11942번, BOJ 11942, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11942번 - 고려대는 사랑입니다](https://www.acmicpc.net/problem/11942)

## 설명

입력이 없으며, 첫 줄에 “고려대학교”를 그대로 출력하면 됩니다.

<br>

## 접근법

정해진 문자열을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("고려대학교");
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

  cout << "고려대학교";

  return 0;
}
```

