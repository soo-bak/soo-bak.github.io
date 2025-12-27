---
layout: single
title: "[백준 3765] Celebrity jeopardy (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 입력된 식을 그대로 출력하는 초단순 구현 문제인 백준 3765번 Celebrity jeopardy 풀이
tags:
  - 백준
  - BOJ
  - 3765
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
  - 애드혹
keywords: "백준 3765, 백준 3765번, BOJ 3765, CelebrityJeopardy, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3765번 - Celebrity jeopardy](https://www.acmicpc.net/problem/3765)

## 설명
입력으로 주어진 각 줄을 그대로 출력하는 문제입니다.

입력이 끝날 때까지 반복합니다.

<br>

## 접근법
한 줄씩 읽어서 그대로 출력합니다.

입력이 끝나면 종료합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string? line;
    while ((line = Console.ReadLine()) != null) {
      Console.WriteLine(line);
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

  string line;
  while (getline(cin, line))
    cout << line << "\n";

  return 0;
}
```
