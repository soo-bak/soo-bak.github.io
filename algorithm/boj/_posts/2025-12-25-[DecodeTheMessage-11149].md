---
layout: single
title: "[백준 11149] Decode the Message (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 11149번 C#, C++ 풀이 - 단어 합의 27 나머지로 메시지를 복원하는 문제"
tags:
  - 백준
  - BOJ
  - 11149
  - C#
  - C++
  - 알고리즘
keywords: "백준 11149, 백준 11149번, BOJ 11149, DecodeTheMessage, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11149번 - Decode the Message](https://www.acmicpc.net/problem/11149)

## 설명
단어의 알파벳 값 합을 27로 나눈 나머지로 글자를 복원하는 문제입니다.

<br>

## 접근법
각 단어마다 a=0, b=1, …, z=25로 변환해 합을 구하고 27로 나눈 값을 얻습니다.  
나머지가 0~25면 해당 알파벳, 26이면 공백을 출력해 문장을 복원합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    for (var caseNo = 0; caseNo < t; caseNo++) {
      var line = Console.ReadLine()!;
      var words = line.Split(' ');
      foreach (var w in words) {
        var sum = 0;
        foreach (var ch in w)
          sum += ch - 'a';
        var r = sum % 27;
        if (r == 26) sb.Append(' ');
        else sb.Append((char)('a' + r));
      }
      sb.AppendLine();
    }

    Console.Write(sb);
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

  int t; cin >> t;
  string line; getline(cin, line);

  while (t--) {
    getline(cin, line);
    stringstream ss(line);
    string w;
    while (ss >> w) {
      int sum = 0;
      for (char ch : w) sum += ch - 'a';
      int r = sum % 27;
      if (r == 26) cout << ' ';
      else cout << char('a' + r);
    }
    cout << "\n";
  }

  return 0;
}
```
