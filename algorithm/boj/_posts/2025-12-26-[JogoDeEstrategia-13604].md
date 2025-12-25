---
layout: single
title: "[백준 13604] Jogo de Estratégia (C#, C++) - soo:bak"
date: "2025-12-26 01:11:06 +0900"
description: 점수 합이 최대인 마지막 플레이어를 찾는 문제
---

## 문제 링크
[13604번 - Jogo de Estratégia](https://www.acmicpc.net/problem/13604)

## 설명
플레이 순서대로 주어진 점수 합을 계산해 승자를 결정하는 문제입니다.

<br>

## 접근법
먼저 각 플레이어의 점수를 누적합니다.

다음으로 최고 점수와 같은 점수가 나올 때마다 해당 플레이어로 갱신하면 마지막에 갱신된 플레이어가 조건을 만족합니다.

마지막으로 그 플레이어 번호를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var j = int.Parse(parts[idx++]);
    var r = int.Parse(parts[idx++]);

    var score = new int[j + 1];
    var best = 1;
    for (var i = 0; i < j * r; i++) {
      var p = (i % j) + 1;
      score[p] += int.Parse(parts[idx++]);
      if (score[p] >= score[best]) best = p;
    }

    Console.WriteLine(best);
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

  int j, r;
  cin >> j >> r;

  vector<int> score(j + 1, 0);
  int best = 1;
  for (int i = 0; i < j * r; i++) {
    int p = (i % j) + 1;
    int v; cin >> v;
    score[p] += v;
    if (score[p] >= score[best]) best = p;
  }

  cout << best << "\n";
  return 0;
}
```
