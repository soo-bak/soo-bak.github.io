---
layout: single
title: "[백준 23234] The World Responds (C#, C++) - soo:bak"
date: "2025-11-21 23:42:00 +0900"
description: 입력 없이 The world says hello!를 출력하는 백준 23234번 The World Responds 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23234
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 23234, 백준 23234번, BOJ 23234, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23234번 - The World Responds](https://www.acmicpc.net/problem/23234)

## 설명

입력 없이 `"The world says hello!"`를 출력합니다.

<br>

## 접근법

정해진 문장을 그대로 출력하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("The world says hello!");
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

  cout << "The world says hello!\n";

  return 0;
}
```

