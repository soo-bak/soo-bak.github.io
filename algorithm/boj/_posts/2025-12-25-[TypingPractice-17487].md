---
layout: single
title: "[백준 17487] 타자 연습 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: QWERTY 기준 왼손/오른손 키 입력 횟수를 계산하는 백준 17487번 타자 연습 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17487
  - C#
  - C++
  - 알고리즘
keywords: "백준 17487, 백준 17487번, BOJ 17487, TypingPractice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17487번 - 타자 연습](https://www.acmicpc.net/problem/17487)

## 설명
문장을 입력할 때 왼손과 오른손이 누르는 키 횟수를 계산하는 문제입니다.

<br>

## 접근법
먼저, 오른손으로 누르는 키 목록을 정의하고, 나머지는 왼손으로 처리합니다.

다음으로, 각 문자를 순회하며 공백과 대문자의 Shift 입력은 별도로 카운트합니다. 일반 키 입력은 해당 손에 바로 더합니다.

이후, 모아둔 공백과 Shift 입력을 현재 적게 사용한 손에 하나씩 분배하여 균형을 맞춥니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var rightKeys = new[] { 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'n', 'm' };
    var input = Console.ReadLine()!;
    var left = 0;
    var right = 0;
    var shiftOrSpace = 0;

    foreach (var ch in input) {
      if (ch == ' ') {
        shiftOrSpace++;
        continue;
      }

      if (ch >= 'A' && ch <= 'Z') {
        shiftOrSpace++;
        var lower = (char)(ch + ('a' - 'A'));
        if (rightKeys.Contains(lower)) right++;
        else left++;
      } else {
        if (rightKeys.Contains(ch)) right++;
        else left++;
      }
    }

    while (shiftOrSpace-- > 0) {
      if (left > right) right++;
      else left++;
    }

    Console.WriteLine($"{left} {right}");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<char> vc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vc rightKeys = { 'u', 'i', 'o', 'p', 'h', 'j', 'k', 'l', 'n', 'm' };

  string input; getline(cin, input);
  int left = 0, right = 0, shiftOrSpace = 0;
  for (char ch : input) {
    if (ch == ' ') {
      shiftOrSpace++;
      continue;
    }

    if (ch >= 'A' && ch <= 'Z') {
      shiftOrSpace++;
      char lower = ch + ('a' - 'A');
      if (find(rightKeys.begin(), rightKeys.end(), lower) != rightKeys.end()) right++;
      else left++;
    } else {
      if (find(rightKeys.begin(), rightKeys.end(), ch) != rightKeys.end()) right++;
      else left++;
    }
  }

  while (shiftOrSpace--) {
    if (left > right) right++;
    else left++;
  }

  cout << left << ' ' << right << '\n';

  return 0;
}
```

