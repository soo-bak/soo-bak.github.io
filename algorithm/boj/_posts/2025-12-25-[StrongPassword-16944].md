---
layout: single
title: "[백준 16944] 강력한 비밀번호 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 16944번 C#, C++ 풀이 - 필요한 문자 종류를 확인해 최소 추가 길이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 16944
  - C#
  - C++
  - 알고리즘
keywords: "백준 16944, 백준 16944번, BOJ 16944, StrongPassword, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16944번 - 강력한 비밀번호](https://www.acmicpc.net/problem/16944)

## 설명
주어진 문자열 S가 규칙을 만족하도록 뒤에 추가해야 하는 최소 문자 수를 구하는 문제입니다.

<br>

## 접근법
소문자, 대문자, 숫자, 특수문자 포함 여부를 확인해 부족한 종류 개수를 셉니다.  
길이 조건(6 이상)과 부족한 종류 개수 중 큰 값을 답으로 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var special = "!@#$%^&*()-+";

    var hasLower = false;
    var hasUpper = false;
    var hasDigit = false;
    var hasSpecial = false;

    foreach (var c in s) {
      if (c >= 'a' && c <= 'z') hasLower = true;
      else if (c >= 'A' && c <= 'Z') hasUpper = true;
      else if (c >= '0' && c <= '9') hasDigit = true;
      else if (special.IndexOf(c) >= 0) hasSpecial = true;
    }

    var need = 0;
    if (!hasLower) need++;
    if (!hasUpper) need++;
    if (!hasDigit) need++;
    if (!hasSpecial) need++;

    var add = 6 - n;
    if (add < 0) add = 0;
    Console.WriteLine(Math.Max(need, add));
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

  int n; cin >> n;
  string s; cin >> s;
  string special = "!@#$%^&*()-+";

  bool hasLower = false, hasUpper = false, hasDigit = false, hasSpecial = false;
  for (char c : s) {
    if ('a' <= c && c <= 'z') hasLower = true;
    else if ('A' <= c && c <= 'Z') hasUpper = true;
    else if ('0' <= c && c <= '9') hasDigit = true;
    else if (special.find(c) != string::npos) hasSpecial = true;
  }

  int need = 0;
  if (!hasLower) need++;
  if (!hasUpper) need++;
  if (!hasDigit) need++;
  if (!hasSpecial) need++;

  int add = 6 - n;
  if (add < 0) add = 0;
  cout << max(need, add) << "\n";

  return 0;
}
```
