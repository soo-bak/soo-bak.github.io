---
layout: single
title: "[백준 9771] Word Searching (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 9771번 C#, C++ 풀이 - 첫 줄 단어를 이후 모든 줄에서 부분 문자열로 몇 번 등장하는지(중복 허용) 세는 문제"
tags:
  - 백준
  - BOJ
  - 9771
  - C#
  - C++
  - 알고리즘
keywords: "백준 9771, 백준 9771번, BOJ 9771, WordSearching, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9771번 - Word Searching](https://www.acmicpc.net/problem/9771)

## 설명
첫 줄의 단어가 이후 모든 줄에서 부분 문자열로 몇 번 등장하는지 세는 문제입니다. 겹치는 경우도 각각 세며, 대소문자를 구분합니다.

<br>

## 접근법
각 줄에서 단어를 찾을 때마다 발견 위치 다음부터 다시 검색하여 겹치는 경우도 셉니다. 모든 줄에서 발견한 횟수를 합산해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var word = Console.ReadLine()!;
    var ans = 0;

    string? line;
    while ((line = Console.ReadLine()) != null) {
      for (var pos = 0; ; pos++) {
        var idx = line.IndexOf(word, pos, StringComparison.Ordinal);
        if (idx == -1) break;
        ans++;
        pos = idx;
      }
    }

    Console.WriteLine(ans);
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

  string word; getline(cin, word);
  int ans = 0;

  string line;
  while (getline(cin, line)) {
    int pos = 0;
    while (true) {
      int idx = line.find(word, pos);
      if (idx == (int)string::npos) break;
      ans++;
      pos = idx + 1;
    }
  }

  cout << ans << "\n";

  return 0;
}
```
