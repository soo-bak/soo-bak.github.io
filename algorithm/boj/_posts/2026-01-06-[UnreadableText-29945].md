---
layout: single
title: "[백준 29945] Loetamatu tekst (C#, C++) - soo:bak"
date: "2026-01-06 20:55:00 +0900"
description: "백준 29945번 C#, C++ 풀이 - 별표가 정확히 한 글자를 대체하는 패턴과 주어진 단어들을 매칭해 가능한 주제를 모두 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 29945
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
  - 완전 탐색
keywords: "백준 29945, 백준 29945번, BOJ 29945, Loetamatu tekst, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29945번 - Loetamatu tekst](https://www.acmicpc.net/problem/29945)

## 설명
N개의 후보 주제와 패턴 문자열이 주어집니다. 패턴은 알파벳 소문자와 별표로 이루어지며, 별표는 정확히 한 글자를 대체합니다.

패턴과 길이가 같고 별표가 아닌 위치의 문자가 모두 일치하는 후보를 찾아 입력 순서대로 모두 출력하는 문제입니다.

<br>

## 접근법
패턴과 길이가 다른 후보는 제외한 후, 길이가 같은 후보에 대해 각 위치를 비교합니다.

패턴의 문자가 별표이면 통과하고, 별표가 아니면 해당 위치의 문자가 일치해야 합니다.

이후 조건을 만족하는 후보를 모두 모아 개수와 함께 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static bool Match(string s, string pat) {
    if (s.Length != pat.Length)
      return false;
    for (int i = 0; i < s.Length; i++) {
      if (pat[i] == '*')
        continue;
      if (pat[i] != s[i])
        return false;
    }
    return true;
  }

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var words = new List<string>(n);
    for (var i = 0; i < n; i++)
      words.Add(Console.ReadLine()!);
    var pat = Console.ReadLine()!;

    var ans = new List<string>();
    foreach (var w in words) {
      if (Match(w, pat))
        ans.Add(w);
    }

    Console.WriteLine(ans.Count);
    foreach (var w in ans)
      Console.WriteLine(w);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<string> vs;

bool match(const string& s, const string& pat) {
  if (s.size() != pat.size())
    return false;
  for (size_t i = 0; i < s.size(); i++) {
    if (pat[i] == '*')
      continue;
    if (pat[i] != s[i])
      return false;
  }
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  cin >> n;
  vs words(n);
  for (int i = 0; i < n; i++)
    cin >> words[i];
  string pat;
  cin >> pat;

  vs ans;
  for (auto& w : words) {
    if (match(w, pat))
      ans.push_back(w);
  }

  cout << ans.size() << "\n";
  for (auto& w : ans)
    cout << w << "\n";

  return 0;
}
```
