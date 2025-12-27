---
layout: single
title: "[백준 25773] Number Maximization (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 25773번 C#, C++ 풀이 - 주어진 숫자의 자릿수를 내림차순으로 정렬해 최대값을 만드는 문제"
tags:
  - 백준
  - BOJ
  - 25773
  - C#
  - C++
  - 알고리즘
keywords: "백준 25773, 백준 25773번, BOJ 25773, NumberMaximization, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25773번 - Number Maximization](https://www.acmicpc.net/problem/25773)

## 설명
입력된 숫자의 자릿수를 그대로 사용해 만들 수 있는 가장 큰 수를 출력하는 문제입니다.

<br>

## 접근법
숫자를 문자열로 보고 자릿수를 내림차순으로 정렬하면 가장 큰 수가 됩니다.  
정렬된 결과를 그대로 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var arr = s.ToCharArray();
    Array.Sort(arr);
    Array.Reverse(arr);
    Console.WriteLine(new string(arr));
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

  string s; cin >> s;
  sort(s.begin(), s.end(), greater<char>());
  cout << s << "\n";

  return 0;
}
```
