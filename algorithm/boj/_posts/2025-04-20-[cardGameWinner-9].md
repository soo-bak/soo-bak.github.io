---
layout: single
title: "[백준 10801] 카드게임 (C#, C++) - soo:bak"
date: "2025-04-20 02:18:00 +0900"
description: 두 플레이어가 10장의 카드를 비교하여 각각의 승리 횟수를 계산하고 승자를 결정하는 백준 10801번 카드게임 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10801
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 10801, 백준 10801번, BOJ 10801, cardGameWinner, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10801번 - 카드게임](https://www.acmicpc.net/problem/10801)

## 설명
**두 플레이어가 각각** `10`**장의 카드를 낸 후, 각 라운드마다 더 높은 숫자를 낸 쪽이 승리하는 방식으로 전체 승부를 결정하는 문제입니다.**
<br>

- `A`와 `B`는 각각 `10`장의 카드를 한 줄씩 입력받습니다.
- 각 라운드마다 `A`와 `B`가 한 장씩 카드를 낸다고 가정하며, 다음 기준으로 승패를 결정합니다:
  - `A의 카드 > B의 카드` → A 승
  - `B의 카드 > A의 카드` → B 승
  - `같을 경우` → 무승부 (승수 증가 없음)

- 10라운드 후 승수가 더 많은 사람이 승자이며,
  - `A`가 더 많이 이긴 경우 `A`
  - `B`가 더 많이 이긴 경우 `B`
  - 승수가 같다면 `D`를 출력합니다.

## 접근법

1. `A`의 카드 10장과 `B`의 카드 10장을 각각 입력받습니다.
2. `10`번 반복하며 각 카드 쌍을 비교합니다.
3. `A`가 이긴 횟수와 `B`가 이긴 횟수를 누적 집계합니다.
4. 최종적으로 승수를 비교하여 결과를 출력합니다.

- 카드의 값 비교만으로 처리되므로 시간 복잡도는 `O(10)`, 상수 시간입니다.

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var cardA = Console.ReadLine().Split().Select(int.Parse).ToArray();
    var cardB = Console.ReadLine().Split().Select(int.Parse).ToArray();

    int aWin = 0, bWin = 0;
    for (int i = 0; i < 10; i++) {
      if (cardA[i] > cardB[i]) aWin++;
      else if (cardA[i] < cardB[i]) bWin++;
    }

    Console.WriteLine(aWin > bWin ? "A" : bWin > aWin ? "B" : "D");
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

  int cardA[10], cardB[10];
  for (int i = 0; i < 10; i++)
    cin >> cardA[i];

  for (int i = 0; i < 10; i++)
    cin >> cardB[i];

  int cntAWin = 0, cntBWin = 0;
  for (int i = 0; i < 10; i++) {
    if (cardA[i] > cardB[i]) cntAWin++;
    else if (cardA[i] < cardB[i]) cntBWin++;
  }

  if (cntAWin > cntBWin) cout << "A\n";
  else if (cntAWin < cntBWin) cout << "B\n";
  else cout << "D\n";

  return 0;
}
```
