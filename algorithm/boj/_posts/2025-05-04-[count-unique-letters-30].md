---
layout: single
title: "[백준 7600] 문자가 몇갤까 (C#, C++) - soo:bak"
date: "2025-05-04 18:12:00 +0900"
description: 대소문자를 구분하지 않고 문장에서 등장한 서로 다른 알파벳의 개수를 세는 백준 7600번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 7600
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 7600, 백준 7600번, BOJ 7600, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7600번 - 문자가 몇갤까](https://www.acmicpc.net/problem/7600)

## 설명

주어진 문장에서 **공백, 숫자, 특수문자를 제외하고**, 알파벳 문자만 고려하여 **서로 다른 알파벳의 개수**를 세는 문제입니다.

<br>
- 알파벳은 대소문자를 구분하지 않으므로 `'A'`와 `'a'`는 동일한 문자로 간주합니다.
- 각 줄은 문장 하나이며, 마지막 줄에 `#`이 입력되면 종료합니다.
- 각 문장에서 등장한 서로 다른 알파벳의 개수를 출력합니다.

<br>

## 접근법

1. 한 줄의 문자열을 입력받습니다.
2. 알파벳 문자인지 확인한 후, 대/소문자를 동일하게 처리하기 위해<br>
  모두 소문자로 변환하여 등장 여부를 기록합니다.
3. 등장한 알파벳의 종류 수를 카운트하여 출력합니다.
4. 입력이 `#`이면 종료합니다.

<br>

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    while (true) {
      var s = Console.ReadLine();
      if (s == "#") break;

      var set = new HashSet<char>();
      foreach (var c in s) {
        if (char.IsLetter(c))
          set.Add(char.ToLower(c));
      }

      Console.WriteLine(set.Count);
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
  while (getline(cin, s) && s != "#") {
    int cnt[26] = {};
    for (char c : s)
      if (isalpha(c)) cnt[tolower(c) - 'a']++;

    int ans = 0;
    for (int x : cnt)
      if (x) ans++;

    cout << ans << "\n";
  }

  return 0;
}
```
