---
layout: single
title: "[백준 20124] 모르고리즘 회장님 추천 받습니다 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: 최고 점수를 가진 사람 중 사전순으로 가장 앞선 이름을 찾는 문제
---

## 문제 링크
[20124번 - 모르고리즘 회장님 추천 받습니다](https://www.acmicpc.net/problem/20124)

## 설명
점수가 가장 높은 사람을 찾고, 동점이면 이름이 사전 순으로 가장 앞선 사람을 출력하는 문제입니다.

<br>

## 접근법
입력을 순서대로 읽으며 현재 최댓값과 이름을 갱신합니다.  
점수가 더 크면 갱신하고, 같으면 사전 순 비교로 더 앞선 이름을 선택합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var bestScore = -1;
    var bestName = "";

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var name = parts[0];
      var score = int.Parse(parts[1]);

      if (score > bestScore || (score == bestScore && string.Compare(name, bestName) < 0)) {
        bestScore = score;
        bestName = name;
      }
    }

    Console.WriteLine(bestName);
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
  int bestScore = -1;
  string bestName = "";

  for (int i = 0; i < n; i++) {
    string name;
    int score;
    cin >> name >> score;

    if (score > bestScore || (score == bestScore && name < bestName)) {
      bestScore = score;
      bestName = name;
    }
  }

  cout << bestName << "\n";

  return 0;
}
```
