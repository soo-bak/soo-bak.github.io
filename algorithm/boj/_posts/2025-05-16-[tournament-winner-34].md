---
layout: single
title: "[백준 12760] 최후의 승자는 누구? (C#, C++) - soo:bak"
date: "2025-05-16 19:21:00 +0900"
description: 각 플레이어가 가진 카드 중 최댓값을 비교하여 점수를 획득하는 과정을 시뮬레이션하는 백준 12760번 최후의 승자는 누구? 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 12760
  - C#
  - C++
  - 알고리즘
  - 구현
  - 정렬
  - 시뮬레이션
keywords: "백준 12760, 백준 12760번, BOJ 12760, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12760번 - 최후의 승자는 누구?](https://www.acmicpc.net/problem/12760)

## 설명

**여러 플레이어가 각자의 카드 중에서 가장 큰 값을 낼 때, 해당 라운드에서 최고값을 낸 플레이어에게 점수를 주는 게임을 시뮬레이션하는 문제입니다.**

- 플레이어 수는 `N`, 각자 가진 카드 수는 `M`입니다.
- 모든 플레이어는 각 라운드마다 자신이 가진 카드 중 가장 큰 카드를 제출합니다.
- 각 라운드에서 가장 큰 카드를 낸 플레이어는 `1점`을 획득하며, 해당 카드는 버려집니다.
- 같은 값을 낸 플레이어가 여러 명일 경우 모두 점수를 얻습니다.
- `M`번의 라운드 후, 최종적으로 가장 많은 점수를 얻은 플레이어 번호를 출력합니다.

<br>

## 접근법

먼저 각 플레이어가 가진 카드들을 우선순위 큐에 저장합니다.

이렇게 하면 매 라운드마다 **가장 큰 값을 빠르게 꺼낼 수 있기 때문**입니다.

<br>
총 `M`번의 라운드가 진행되며, 매 라운드마다 다음 과정을 반복합니다:

- 모든 플레이어의 카드 중 가장 큰 값을 비교하여 라운드의 최고값을 구합니다.
- 이후, 최고값과 같은 카드를 낸 플레이어에게 점수를 `1점`씩 부여합니다.
- 해당 라운드에서 사용된 카드는 제거합니다.

이 과정을 모두 마친 후, 점수가 가장 높은 플레이어를 탐색하여 출력합니다.

만약, 동점자가 있다면 해당 플레이어들을 **번호 오름차순으로 모두 출력**합니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int n = input[0], m = input[1];

    var cards = new List<Queue<int>>();
    for (int i = 0; i < n; i++) {
      var q = new Queue<int>(
        Console.ReadLine().Split().Select(int.Parse).OrderByDescending(x => x)
      );
      cards.Add(q);
    }

    var scores = new int[n];
    for (int round = 0; round < m; round++) {
      int max = cards.Max(q => q.Peek());
      for (int i = 0; i < n; i++) {
        if (cards[i].Peek() == max)
          scores[i]++;
        cards[i].Dequeue();
      }
    }

    int topScore = scores.Max();
    var winners = Enumerable.Range(0, n)
      .Where(i => scores[i] == topScore)
      .Select(i => i + 1);

    Console.WriteLine(string.Join(" ", winners));
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef priority_queue<int> pqi;
typedef vector<pqi> vpqi;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vpqi cards(n);
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      int x; cin >> x;
      cards[i].push(x);
    }
  }

  vi scores(n, 0);
  for (int i = 0; i < m; ++i) {
    int maxCard = 0;
    for (auto& pq : cards)
      maxCard = max(maxCard, pq.top());
    for (auto& pq : cards) {
      if (pq.top() == maxCard) ++scores[&pq - &cards[0]];
      pq.pop();
    }
  }

  int maxScore = *max_element(scores.begin(), scores.end());
  vi winners;
  for (int i = 0; i < n; ++i)
    if (scores[i] == maxScore) winners.push_back(i + 1);

  for (size_t i = 0; i < winners.size(); ++i)
    cout << winners[i] << (i + 1 == winners.size() ? "\n" : " ");

  return 0;
}
```
