---
layout: single
title: "[백준 5211] 가단조와 다장조 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 5211번 C#, C++ 풀이 - 마디의 첫 음 중심음을 세어 조성을 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 5211
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 5211, 백준 5211번, BOJ 5211, AMinorAndCMajor, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5211번 - 가단조와 다장조](https://www.acmicpc.net/problem/5211)

## 설명
각 마디의 첫 음에 등장하는 중심음 개수를 비교해 조성을 판별하는 문제입니다.

<br>

## 접근법
마디 시작 위치(문자열 시작 또는 `|` 뒤)의 음을 확인합니다.

다장조 중심음(C, F, G)과 가단조 중심음(A, D, E)의 등장 횟수를 세고, 동률이면 마지막 음으로 결정합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static bool IsCMajorCenter(char ch) {
    return ch == 'C' || ch == 'F' || ch == 'G';
  }

  static bool IsAMinorCenter(char ch) {
    return ch == 'A' || ch == 'D' || ch == 'E';
  }

  static void Main() {
    var s = Console.ReadLine()!;
    var cMajor = 0;
    var aMinor = 0;

    for (var i = 0; i < s.Length; i++) {
      if (i == 0 || s[i - 1] == '|') {
        var ch = s[i];
        if (IsCMajorCenter(ch)) cMajor++;
        if (IsAMinorCenter(ch)) aMinor++;
      }
    }

    if (cMajor > aMinor) Console.WriteLine("C-major");
    else if (aMinor > cMajor) Console.WriteLine("A-minor");
    else {
      var last = s[s.Length - 1];
      Console.WriteLine(IsCMajorCenter(last) ? "C-major" : "A-minor");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isCMajor(char ch) {
  return ch == 'C' || ch == 'F' || ch == 'G';
}

bool isAMinor(char ch) {
  return ch == 'A' || ch == 'D' || ch == 'E';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;
  int cMajor = 0, aMinor = 0;

  for (int i = 0; i < (int)s.size(); i++) {
    if (i == 0 || s[i - 1] == '|') {
      char ch = s[i];
      if (isCMajor(ch)) cMajor++;
      if (isAMinor(ch)) aMinor++;
    }
  }

  if (cMajor > aMinor) cout << "C-major\n";
  else if (aMinor > cMajor) cout << "A-minor\n";
  else {
    char last = s.back();
    cout << (isCMajor(last) ? "C-major" : "A-minor") << "\n";
  }

  return 0;
}
```
