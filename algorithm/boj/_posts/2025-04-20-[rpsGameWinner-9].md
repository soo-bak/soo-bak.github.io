---
layout: single
title: "[백준 4493] 가위 바위 보 (C#, C++) - soo:bak"
date: "2025-04-20 02:15:00 +0900"
description: 가위 바위 보 게임에서 여러 라운드의 결과를 종합해 최종 승자를 출력하는 백준 4493번 가위 바위 보 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4493
  - C#
  - C++
  - 알고리즘
keywords: "백준 4493, 백준 4493번, BOJ 4493, rpsGameWinner, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4493번 - 가위 바위 보](https://www.acmicpc.net/problem/4493)

## 설명
**여러 라운드의 가위 바위 보 게임 결과를 종합해, 최종 승자를 결정하는 문제입니다.**
<br>

- 입력은 여러 테스트케이스로 구성됩니다.
- 각 테스트케이스의 첫 줄에는 게임 라운드 수가 주어집니다.
- 이어서 각 라운드마다 두 사람이 낸 손 모양이 주어집니다:
  - `R` = 바위 (Rock)
  - `S` = 가위 (Scissors)
  - `P` = 보 (Paper)

- 승리 조건은 다음과 같습니다:
  - `바위 > 가위`, `가위 > 보`, `보 > 바위`

- 각 라운드의 승자를 판단하여 플레이어 1과 2의 승리 횟수를 누적한 후,
  게임 종료 시점에 전체 승부 결과를 출력합니다.
  - 플레이어 1이 더 많이 이긴 경우: `"Player 1"`
  - 플레이어 2가 더 많이 이긴 경우: `"Player 2"`
  - 비긴 경우: `"TIE"`

## 접근법

1. 테스트케이스 수를 입력받습니다.
2. 각 테스트케이스마다 라운드 수를 입력받고,
3. 각 라운드에서 두 사람이 낸 손 모양을 입력받아 승자를 판단합니다.
4. 조건에 따라 플레이어 1 또는 2의 승리 횟수를 증가시킵니다.
5. 모든 라운드 종료 후 승리 횟수를 비교하여 결과를 출력합니다.

## Code

### C#
```csharp
using System;

class Program {
  static bool IsWin(char me, char other) {
    return (me == 'R' && other == 'S') ||
           (me == 'S' && other == 'P') ||
           (me == 'P' && other == 'R');
  }

  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int rounds = int.Parse(Console.ReadLine());
      int p1 = 0, p2 = 0;

      for (int i = 0; i < rounds; i++) {
        var tokens = Console.ReadLine().Split();
        char a = tokens[0][0];
        char b = tokens[1][0];

        if (IsWin(a, b)) p1++;
        else if (IsWin(b, a)) p2++;
      }

      Console.WriteLine(p1 > p2 ? "Player 1" : p2 > p1 ? "Player 2" : "TIE");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;

bool isWin(char me, char other) {
  return (me == 'R' && other == 'S') || (me == 'S' && other == 'P') ||
         (me == 'P' && other == 'R');
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int r; cin >> r;
    int p1 = 0, p2 = 0;
    while (r--) {
      char a, b; cin >> a >> b;
      if (isWin(a, b)) p1++;
      else if (isWin(b, a)) p2++;
    }
    cout << (p1 > p2 ? "Player 1" : p1 < p2 ? "Player 2" : "TIE") << "\n";
  }
}
```
