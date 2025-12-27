---
layout: single
title: "[백준 17502] 클레어와 팰린드롬 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: "백준 17502번 C#, C++ 풀이 - ?로 지워진 문자를 복원해 팰린드롬 문자열을 만드는 문제"
tags:
  - 백준
  - BOJ
  - 17502
  - C#
  - C++
  - 알고리즘
keywords: "백준 17502, 백준 17502번, BOJ 17502, ClaireAndPalindrome, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17502번 - 클레어와 팰린드롬](https://www.acmicpc.net/problem/17502)

## 설명
길이가 N인 팰린드롬 문자열에서 일부 문자가 지워져 ?로 표시될 때, 원래대로 팰린드롬이 되도록 복원하는 문제입니다.

<br>

## 접근법
문자열의 양 끝에서 가운데로 오면서 i와 N-1-i를 확인합니다.

두 문자가 모두 ?면 임의의 문자로 맞추고, 하나만 ?면 다른 쪽 문자를 그대로 복사합니다.

길이가 홀수라면 가운데 문자가 ?일 수 있으므로 마지막에 한 번 더 채웁니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!.ToCharArray();

    for (var i = 0; i < n / 2; i++) {
      var j = n - 1 - i;
      if (s[i] == '?' && s[j] == '?') {
        s[i] = 'a';
        s[j] = 'a';
      } else if (s[i] == '?') s[i] = s[j];
      else if (s[j] == '?') s[j] = s[i];
    }

    if (n % 2 == 1 && s[n / 2] == '?') s[n / 2] = 'a';

    Console.WriteLine(new string(s));
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

  for (int i = 0; i < n / 2; i++) {
    int j = n - 1 - i;
    if (s[i] == '?' && s[j] == '?') {
      s[i] = 'a';
      s[j] = 'a';
    } else if (s[i] == '?') s[i] = s[j];
    else if (s[j] == '?') s[j] = s[i];
  }

  if (n % 2 == 1 && s[n / 2] == '?') s[n / 2] = 'a';

  cout << s << "\n";

  return 0;
}
```
