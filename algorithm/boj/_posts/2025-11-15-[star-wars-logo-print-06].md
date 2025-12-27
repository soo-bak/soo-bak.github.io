---
layout: single
title: "[백준 9653] 스타워즈 로고 (C#, C++) - soo:bak"
date: "2025-11-15 01:20:00 +0900"
description: 주어진 스타워즈 ASCII 로고를 그대로 출력하는 백준 9653번 스타워즈 로고 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 9653
  - C#
  - C++
  - 알고리즘
keywords: "백준 9653, 백준 9653번, BOJ 9653, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9653번 - 스타워즈 로고](https://www.acmicpc.net/problem/9653)

## 설명

입력 없이 스타워즈 로고를 예제처럼 출력하는 문제입니다.

<br>

## 접근법

문제에서 제시된 ASCII 아트를 그대로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    Console.WriteLine("    8888888888  888    88888");
    Console.WriteLine("   88     88   88 88   88  88");
    Console.WriteLine("    8888  88  88   88  88888");
    Console.WriteLine("       88 88 888888888 88   88");
    Console.WriteLine("88888888  88 88     88 88    888888");
    Console.WriteLine();
    Console.WriteLine("88  88  88   888    88888    888888");
    Console.WriteLine("88  88  88  88 88   88  88  88");
    Console.WriteLine("88 8888 88 88   88  88888    8888");
    Console.WriteLine(" 888  888 888888888 88  88      88");
    Console.WriteLine("  88  88  88     88 88   88888888");
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

  cout << "    8888888888  888    88888\n";
  cout << "   88     88   88 88   88  88\n";
  cout << "    8888  88  88   88  88888\n";
  cout << "       88 88 888888888 88   88\n";
  cout << "88888888  88 88     88 88    888888\n\n";
  cout << "88  88  88   888    88888    888888\n";
  cout << "88  88  88  88 88   88  88  88\n";
  cout << "88 8888 88 88   88  88888    8888\n";
  cout << " 888  888 888888888 88  88      88\n";
  cout << "  88  88  88     88 88   88888888\n";
  
  return 0;
}
```

