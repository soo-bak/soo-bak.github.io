---
layout: single
title: "[백준 20001] 고무오리 디버깅 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 20001번 C#, C++ 풀이 - 문제 수를 스택처럼 관리해 디버깅 결과를 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 20001
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 20001, 백준 20001번, BOJ 20001, RubberDuckDebugging, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20001번 - 고무오리 디버깅](https://www.acmicpc.net/problem/20001)

## 설명
입력 흐름에 따라 남은 문제 수를 관리하고 결과를 출력하는 문제입니다.

<br>

## 접근법
문제 수를 정수로 관리합니다.

"문제"면 1 증가, "고무오리"면 1 감소하되 0일 때는 2 증가합니다. 종료 후 0이면 성공입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine();
    var cnt = 0;

    while (true) {
      line = Console.ReadLine();
      if (line == "고무오리 디버깅 끝") break;

      if (line == "문제") cnt++;
      else {
        if (cnt == 0) cnt += 2;
        else cnt--;
      }
    }

    Console.WriteLine(cnt == 0 ? "고무오리야 사랑해" : "힝구");
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
  getline(cin, line);

  int cnt = 0;
  while (true) {
    getline(cin, line);
    if (line == "고무오리 디버깅 끝") break;

    if (line == "문제") cnt++;
    else {
      if (cnt == 0) cnt += 2;
      else cnt--;
    }
  }

  cout << (cnt == 0 ? "고무오리야 사랑해" : "힝구") << "\n";

  return 0;
}
```
