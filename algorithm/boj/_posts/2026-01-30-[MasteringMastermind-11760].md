---
layout: single
title: "[백준 11760] Mastering Mastermind (C#, C++) - soo:bak"
date: "2026-01-30 20:11:00 +0900"
description: "백준 11760번 C#, C++ 풀이 - 코드와 추측이 주어졌을 때 r, s 값을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 11760
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 11760, 백준 11760번, BOJ 11760, Mastering Mastermind, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11760번 - Mastering Mastermind](https://www.acmicpc.net/problem/11760)

## 설명
길이 n의 코드와 추측이 주어질 때, 같은 위치에서 색이 일치하는 개수 r과, 남은 문자들 중 색만 일치하는 개수 s를 구하는 문제입니다.

<br>

## 접근법
먼저 같은 위치에서 일치하는 문자를 세어 r을 구하고, 그 위치들을 제외한 나머지 문자 빈도를 배열로 누적합니다.

알파벳 26글자에 대해 두 빈도 배열의 min 값을 합하면 s가 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    int n = int.Parse(parts[0]);
    var code = parts[1];
    var guess = parts[2];

    int r = 0;
    var cntCode = new int[26];
    var cntGuess = new int[26];

    for (int i = 0; i < n; i++) {
      if (code[i] == guess[i]) {
        r++;
      } else {
        cntCode[code[i] - 'A']++;
        cntGuess[guess[i] - 'A']++;
      }
    }

    int s = 0;
    for (int i = 0; i < 26; i++)
      s += Math.Min(cntCode[i], cntGuess[i]);

    Console.WriteLine($"{r} {s}");
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

  int n; string code, guess;
  cin >> n >> code >> guess;

  int r = 0;
  int cnt_code[26] = {0}, cnt_guess[26] = {0};

  for (int i = 0; i < n; i++) {
    if (code[i] == guess[i]) r++;
    else {
      cnt_code[code[i] - 'A']++;
      cnt_guess[guess[i] - 'A']++;
    }
  }

  int s = 0;
  for (int i = 0; i < 26; i++)
    s += min(cnt_code[i], cnt_guess[i]);

  cout << r << ' ' << s << "\n";
  return 0;
}
```
