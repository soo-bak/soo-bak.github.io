---
layout: single
title: "[백준 8794] Poniedziałki (C#, C++) - soo:bak"
date: "2023-08-17 09:59:00 +0900"
description: 수학, 구현 등을 주제로 하는 백준 8794번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 8794
  - C#
  - C++
  - 알고리즘
keywords: "백준 8794, 백준 8794번, BOJ 8794, Poneidzialki, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [8794번 - Poniedziałki](https://www.acmicpc.net/problem/8794)

## 설명
문제의 목표는 주어진 조건에 따라, 특정 연도에서 `월요일` 의 횟수를 계산하는 것입니다. <br>
<br>
풀이 과정은 다음과 같습니다.<br>
<br>
1. 첫 번째 주에서 `월요일` 의 수 계산<br>
- 연도의 첫 번째 날이 `월요일` 인 경우, 첫 번째 주에는 하나의 `월요일` 이 있습니다.<br>
- 그렇지 않으면 첫 번째 주에 `월요일` 은 없습니다.<br>
<br>
2. 연도의 나머지 일수에서 `월요일`의 수 계산<br>
- 첫 번째 주 이후의 전체 주에서 `월요일` 의 수를 계산합니다.<br>
- 나머지 일수에서 추가로 `월요일` 이 있는지 확인합니다.<br>
3. 두 결과 합산<br>
- 첫 번째 주와 나머지 주에서의 `월요일` 의 수를 합하여 총 `월요일` 의 수를 구합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var z = int.Parse(Console.ReadLine()!);
      for (int i = 0; i < z; i++) {
        var inputs = Console.ReadLine()!.Split();
        var n = int.Parse(inputs[0]);
        var m = int.Parse(inputs[1]);
        var l = int.Parse(inputs[2]);

        int firstWeekMondays = (l == 1) ? 1 : 0;

        n -= (m - l + 1);
        var otherMondays = n / m;

        var remainingDays = n % m;
        int extraMondays = (remainingDays >= 1) ? 1 : 0;

        Console.WriteLine(firstWeekMondays + otherMondays + extraMondays);
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

  int z; cin >> z;
  for (int i = 0; i < z; i++) {
    int n, m, l; cin >> n >> m >> l;

    int firstWeekMondays = (l == 1) ? 1 : 0;

    n -= (m - l + 1);
    int otherMondays = n / m;

    int reaminingDays = n % m;
    int extraMondays = (reaminingDays >= 1) ? 1 : 0;

    cout << firstWeekMondays + otherMondays + extraMondays << "\n";
  }

  return 0;
}
  ```
