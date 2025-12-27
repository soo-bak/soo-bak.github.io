---
layout: single
title: "[백준 15181] Beautiful Music (C#, C++) - soo:bak"
date: "2025-12-26 03:40:00 +0900"
description: "백준 15181번 C#, C++ 풀이 - 인접 음의 간격으로 아름다움을 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 15181
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 15181, 백준 15181번, BOJ 15181, BeautifulMusic, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15181번 - Beautiful Music](https://www.acmicpc.net/problem/15181)

## 설명
연속된 음들 사이의 간격이 2, 4, 6일 때만 아름다운 음악으로 판단하는 문제입니다.

<br>

## 접근법
먼저 각 음을 0부터 6까지의 번호로 변환합니다.

다음으로 인접한 두 음의 차이를 위로 올려 계산하고, 허용된 간격인지 확인합니다.

하나라도 조건을 벗어나면 즉시 실패로 처리하고, 끝까지 통과하면 성공으로 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int NoteIndex(char c) {
    return c - 'A';
  }

  static void Main() {
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      if (line == "#") break;

      var ok = true;
      for (var i = 0; i + 1 < line.Length; i++) {
        var a = NoteIndex(line[i]);
        var b = NoteIndex(line[i + 1]);
        var diff = (b - a + 7) % 7;
        if (diff != 2 && diff != 4 && diff != 6) {
          ok = false;
          break;
        }
      }

      if (ok) Console.WriteLine("That music is beautiful.");
      else Console.WriteLine("Ouch! That hurts my ears.");
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

  string line;
  while (cin >> line) {
    if (line == "#") break;

    bool ok = true;
    for (int i = 0; i + 1 < (int)line.size(); i++) {
      int a = line[i] - 'A';
      int b = line[i + 1] - 'A';
      int diff = (b - a + 7) % 7;
      if (diff != 2 && diff != 4 && diff != 6) {
        ok = false;
        break;
      }
    }

    if (ok) cout << "That music is beautiful.\n";
    else cout << "Ouch! That hurts my ears.\n";
  }

  return 0;
}
```
