---
layout: single
title: "[백준 11478] 서로 다른 부분 문자열의 개수 (C#, C++) - soo:bak"
date: "2025-12-07 03:15:00 +0900"
description: 모든 부분 문자열을 집합에 넣어 중복을 제거하는 백준 11478번 서로 다른 부분 문자열의 개수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11478
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 문자열
  - set
  - hash_set
  - tree_set
keywords: "백준 11478, 백준 11478번, BOJ 11478, DistinctSubstrings, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11478번 - 서로 다른 부분 문자열의 개수](https://www.acmicpc.net/problem/11478)

## 설명
문자열이 주어질 때, 서로 다른 부분 문자열의 개수를 구하는 문제입니다.

<br>

## 접근법
이중 반복문으로 모든 부분 문자열을 생성합니다. 시작 위치를 고정한 후 끝 위치를 늘려가며 연속한 구간의 문자열을 만듭니다.

생성된 문자열을 집합에 넣으면 중복이 자동으로 제거됩니다. 모든 부분 문자열을 처리한 후 집합의 크기가 답이 됩니다.

<br>

- - -

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var set = new HashSet<string>();
    for (var i = 0; i < s.Length; i++) {
      var tmp = "";
      for (var j = i; j < s.Length; j++) {
        tmp += s[j];
        set.Add(tmp);
      }
    }
    Console.WriteLine(set.Count);
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
  cin >> s;
  unordered_set<string> st;
  st.reserve(s.size() * s.size());

  for (int i = 0; i < (int)s.size(); i++) {
    string tmp;
    tmp.reserve(s.size() - i);
    for (int j = i; j < (int)s.size(); j++) {
      tmp.push_back(s[j]);
      st.insert(tmp);
    }
  }

  cout << st.size() << "\n";

  return 0;
}
```
