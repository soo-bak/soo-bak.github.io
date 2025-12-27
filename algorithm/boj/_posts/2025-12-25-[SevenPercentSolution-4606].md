---
layout: single
title: "[백준 4606] The Seven Percent Solution (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 4606번 C#, C++ 풀이 - 예약 문자를 퍼센트 인코딩으로 치환하는 문제"
tags:
  - 백준
  - BOJ
  - 4606
  - C#
  - C++
  - 알고리즘
keywords: "백준 4606, 백준 4606번, BOJ 4606, SevenPercentSolution, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4606번 - The Seven Percent Solution](https://www.acmicpc.net/problem/4606)

## 설명
문자열에서 지정된 예약 문자를 해당 퍼센트 인코딩으로 치환해 출력하는 문제입니다.

<br>

## 접근법
입력을 한 줄씩 읽어 `#`이면 종료합니다.  
각 문자를 확인하며 표에 해당하면 인코딩 문자열로 바꿔 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    while (true) {
      var line = Console.ReadLine();
      if (line == null || line == "#") break;
      var sb = new StringBuilder();
      foreach (var ch in line) {
        if (ch == ' ') sb.Append("%20");
        else if (ch == '!') sb.Append("%21");
        else if (ch == '$') sb.Append("%24");
        else if (ch == '%') sb.Append("%25");
        else if (ch == '(') sb.Append("%28");
        else if (ch == ')') sb.Append("%29");
        else if (ch == '*') sb.Append("%2a");
        else sb.Append(ch);
      }
      Console.WriteLine(sb.ToString());
    }
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
  while (getline(cin, line)) {
    if (line == "#") break;
    string res;
    for (char ch : line) {
      if (ch == ' ') res += "%20";
      else if (ch == '!') res += "%21";
      else if (ch == '$') res += "%24";
      else if (ch == '%') res += "%25";
      else if (ch == '(') res += "%28";
      else if (ch == ')') res += "%29";
      else if (ch == '*') res += "%2a";
      else res += ch;
    }
    cout << res << "\n";
  }

  return 0;
}
```
