---
layout: single
title: "[백준 25840] Sharing Birthdays (C#, C++) - soo:bak"
date: "2025-12-20 15:33:00 +0900"
description: "백준 25840번 C#, C++ 풀이 - 주어진 생일 목록에서 서로 다른 날짜의 개수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 25840
  - C#
  - C++
  - 알고리즘
keywords: "백준 25840, 백준 25840번, BOJ 25840, SharingBirthdays, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25840번 - Sharing Birthdays](https://www.acmicpc.net/problem/25840)

## 설명
여러 생일이 주어질 때, 서로 다른 생일의 개수를 출력하는 문제입니다.

<br>

## 접근법
집합 자료구조는 중복을 자동으로 제거하므로, 모든 생일을 집합에 넣으면 서로 다른 생일만 남습니다.

집합의 크기가 곧 서로 다른 생일의 개수입니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var set = new HashSet<string>();

    for (var i = 0; i < n; i++) {
      var s = Console.ReadLine()!;
      set.Add(s);
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

  int n; cin >> n;
  unordered_set<string> st;

  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    st.insert(s);
  }

  cout << st.size() << "\n";

  return 0;
}
```
