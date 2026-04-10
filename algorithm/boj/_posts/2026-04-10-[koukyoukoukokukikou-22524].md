---
layout: single
title: "[백준 22524] koukyoukoukokukikou (C#, C++) - soo:bak"
date: "2026-04-10 22:25:00 +0900"
description: "백준 22524번 C#, C++ 풀이 - QWERTY 기준으로 인접한 문자 사이의 손 전환 횟수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 22524
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 구현
keywords: "백준 22524, 백준 22524번, BOJ 22524, koukyoukoukokukikou, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[22524번 - koukyoukoukokukikou](https://www.acmicpc.net/problem/22524)

## 설명
문자열을 QWERTY 키보드로 입력한다고 할 때, 문자를 입력하는 손이 몇 번 바뀌는지 구하는 문제입니다.

<br>

## 접근법
각 알파벳이 왼손인지 오른손인지 먼저 정해 두면 됩니다.

QWERTY 기준으로 왼손으로 누르는 문자는 `qwertasdfgzxcvb`, 오른손으로 누르는 문자는 `yuiophjklnm`입니다. 문자열을 앞에서부터 보면서 현재 문자와 이전 문자를 누르는 손이 다를 때마다 횟수를 하나씩 늘리면 됩니다.

입력은 `#`가 나올 때까지 이어지므로, 문자열을 한 줄씩 읽으면서 바로 정답을 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static bool IsLeft(char ch) {
    return ch == 'q' || ch == 'w' || ch == 'e' || ch == 'r' || ch == 't' ||
           ch == 'a' || ch == 's' || ch == 'd' || ch == 'f' || ch == 'g' ||
           ch == 'z' || ch == 'x' || ch == 'c' || ch == 'v' || ch == 'b';
  }

  static void Main() {
    while (true) {
      string s = Console.ReadLine()!;
      if (s == "#")
        break;

      int count = 0;
      for (int i = 1; i < s.Length; i++) {
        if (IsLeft(s[i - 1]) != IsLeft(s[i]))
          count++;
      }

      Console.WriteLine(count);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isLeft(char ch) {
  return ch == 'q' || ch == 'w' || ch == 'e' || ch == 'r' || ch == 't' ||
         ch == 'a' || ch == 's' || ch == 'd' || ch == 'f' || ch == 'g' ||
         ch == 'z' || ch == 'x' || ch == 'c' || ch == 'v' || ch == 'b';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s;
  while (cin >> s) {
    if (s == "#")
      break;

    int count = 0;
    for (int i = 1; i < (int)s.size(); i++) {
      if (isLeft(s[i - 1]) != isLeft(s[i]))
        count++;
    }

    cout << count << "\n";
  }

  return 0;
}
```
