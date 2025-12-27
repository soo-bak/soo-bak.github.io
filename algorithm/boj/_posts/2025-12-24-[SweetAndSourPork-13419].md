---
layout: single
title: "[백준 13419] 탕수육 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 13419번 C#, C++ 풀이 - 문자열 길이의 홀짝에 따라 번갈아 말하게 되는 최소 패턴을 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 13419
  - C#
  - C++
  - 알고리즘
keywords: "백준 13419, 백준 13419번, BOJ 13419, SweetAndSourPork, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13419번 - 탕수육](https://www.acmicpc.net/problem/13419)

## 설명
주어진 문자열로 게임을 했을 때, 먼저 말하는 사람과 나중에 말하는 사람이 기억해야 할 최소 문자열을 출력하는 문제입니다.

<br>

## 접근법
말하는 순서는 문자열 인덱스를 따라가며 번갈아 진행됩니다.

길이가 짝수면 시작 플레이어는 짝수 인덱스만, 다음 플레이어는 홀수 인덱스만 반복하면 됩니다.

길이가 홀수면 한 바퀴가 끝날 때 순서가 바뀌므로, 짝수 인덱스 뒤에 홀수 인덱스를 이어서 사용해야 합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static string Build(string s, int start, bool oddLength) {
    var sb = new StringBuilder();
    for (var i = start; i < s.Length; i += 2)
      sb.Append(s[i]);
    if (oddLength) {
      for (var i = 1 - start; i < s.Length; i += 2)
        sb.Append(s[i]);
    }
    return sb.ToString();
  }

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var outSb = new StringBuilder();
    for (var i = 0; i < t; i++) {
      var s = Console.ReadLine()!;
      var odd = s.Length % 2 == 1;
      outSb.AppendLine(Build(s, 0, odd));
      outSb.AppendLine(Build(s, 1, odd));
    }
    Console.Write(outSb.ToString());
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

string build(const string& s, int start, bool oddLen) {
  string res;
  for (int i = start; i < (int)s.size(); i += 2)
    res.push_back(s[i]);
  if (oddLen) {
    for (int i = 1 - start; i < (int)s.size(); i += 2)
      res.push_back(s[i]);
  }
  return res;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;
    bool odd = s.size() % 2 == 1;
    cout << build(s, 0, odd) << "\n";
    cout << build(s, 1, odd) << "\n";
  }

  return 0;
}
```
