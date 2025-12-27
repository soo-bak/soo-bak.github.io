---
layout: single
title: "[백준 17295] 엔드게임 스포일러 (C#, C++) - soo:bak"
date: "2025-11-22 03:05:00 +0900"
description: 입력과 상관없이 Avengers Endgame을 출력하는 백준 17295번 엔드게임 스포일러 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17295
  - C#
  - C++
  - 알고리즘
keywords: "백준 17295, 백준 17295번, BOJ 17295, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17295번 - 엔드게임 스포일러](https://www.acmicpc.net/problem/17295)

## 설명

입력은 무시하고, `"Avengers: Endgame"`을 출력하면 됩니다.

<br>

## 접근법

정해진 문자열을 그대로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("Avengers: Endgame");
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

  cout << "Avengers: Endgame\n";
  return 0;
}
```

