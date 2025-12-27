---
layout: single
title: "[백준 25784] Easy-to-Solve Expressions (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: 세 수 중 하나가 나머지 두 수의 합이면 1, 곱이면 2, 아니면 3을 출력하는 백준 25784번 Easy-to-Solve Expressions 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 25784
  - C#
  - C++
  - 알고리즘
keywords: "백준 25784, 백준 25784번, BOJ 25784, EasyExpressions, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25784번 - Easy-to-Solve Expressions](https://www.acmicpc.net/problem/25784)

## 설명
서로 다른 양의 정수 3개가 주어질 때, 세 수 사이의 관계를 판별하는 문제입니다.

<br>

## 접근법
먼저 세 수를 정렬하여 가장 큰 값을 찾습니다.

가장 큰 값이 나머지 두 수의 합이면 1, 곱이면 2, 둘 다 아니면 3을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var a = int.Parse(line[0]);
    var b = int.Parse(line[1]);
    var c = int.Parse(line[2]);
    var arr = new int[] { a, b, c };
    Array.Sort(arr);
    if (arr[0] + arr[1] == arr[2]) Console.WriteLine(1);
    else if (arr[0] * arr[1] == arr[2]) Console.WriteLine(2);
    else Console.WriteLine(3);
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

  int a, b, c; cin >> a >> b >> c;
  int v[3] = {a, b, c};
  sort(v, v + 3);
  if (v[0] + v[1] == v[2]) cout << 1 << "\n";
  else if (v[0] * v[1] == v[2]) cout << 2 << "\n";
  else cout << 3 << "\n";

  return 0;
}
```
