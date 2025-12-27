---
layout: single
title: "[백준 10708] 크리스마스 파티 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 10708번 C#, C++ 풀이 - 각 게임의 정답 수와 타겟 보너스를 반영해 점수를 합산하는 문제"
tags:
  - 백준
  - BOJ
  - 10708
  - C#
  - C++
  - 알고리즘
keywords: "백준 10708, 백준 10708번, BOJ 10708, ChristmasParty, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10708번 - 크리스마스 파티](https://www.acmicpc.net/problem/10708)

## 설명
매 게임마다 정답을 맞힌 사람은 1점, 타겟은 추가로 오답 수만큼 점수를 얻습니다. 모든 게임의 합계를 구하는 문제입니다.

<br>

## 접근법
각 게임에서 타겟을 알고 있으므로, 모든 친구의 선택을 확인해 맞힌 사람에게 1점을 더합니다.

맞힌 사람 수를 이용해 오답 수를 계산하고, 타겟에게 추가 점수를 더합니다.

이를 M번 반복해 점수를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var m = int.Parse(Console.ReadLine()!);
    var targets = Console.ReadLine()!.Split();

    var score = new int[n];
    for (var i = 0; i < m; i++) {
      var target = int.Parse(targets[i]) - 1;
      var picks = Console.ReadLine()!.Split();

      var correct = 0;
      for (var j = 0; j < n; j++) {
        if (int.Parse(picks[j]) - 1 == target) {
          score[j]++;
          correct++;
        }
      }

      score[target] += n - correct;
    }

    for (var i = 0; i < n; i++)
      Console.WriteLine(score[i]);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vi target(m);
  for (int i = 0; i < m; i++) {
    cin >> target[i];
    target[i]--;
  }

  vi score(n, 0);
  for (int i = 0; i < m; i++) {
    int correct = 0;
    for (int j = 0; j < n; j++) {
      int pick; cin >> pick;
      if (pick - 1 == target[i]) {
        score[j]++;
        correct++;
      }
    }
    score[target[i]] += n - correct;
  }

  for (int i = 0; i < n; i++)
    cout << score[i] << "\n";

  return 0;
}
```
