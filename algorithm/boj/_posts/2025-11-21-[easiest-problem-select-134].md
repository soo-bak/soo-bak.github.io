---
layout: single
title: "[백준 22966] 가장 쉬운 문제를 찾는 문제 (C#, C++) - soo:bak"
date: "2025-11-21 23:44:00 +0900"
description: 입력된 문제 중 난이도가 가장 낮은 문제의 제목을 출력하는 백준 22966번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 22966
  - C#
  - C++
  - 알고리즘
keywords: "백준 22966, 백준 22966번, BOJ 22966, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[22966번 - 가장 쉬운 문제를 찾는 문제](https://www.acmicpc.net/problem/22966)

## 설명

`N`개의 문제가 주어집니다. 각 문제는 제목과 난이도로 구성되며, 난이도는 `1`부터 `5`까지의 정수입니다. 수치가 작을수록 쉬운 문제입니다.<br>

가장 쉬운 문제의 제목을 출력하는 문제입니다.<br>

<br>

## 접근법

`N`개의 문제를 순회하며 가장 낮은 난이도를 가진 문제를 찾습니다.

최소 난이도와 해당 문제의 제목을 저장하며, 더 낮은 난이도를 만나면 갱신합니다.<br>

<br>
예를 들어 문제들의 난이도가 `3, 1, 2`라면, 첫 번째 문제(`3`)를 저장한 후 두 번째 문제(`1`)에서 갱신하고, 세 번째 문제(`2`)는 갱신하지 않습니다.<br>

모든 문제를 확인한 후 저장된 제목을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var answerTitle = "";
      var minDifficulty = int.MaxValue;

      for (var i = 0; i < n; i++) {
        var tokens = Console.ReadLine()!.Split();
        var title = tokens[0];
        var difficulty = int.Parse(tokens[1]);

        if (difficulty < minDifficulty) {
          minDifficulty = difficulty;
          answerTitle = title;
        }
      }

      Console.WriteLine(answerTitle);
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

  string answer;
  int minDiff = INT_MAX;
  while (n--) {
    string title; int difficulty; cin >> title >> difficulty;

    if (difficulty < minDiff) {
      minDiff = difficulty;
      answer = title;
    }
  }

  cout << answer << "\n";

  return 0;
}
```

