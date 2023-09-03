---
layout: single
title: "[백준 29064] Обучение войск (C#, C++) - soo:bak"
date: "2023-09-03 17:59:00 +0900"
description: 수학, 사칙연산, 구현 등을 주제로 하는 백준 29064번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [29064번 - Обучение войск](https://www.acmicpc.net/problem/29064)

## 설명
병사의 훈련 수준이 `1` 부터 `3` 까지의 숫자로 주어지며, `1` 이 완벽히 훈련된 상태를 나타낼 때, <br>
<br>
주어진 병사들 중에서, 최소 몇 명을 추가로 훈련시켜야 전체 병사의 절반 이상이 완벽하게 훈련되어 있는 상태가 되는지 계산하는 문제입니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var soldiers = new int[n];
      int fullyTrained = 0;
      var input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < n; i++) {
        soldiers[i] = int.Parse(input[i]);
        if (soldiers[i] == 1) fullyTrained++;
      }

      int requiredTrained = (n / 2 + n % 2) - fullyTrained;
      if (requiredTrained < 0) requiredTrained = 0;

      Console.WriteLine(requiredTrained);

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

  int n; cin >> n;

  vector<int> soldiers(n);
  int fullyTrained = 0;
  for (int i = 0; i < n; i++) {
    cin >> soldiers[i];
    if (soldiers[i] == 1) fullyTrained++;
  }

  int requiredTrained = n / 2 + n % 2 - fullyTrained;
  if (requiredTrained < 0)
    requiredTrained = 0;

  cout << requiredTrained << "\n";

  return 0;
}
  ```
