---
layout: single
title: "[백준 2346] 풍선 터뜨리기 (C#, C++) - soo:bak"
date: "2026-03-14 23:42:00 +0900"
description: "백준 2346번 C#, C++ 풀이 - 원형으로 놓인 풍선을 순서대로 터뜨리는 시뮬레이션 문제"
tags:
  - 백준
  - BOJ
  - 2346
  - C#
  - C++
  - 알고리즘
  - 시뮬레이션
  - 자료 구조
keywords: "백준 2346, 백준 2346번, BOJ 2346, 풍선 터뜨리기, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2346번 - 풍선 터뜨리기](https://www.acmicpc.net/problem/2346)

## 설명
원형으로 배치된 풍선들을 차례로 터뜨리면서, 각 풍선 안에 적힌 숫자만큼 다음 위치로 이동해 터뜨리는 순서를 구하는 문제입니다.

<br>

## 접근법
각 풍선을 `(번호, 이동값)` 형태로 저장한 뒤, 현재 위치의 풍선을 하나씩 제거하며 시뮬레이션합니다.

풍선을 하나 터뜨리면 원형 배열의 크기가 1 줄어듭니다. 이후 다음 위치는 남은 풍선 개수로 나눈 나머지를 이용해 계산할 수 있습니다.

- 이동값이 양수라면, 이미 현재 풍선은 제거되었으므로 `이동값 - 1`만큼 더 이동합니다.
- 이동값이 음수라면, 왼쪽으로 그대로 `이동값`만큼 이동한 효과를 내면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine()!);
    int[] moves = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    var balloons = new List<(int index, int move)>();
    for (int i = 0; i < n; i++)
      balloons.Add((i + 1, moves[i]));

    int pos = 0;
    var sb = new StringBuilder();

    while (balloons.Count > 0) {
      var current = balloons[pos];
      balloons.RemoveAt(pos);

      if (sb.Length > 0)
        sb.Append(' ');
      sb.Append(current.index);

      if (balloons.Count == 0)
        break;

      int size = balloons.Count;
      if (current.move > 0) {
        pos = (pos + current.move - 1) % size;
      } else {
        pos = (pos + current.move) % size;
        if (pos < 0)
          pos += size;
      }
    }

    Console.WriteLine(sb.ToString());
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

  int n;
  cin >> n;

  vector<pair<int, int>> balloons;
  balloons.reserve(n);
  for (int i = 0; i < n; i++) {
    int move;
    cin >> move;
    balloons.push_back({i + 1, move});
  }

  int pos = 0;
  vector<int> order;
  order.reserve(n);

  while (!balloons.empty()) {
    auto current = balloons[pos];
    balloons.erase(balloons.begin() + pos);
    order.push_back(current.first);

    if (balloons.empty())
      break;

    int size = (int)balloons.size();
    if (current.second > 0) {
      pos = (pos + current.second - 1) % size;
    } else {
      pos = (pos + current.second) % size;
      if (pos < 0)
        pos += size;
    }
  }

  for (int i = 0; i < (int)order.size(); i++) {
    if (i > 0)
      cout << ' ';
    cout << order[i];
  }
  cout << "\n";

  return 0;
}
```
