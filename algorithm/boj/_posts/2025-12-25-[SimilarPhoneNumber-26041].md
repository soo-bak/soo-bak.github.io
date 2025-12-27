---
layout: single
title: "[백준 26041] 비슷한 전화번호 표시 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 26041번 C#, C++ 풀이 - 전화번호 목록에서 특정 접두사를 갖는 항목을 세는 문제"
tags:
  - 백준
  - BOJ
  - 26041
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 26041, 백준 26041번, BOJ 26041, SimilarPhoneNumber, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[26041번 - 비슷한 전화번호 표시](https://www.acmicpc.net/problem/26041)

## 설명
문자열 A에 있는 전화번호 중 B와 다르면서 B를 접두사로 갖는 개수를 세는 문제입니다.

<br>

## 접근법
첫 줄의 전화번호들을 분리한 뒤, 각 번호가 B로 시작하면서 길이가 더 긴지 확인합니다.  
조건을 만족하는 개수를 합산해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!;
    var b = Console.ReadLine()!;
    var nums = line.Split(' ');

    var cnt = 0;
    foreach (var s in nums)
      if (s.Length > b.Length && s.StartsWith(b)) cnt++;

    Console.WriteLine(cnt);
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

  string line, b;
  getline(cin, line);
  getline(cin, b);

  int cnt = 0;
  int start = 0;
  int len = (int)line.size();
  for (int i = 0; i <= len; i++) {
    if (i == len || line[i] == ' ') {
      if (i > start) {
        int wlen = i - start;
        if (wlen > (int)b.size() && line.compare(start, b.size(), b) == 0)
          cnt++;
      }
      start = i + 1;
    }
  }

  cout << cnt << "\n";

  return 0;
}
```
