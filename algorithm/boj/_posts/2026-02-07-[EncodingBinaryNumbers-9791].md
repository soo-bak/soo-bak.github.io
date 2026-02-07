---
layout: single
title: "[백준 9791] Encoding Binary Numbers (C#, C++) - soo:bak"
date: "2026-02-07 21:33:00 +0900"
description: "백준 9791번 C#, C++ 풀이 - 이진수를 0/1 연속 개수와 값으로 변환하는 문제"
tags:
  - 백준
  - BOJ
  - 9791
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 9791, 백준 9791번, BOJ 9791, Encoding Binary Numbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9791번 - Encoding Binary Numbers](https://www.acmicpc.net/problem/9791)

## 설명
이진수 문자열을 연속된 같은 숫자의 길이와 그 숫자를 번갈아 적어 십진수 문자열로 만드는 문제입니다.

<br>

## 접근법
같은 숫자가 이어지는 구간을 왼쪽부터 읽어, 각 구간의 길이와 숫자를 차례로 적는 런-길이 인코딩으로 결과 문자열을 만듭니다. 

예를 들어 `1111000`은 `4 1 3 0`으로 변환됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    string? line;
    while ((line = Console.ReadLine()) != null) {
      if (line == "0") break;
      var sb = new StringBuilder();
      int n = line.Length;
      int cnt = 1;
      for (int i = 1; i <= n; i++) {
        if (i < n && line[i] == line[i - 1]) {
          cnt++;
        } else {
          sb.Append(cnt).Append(line[i - 1]);
          cnt = 1;
        }
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

  string s;
  while (cin >> s) {
    if (s == "0") break;
    string out;
    int n = s.size();
    int cnt = 1;
    for (int i = 1; i <= n; i++) {
      if (i < n && s[i] == s[i - 1]) {
        cnt++;
      } else {
        out += to_string(cnt);
        out.push_back(s[i - 1]);
        cnt = 1;
      }
    }
    cout << out << "\n";
  }

  return 0;
}
```
