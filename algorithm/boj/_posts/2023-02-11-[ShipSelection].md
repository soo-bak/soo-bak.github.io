---
layout: single
title: "[백준 10180] Ship Selection (C#, C++) - soo:bak"
date: "2023-02-11 11:36:00 +0900"
description: 수학을 주제로한 백준 10180번 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10180
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 10180, 백준 10180번, BOJ 10180, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [10180번 - Ship Selection](https://www.acmicpc.net/problem/10180)

## 설명
  간단한 수학에 대한 구현 문제입니다.<br>

  문제에서 주어지는 변수들이 많으므로, 차근 차근 각 변수간의 관계를 이해하면서 계산해 나갑니다.<br>

  `선박이 도달할 수 있는 거리` 는 `선박의 속도` * `선박이 이동 가능한 시간` 이며, <br>
  `선박이 이동 가능한 시간` 은 `선박의 남은 연료량` / `선박의 시간 당 연료 소모량` 임을 이용하면 <br>
  `n` 개의 선박들 각각에 대하여 도착지까지 도달 가능 여부를 판단할 수 있습니다.

  반복문을 통해 각 선박들에 대하여 위와 같이 판단을 진행하며, <br>
  도착지까지 도달 할 수 있는 선박들의 개수를 합산하여 출력합니다.
  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int.TryParse(Console.ReadLine(), out int cntCase);
      for (int c = 0; c < cntCase; c++) {
        string[]? input = Console.ReadLine()?.Split();
        int.TryParse(input?[0], out int n);
        int.TryParse(input?[1], out int distTarget);

        int ans = 0;
        for (int i = 0; i < n; i++) {
          input = Console.ReadLine()?.Split();
          int.TryParse(input?[0], out int velo);
          int.TryParse(input?[1], out int fuel);
          int.TryParse(input?[2], out int consume);

          double distAvail = velo * (double)fuel / consume;
          if (distAvail >= distTarget) ans++;
        }

        Console.WriteLine(ans);
      }

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase; cin >> cntCase;
  for (int c = 0; c < cntCase; c++) {
    int n, distTarget; cin >> n >> distTarget;

    int ans = 0;
    for (int i = 0; i < n; i++) {
      int velo, fuel, consume; cin >> velo >> fuel >> consume;

      double distAvail = velo * (double)fuel / consume;
      if (distAvail >= distTarget) ans++;
    }

    cout << ans << "\n";
  }

  return 0;
}
  ```
