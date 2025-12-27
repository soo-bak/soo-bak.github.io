---
layout: single
title: "[백준 28722] Звуки в подвале (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 28722번 C#, C++ 풀이 - 문자열의 양끝 색이 다르면 Win, 같으면 Lose를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 28722
  - C#
  - C++
  - 알고리즘
  - 구현
  - game_theory
keywords: "백준 28722, 백준 28722번, BOJ 28722, SoundsInBasement, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[28722번 - Звуки в подвале](https://www.acmicpc.net/problem/28722)

## 설명
빨강과 파랑으로 이루어진 문자열이 주어질 때, 선공이 이길 수 있는지 판별하는 문제입니다.

<br>

## 접근법
첫 칸과 마지막 칸의 색이 다르면, 색이 바뀌는 지점에서 잘라 양끝 색이 같은 두 조각을 만들 수 있습니다. 상대는 더 이상 자를 수 없으므로 선공이 승리합니다.

양끝 색이 같으면 처음부터 자를 수 없어 선공이 패배합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    Console.WriteLine(s[0] == s[s.Length - 1] ? "Lose" : "Win");
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
  cout << (s.front() == s.back() ? "Lose" : "Win") << "\n";

  return 0;
}
```
