---
layout: single
title: "[백준 5524] 입실 관리 (C#, C++) - soo:bak"
date: "2025-04-20 02:13:00 +0900"
description: 대소문자 구분 없이 이름을 처리하기 위해 모든 문자를 소문자로 변환하는 백준 5524번 입실 관리 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5524
  - C#
  - C++
  - 알고리즘
  - 문자열
keywords: "백준 5524, 백준 5524번, BOJ 5524, lowercaseNames, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5524번 - 입실 관리](https://www.acmicpc.net/problem/5524)

## 설명
**입력으로 주어진 이름들을 모두 소문자로 변환하여 출력하는 단순 문자열 처리 문제입니다.**
<br>

- 여러 명의 이름이 대소문자를 섞어 입력으로 주어집니다.
- 이름을 통일된 형식으로 출력하기 위해 **모든 문자를 소문자로 변환**하여 출력해야 합니다.
- 이름은 알파벳 대소문자로만 구성되어 있습니다.

## 접근법

1. 먼저 이름의 개수를 입력받습니다.
2. 각 이름마다 문자열을 읽고,
3. 해당 문자열의 모든 문자를 소문자로 변환합니다.
4. 변환된 문자열을 출력합니다.

- 소문자로의 변환 과정은 `C#`에서는 `ToLower()`를, `C++`에서는 `tolower()`, 또는 아스키 코드 변환으로 처리 가능합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    while (n-- > 0) {
      string name = Console.ReadLine();
      Console.WriteLine(name.ToLower());
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

  int n; cin >> n;
  while (n--) {
    string name; cin >> name;
    for (size_t i = 0; i < name.size(); i++) {
      if (isupper(name[i])) name[i] += 32;
    }
    cout << name << "\n";
  }

  return 0;
}
```
