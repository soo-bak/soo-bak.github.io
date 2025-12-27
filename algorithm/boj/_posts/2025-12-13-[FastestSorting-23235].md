---
layout: single
title: "[백준 23235] The Fastest Sorting Algorithm In The World (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 입력이 이미 정렬됐다고 가정하는 문제에서 각 테스트케이스마다 출력하는 백준 23235번 The Fastest Sorting Algorithm In The World 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23235
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 23235, 백준 23235번, BOJ 23235, FastestSorting, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23235번 - The Fastest Sorting Algorithm In The World](https://www.acmicpc.net/problem/23235)

## 설명
각 테스트케이스마다 정렬 완료 메시지를 출력하는 문제입니다.

<br>

## 접근법
입력은 이미 정렬되어 있다고 가정하므로 실제 정렬 작업이 필요 없습니다.

입력 라인을 차례로 읽다가 0이면 종료하고, 그 외에는 케이스 번호와 함께 고정된 문구를 출력합니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var idx = 1;
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      if (line.Trim() == "0") break;
      Console.WriteLine($"Case {idx}: Sorting... done!");
      idx++;
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
  int idx = 1;
  while (getline(cin, line)) {
    if (line == "0") break;
    cout << "Case " << idx++ << ": Sorting... done!\n";
  }

  return 0;
}
```
