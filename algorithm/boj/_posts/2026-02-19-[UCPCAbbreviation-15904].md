---
layout: single
title: "[백준 15904] UCPC는 무엇의 약자일까? (C#, C++) - soo:bak"
date: "2026-02-19 23:03:00 +0900"
description: "백준 15904번 C#, C++ 풀이 - 문자열을 축약해 UCPC를 만들 수 있는지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 15904
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 15904, 백준 15904번, BOJ 15904, UCPC는 무엇의 약자일까, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15904번 - UCPC는 무엇의 약자일까?](https://www.acmicpc.net/problem/15904)

## 설명
문자열에서 일부 문자를 지워 대소문자를 유지한 채 `UCPC`를 순서대로 만들 수 있는지 확인하는 문제입니다.

<br>

## 접근법
목표 문자열 `UCPC`를 두고 입력을 왼쪽부터 보면서 일치하는 문자를 찾을 때마다 목표 인덱스를 하나씩 증가시킵니다. 끝까지 보았을 때 목표 인덱스가 4라면 만들 수 있으므로 `I love UCPC`, 아니면 `I hate UCPC`를 출력하면 됩니다.

시간 복잡도는 O(N)입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var target = "UCPC";
    var idx = 0;

    foreach (var ch in s) {
      if (idx < 4 && ch == target[idx])
        idx++;
    }

    Console.WriteLine(idx == 4 ? "I love UCPC" : "I hate UCPC");
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

  string s;
  getline(cin, s);

  string target = "UCPC";
  int idx = 0;
  for (char ch : s) {
    if (idx < 4 && ch == target[idx])
      idx++;
  }

  cout << (idx == 4 ? "I love UCPC" : "I hate UCPC") << "\n";

  return 0;
}
```
