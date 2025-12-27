---
layout: single
title: "[백준 4470] 줄 번호 (C#, C++) - soo:bak"
date: "2025-04-20 01:51:00 +0900"
description: 각 문장의 앞에 줄 번호를 붙여 출력하는 백준 4470번 줄 번호 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4470
  - C#
  - C++
  - 알고리즘
keywords: "백준 4470, 백준 4470번, BOJ 4470, numberedSentences, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4470번 - 줄 번호](https://www.acmicpc.net/problem/4470)

## 설명
**여러 줄의 문자열을 입력받고, 각 줄의 앞에 줄 번호를 붙여 출력하는 단순 구현 문제**입니다.
<br>

- 첫 줄에 입력될 줄의 개수 `n`이 주어집니다.
- 이후 `n`개의 줄에 걸쳐 문자열이 주어지며, 각 줄 앞에 `"줄 번호. "` 형식으로 번호를 붙여 출력해야 합니다.
- 줄 번호는 `1`부터 시작합니다.

## 접근법

1. 첫 줄에서 정수 `n`을 입력받습니다.
2. `n`번 반복하여 각 줄의 문자열을 읽습니다.
3. 읽은 각 줄 앞에 현재 반복 순번을 `"i. "` 형태로 붙여 출력합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    for (int i = 1; i <= n; i++) {
      string line = Console.ReadLine();
      Console.WriteLine(i + ". " + line);
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

  string cntLine; getline(cin, cntLine);
  int numLine = 1;
  for (int i = 0; i < stoi(cntLine); i++) {
    cout << numLine << ". ";
    string str; getline(cin, str);
    cout << str << "\n";
    numLine++;
  }

  return 0;
}
```
