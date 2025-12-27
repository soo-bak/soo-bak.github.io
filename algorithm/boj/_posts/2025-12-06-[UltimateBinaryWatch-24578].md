---
layout: single
title: "[백준 24578] Ultimate Binary Watch (C#, C++) - soo:bak"
date: "2025-12-06 21:40:00 +0900"
description: 4자리 시각의 각 자리를 4비트로 표현해 LED 시계를 출력하는 백준 24578번 Ultimate Binary Watch 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 24578
  - C#
  - C++
  - 알고리즘
keywords: "백준 24578, 백준 24578번, BOJ 24578, UltimateBinaryWatch, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24578번 - Ultimate Binary Watch](https://www.acmicpc.net/problem/24578)

## 설명
시각은 HHMM 형태의 4자리로 주어집니다. 네 자리 각각을 4비트로 표현해 세로 4칸짜리 LED 기둥으로 출력합니다.

출력 형식은 각 행마다 점과 별을 찍으며, 지정된 위치에 공백을 삽입합니다.

<br>

## 접근법
먼저, 문자열로 시각을 받아 각 자리 숫자를 배열에 저장합니다.

다음으로, 행을 위에서 아래로 내려가며 각 열의 비트를 확인합니다. 해당 비트가 1이면 별, 아니면 점을 출력합니다.

이후, 각 열 값을 채우고 지정된 공백을 삽입해 한 줄을 만들어 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var time = Console.ReadLine()!;
      var d = new int[4];
      for (var i = 0; i < 4; i++)
        d[i] = time[i] - '0';

      var sb = new StringBuilder();
      for (var row = 3; row >= 0; row--) {
        sb.Clear();
        for (var col = 0; col < 4; col++) {
          var ch = ((d[col] >> row) & 1) == 1 ? '*' : '.';
          sb.Append(ch);
          if (col == 0 || col == 2) sb.Append(' ');
          if (col == 1) sb.Append("   ");
        }
        Console.WriteLine(sb.ToString());
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

  string time; cin >> time;
  int d[4];
  for (int i = 0; i < 4; i++)
    d[i] = time[i] - '0';

  for (int row = 3; row >= 0; row--) {
    string line;
    for (int col = 0; col < 4; col++) {
      char ch = ((d[col] >> row) & 1) ? '*' : '.';
      line.push_back(ch);
      if (col == 0 || col == 2) line.push_back(' ');
      if (col == 1) line.append("   ");
    }
    cout << line << "\n";
  }

  return 0;
}
```
