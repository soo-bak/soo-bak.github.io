---
layout: single
title: "[백준 16172] 나는 친구가 적다 (Large) (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 16172번 C#, C++ 풀이 - 숫자를 제거한 문자열에서 키워드가 연속 부분 문자열로 존재하는지 확인하는 문제"
tags:
  - 백준
  - BOJ
  - 16172
  - C#
  - C++
  - 알고리즘
keywords: "백준 16172, 백준 16172번, BOJ 16172, IHaveFewFriends, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16172번 - 나는 친구가 적다 (Large)](https://www.acmicpc.net/problem/16172)

## 설명
숫자를 제거한 교과서 문자열에서 키워드가 연속 부분 문자열로 존재하는지 판단하는 문제입니다.

<br>

## 접근법
먼저 교과서 문자열에서 알파벳만 추출해 새로운 문자열을 만듭니다.

다음으로 이 문자열에서 키워드가 포함되어 있는지 확인합니다. 포함되어 있으면 1, 없으면 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = Console.ReadLine()!;
    var b = Console.ReadLine()!;

    var sb = new StringBuilder();
    foreach (var ch in t) {
      if (char.IsLetter(ch))
        sb.Append(ch);
    }

    var a = sb.ToString();
    Console.WriteLine(a.Contains(b) ? 1 : 0);
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

  string t, b; cin >> t >> b;
  string a = "";
  for (size_t i = 0; i < t.size(); i++) {
    if (isalpha(t[i]))
      a.push_back(t[i]);
  }

  cout << (a.find(b) != string::npos) << "\n";

  return 0;
}
```
