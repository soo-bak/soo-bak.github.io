---
layout: single
title: "[백준 5523] 경기 결과 (C#, C++) - soo:bak"
date: "2025-04-20 01:55:00 +0900"
description: 두 플레이어 간 여러 판의 경기 결과를 비교하여 각각 몇 번 승리했는지 출력하는 백준 5523번 경기 결과 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5523
  - C#
  - C++
  - 알고리즘
keywords: "백준 5523, 백준 5523번, BOJ 5523, matchVictory, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5523번 - 경기 결과](https://www.acmicpc.net/problem/5523)

## 설명
**여러 판의 1:1 경기에서 두 플레이어의 점수를 비교하여, 각각 몇 번씩 이겼는지를 출력하는 간단한 비교 문제**입니다.
<br>

- 첫 줄에 전체 경기 횟수 `n`이 주어집니다.
- 이후 `n`줄에 걸쳐 각 라운드마다 `A`와 `B`의 점수가 주어집니다.
- 점수가 높은 사람이 해당 라운드를 승리한 것으로 간주합니다.
- 각 라운드마다:
  - `A > B` → `A` 승
  - `A < B` → `B` 승
  - `A == B` → 무승부 (무시됨)

- 출력은 `A`의 승리 횟수와 `B`의 승리 횟수를 공백으로 구분하여 출력합니다.

## 접근법

1. 첫 줄에서 경기 횟수를 입력받습니다.
2. 각 라운드마다 두 정수를 입력받습니다.
3. 두 값을 비교하여 `A`와 `B`의 승리 횟수를 각각 누적합니다.
4. 무승부는 무시하고 승패만 집계합니다.
5. 두 사람의 승리 횟수를 출력합니다.

- 입력의 양이 작고 조건이 단순하므로, 반복문과 조건문으로 충분히 처리할 수 있습니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    int cntA = 0, cntB = 0;

    for (int i = 0; i < n; i++) {
      var tokens = Console.ReadLine().Split();
      int a = int.Parse(tokens[0]);
      int b = int.Parse(tokens[1]);

      if (a > b) cntA++;
      else if (b > a) cntB++;
    }

    Console.WriteLine($"{cntA} {cntB}");
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

  int cntRound; cin >> cntRound;
  int cntAWin = 0, cntBWin = 0;
  while (cntRound--) {
    int scoreA, scoreB; cin >> scoreA >> scoreB;
    if (scoreA > scoreB) cntAWin++;
    else if (scoreB > scoreA) cntBWin++;
  }
  cout << cntAWin << " " << cntBWin << "\n";

  return 0;
}
```
