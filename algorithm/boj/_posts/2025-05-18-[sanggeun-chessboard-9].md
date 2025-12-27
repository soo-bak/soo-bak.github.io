---
layout: single
title: "[백준 3076] 상근이의 체스판 (C#, C++) - soo:bak"
date: "2025-05-18 02:07:19 +0900"
description: 행과 열, 너비와 높이 단위로 체스판 무늬를 확장 출력하는 백준 3076번 상근이의 체스판 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3076
  - C#
  - C++
  - 알고리즘
keywords: "백준 3076, 백준 3076번, BOJ 3076, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3076번 - 상근이의 체스판](https://www.acmicpc.net/problem/3076)

## 설명

**주어진 행(R), 열(C), 높이(A), 너비(B)에 따라 체스판 무늬를 확장하여 출력하는 문제입니다.**

- 체스판의 기본 형태는 `검정칸(X)`과 `흰칸(.)`이 번갈아 배치된 구조입니다.
- 기본 칸 하나를 `A줄 × B열`로 확대하여 구성하며, 전체 출력은 `R × A행`, `C × B열`이 됩니다.
- 좌측 상단은 항상 `'X'`로 시작합니다.

<br>

## 접근법
출력해야 할 체스판은 `R행` `C열` 크기의 기본 체스판을 각 칸마다 `A줄 × B칸` 크기로 확대하여 구성한 것입니다.

출력할 위치 `(r, c)`가 어느 원래 칸에 속하는지를 확인하기 위해,

해당 좌표를 각각 `A, B`로 나눈 몫을 이용합니다:

- `r / A` → 원래 체스판의 행 위치
- `c / B` → 원래 체스판의 열 위치

<br>
체스판의 색은 위쪽 왼쪽에서 시작하여 가로·세로 방향으로 번갈아 반복되므로,

원래 체스판의 `(i, j)` 칸이 검정 칸이 되기 위한 조건은 다음과 같습니다:

- `(i + j)`가 짝수일 경우 `검정(X)`

- `(i + j)`가 홀수일 경우 `흰색(.)`

<br>
즉, 출력 위치 `(r, c)`는 다음 조건으로 판단할 수 있습니다:

$$(r / A + c / B) \bmod 2 = 0 \Rightarrow \text{'X' 출력}$$

$$ (r / A + c / B) \bmod 2 = 1 \Rightarrow \text{'.' 출력}$$

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var rc = Console.ReadLine().Split();
    int row = int.Parse(rc[0]);
    int col = int.Parse(rc[1]);

    var hw = Console.ReadLine().Split();
    int h = int.Parse(hw[0]);
    int w = int.Parse(hw[1]);

    for (int r = 0; r < row * h; r++) {
      for (int c = 0; c < col * w; c++) {
        bool isX = (r / h) % 2 == (c / w) % 2;
        Console.Write(isX ? 'X' : '.');
      }
      Console.WriteLine();
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

  int row, col, h, w; cin >> row >> col >> h >> w;

  for (int r = 0; r < row * h; ++r) {
    for (int c = 0; c < col * w; ++c) {
      bool isX = (r / h) % 2 == (c / w) % 2;
      cout << (isX ? 'X' : '.');
    }
    cout << "\n";
  }

  return 0;
}
```
