---
layout: single
title: "[백준 1652] 누울 자리를 찾아라 (C#, C++) - soo:bak"
date: "2025-11-29 22:00:00 +0900"
description: 가로나 세로로 연속된 빈칸 길이가 2 이상인 구간을 세어 누울 자리를 구하는 백준 1652번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1652
  - C#
  - C++
  - 알고리즘
keywords: "백준 1652, 백준 1652번, BOJ 1652, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1652번 - 누울 자리를 찾아라](https://www.acmicpc.net/problem/1652)

## 설명

N × N 크기의 방 배치도가 주어지는 상황에서, N (1 ≤ N ≤ 100)과 각 칸의 상태(`.`은 빈 칸, `X`는 짐)가 주어질 때, 가로 방향과 세로 방향에서 누울 수 있는 자리의 개수를 각각 구하는 문제입니다.

연속된 빈 칸이 2개 이상이면 그 구간에 누울 수 있으며, 한 구간은 하나의 자리로 카운트됩니다.

<br>

## 접근법

가로 방향과 세로 방향을 각각 확인하여 연속된 빈 칸의 개수를 셉니다.

각 행을 왼쪽에서 오른쪽으로 순회하면서 연속된 빈 칸의 길이를 추적합니다. 연속 길이가 2가 되는 순간 누울 수 있는 자리가 하나 생기며, 그 이후는 같은 구간이므로 추가로 카운트하지 않습니다.

세로 방향도 동일한 방식으로 각 열을 위에서 아래로 순회하며 처리합니다.

<br>
예를 들어, 다음과 같은 방이 있다면:

```
..X..
.....
XX...
```

- 가로: 1행에 `.X.` 구간 없음 (연속 2개 미만), 2행에 `.....` 구간 1개, 3행에 `...` 구간 1개 → 총 2개
- 세로: 1열에 `..X` 구간 1개, 2열에 `...` 구간 1개, 3열 없음, 4열에 `...` 구간 1개, 5열에 `...` 구간 1개 → 총 4개

<br>
각 칸을 한 번씩만 확인하므로 시간 복잡도는 O(N²)입니다.

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
      var room = new char[n, n];
      for (var r = 0; r < n; r++) {
        var line = Console.ReadLine()!;
        for (var c = 0; c < n; c++)
          room[r, c] = line[c];
      }

      var horizontal = 0;
      var vertical = 0;

      for (var r = 0; r < n; r++) {
        var length = 0;
        for (var c = 0; c < n; c++) {
          if (room[r, c] == '.') length++;
          else length = 0;
          if (length == 2) horizontal++;
        }
      }

      for (var c = 0; c < n; c++) {
        var length = 0;
        for (var r = 0; r < n; r++) {
          if (room[r, c] == '.') length++;
          else length = 0;
          if (length == 2) vertical++;
        }
      }

      Console.WriteLine($"{horizontal} {vertical}");
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<char> vc;
typedef vector<vc> vvc;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvc room(n, vc(n));
  for (int r = 0; r < n; r++) {
    for (int c = 0; c < n; c++) {
      cin >> room[r][c];
    }
  }

  int horizontal = 0, vertical = 0;

  for (int r = 0; r < n; r++) {
    int length = 0;
    for (int c = 0; c < n; c++) {
      if (room[r][c] == '.') length++;
      else length = 0;
      if (length == 2) horizontal++;
    }
  }

  for (int c = 0; c < n; c++) {
    int length = 0;
    for (int r = 0; r < n; r++) {
      if (room[r][c] == '.') length++;
      else length = 0;
      if (length == 2) vertical++;
    }
  }

  cout << horizontal << " " << vertical << "\n";
  
  return 0;
}
```


