---
layout: single
title: "[백준 17219] 비밀번호 찾기 (C#, C++) - soo:bak"
date: "2025-11-14 23:45:00 +0900"
description: 사이트 주소를 키로 비밀번호를 저장해 즉시 조회하는 백준 17219번 비밀번호 찾기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17219
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - set
  - hash_set
keywords: "백준 17219, 백준 17219번, BOJ 17219, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17219번 - 비밀번호 찾기](https://www.acmicpc.net/problem/17219)

## 설명

`N`개의 사이트 주소와 비밀번호 쌍이 주어진 후, `M`개의 사이트 주소에 대해 저장된 비밀번호를 찾아 출력하는 문제입니다.<br>

사이트 주소는 중복되지 않으며, 조회하는 주소는 항상 저장된 주소임이 보장됩니다.<br>

<br>

## 접근법

해시맵을 사용하여 사이트 주소를 키, 비밀번호를 값으로 저장합니다.

먼저 `N`개의 사이트 주소와 비밀번호 쌍을 입력받아 해시맵에 저장합니다.

이후 `M`개의 조회 요청에 대해 해시맵에서 사이트 주소를 키로 사용하여 비밀번호를 찾아 출력합니다.

해시맵을 사용하면 각 조회를 `O(1)` 시간에 처리할 수 있습니다.

C#에서는 `Dictionary<string, string>`을, C++에서는 `unordered_map<string, string>`을 사용합니다.

입력 크기가 최대 `100,000`개이므로 빠른 입출력을 사용합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var n = tokens[0];
      var m = tokens[1];

      var book = new Dictionary<string, string>(n);
      for (var i = 0; i < n; i++) {
        var entry = Console.ReadLine()!.Split();
        book[entry[0]] = entry[1];
      }

      var answers = new string[m];
      for (var i = 0; i < m; i++) {
        var site = Console.ReadLine()!;
        answers[i] = book[site];
      }

      Console.WriteLine(string.Join("\n", answers));
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

  int n, m; cin >> n >> m;

  unordered_map<string, string> book;
  book.reserve(n * 2);
  for (int i = 0; i < n; ++i) {
    string site, pwd; cin >> site >> pwd;
    book[site] = pwd;
  }

  while (m--) {
    string site; cin >> site;
    cout << book[site] << "\n";
  }

  return 0;
}
```

