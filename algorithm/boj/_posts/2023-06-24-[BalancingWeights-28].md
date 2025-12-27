---
layout: single
title: "[백준 11131] Balancing Weights (C#, C++) - soo:bak"
date: "2023-06-24 10:18:00 +0900"
description: 수학, 물리학, 토크, 돌림힘 등을 주제로 하는 백준 11131번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11131
  - C#
  - C++
  - 알고리즘
keywords: "백준 11131, 백준 11131번, BOJ 11131, BalancingWeights, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [11131번 - Balancing Weights](https://www.acmicpc.net/problem/11131)

## 설명
물리학의 돌림힘(Torque)을 활용하여, 추가 달린 레버가 어느 방향으로 기울어질지 판단하는 문제입니다. <br>

<br>
돌림힘이란 어떤 물체를 회전시키는 힘을 나타내며, 다음과 같이 정의됩니다. <br>

`τ` = `F` * `r` * `sinθ`, (`r`은 회전축에서 힘의 작용점까지의 거리, `F` 는 가해진 힘, `θ` 는 힘의 방향과 `r` 사이의 각도) <br>

<br>
문제에서는 모든 추의 무게 작용점에 대하여 `θ` 가 `90`으로 동일하며, 질량에 작용하는 가속도는 동일하다는 전제가 있습니다. <br>

따라서, 힘 `F` 는 질량 `m` * 가속도 `a` 로 표현되므로, 가속도 `a` 가 일정하다면, <br>

단순히 `τ` = `m` * `d` , (`m` 은 추의 질량, `d` 는 회전축에서 힘의 작용점까지의 거리) 로 돌림힘을 계산할 수 있습니다. <br>

<br>
따라서, 입력으로 주어지는 각 추의 무게에 대한 돌림힘을 모두 합산하여, 총 돌림힘을 계산하여 레버가 어느 방향으로 회전할지 결정하여 출력합니다. <br>

돌림힘의 총합이 `0` 이면, 균형 상태(`"Equilibrium"`), 양수이면 오른쪽(`"Right"`), 음수이면 왼쪽(`"Left"`) 으로 회전합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int t = 0; t < cntCase; t++) {
        var n = int.Parse(Console.ReadLine()!);

        var w = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

        int torque = 0;
        for (int i = 0; i < n; i++)
          torque += 100 * w[i];

        if (torque == 0) Console.WriteLine("Equilibrium");
        else if (torque > 0) Console.WriteLine("Right");
        else Console.WriteLine("Left");
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

  for (int t = 0; t < cntCase; t++) {
    int n; cin >> n;

    vector<int> w(n);
    for (int i = 0; i < n; i++)
      cin >> w[i];

    int torque = 0;
    for (int i = 0; i < n; i++)
      torque += 100 * w[i];

    if (torque == 0) cout << "Equilibrium\n";
    else if (torque > 0) cout << "Right\n";
    else cout << "Left\n";
  }

  return 0;
}
  ```
