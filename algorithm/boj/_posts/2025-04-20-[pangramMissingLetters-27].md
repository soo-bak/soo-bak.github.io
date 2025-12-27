---
layout: single
title: "[백준 11091] 알파벳 전부 쓰기 (C#, C++) - soo:bak"
date: "2025-04-20 03:25:00 +0900"
description: 팬그램 여부를 판단하고 부족한 알파벳을 출력하는 백준 11091번 알파벳 전부 쓰기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11091
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 11091, 백준 11091번, BOJ 11091, pangramMissingLetters, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11091번 - 알파벳 전부 쓰기](https://www.acmicpc.net/problem/11091)

## 설명
**입력된 문장이 팬그램인지 판별하고, 아니라면 누락된 알파벳을 출력하는 문제입니다.**
<br>

- 테스트케이스 수가 주어지고, 이어서 그 수만큼의 줄이 입력됩니다.
- 각 줄마다 다음을 수행합니다:
  - 문장에서 등장한 알파벳을 모두 기록합니다.
  - `a`부터 `z`까지 모든 알파벳이 한 번 이상 등장했다면 `pangram`을 출력합니다.
  - 그렇지 않다면 `missing ` 뒤에 누락된 알파벳들을 **사전 순으로** 출력합니다.


## 접근법

1. 테스트케이스 개수를 입력받습니다.
2. 각 줄을 문자열로 입력받습니다.
3. 모든 알파벳이 등장했는지 확인합니다.
   - 모두 등장 → `"pangram"` 출력
   - 일부 누락 → `"missing "` + 누락된 알파벳 나열

- 대소문자 구분 없이 처리하며, 정렬은 기본적으로 알파벳 순입니다.


## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int count = int.Parse(Console.ReadLine());
    while (count-- > 0) {
      string s = Console.ReadLine();
      var seen = new bool[26];

      foreach (char c in s.ToLower())
        if (char.IsLetter(c)) seen[c - 'a'] = true;

      if (seen.All(x => x)) Console.WriteLine("pangram");
      else {
        Console.Write("missing ");
        for (int i = 0; i < 26; i++)
          if (!seen[i]) Console.Write((char)('a' + i));
        Console.WriteLine();
      }
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

  int t; cin >> t;
  cin.ignore();
  while (t--) {
    bitset<26> seen;
    string s; getline(cin, s);
    for (char c : s)
      if (isalpha(c)) seen[tolower(c) - 'a'] = 1;

    if (seen.all()) cout << "pangram\n";
    else {
      cout << "missing ";
      for (int i = 0; i < 26; i++)
        if (!seen[i]) cout << (char)('a' + i);
      cout << "\n";
    }
  }

  return 0;
}
```
