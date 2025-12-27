---
layout: single
title: "[백준 18127] 모형결정 (C#, C++) - soo:bak"
date: "2023-06-17 08:21:00 +0900"
description: 수열, 수학, 사칙연산 등을 주제로 하는 백준 18127번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 18127
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 18127, 백준 18127번, BOJ 18127, CristalModel, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [18127번 - 모형결정](https://www.acmicpc.net/problem/18127)

## 설명
문제의 목표는 정`a`각형에 대하여 온도 `b` 에 따라 규칙적으로 증가하는 결정의 총 갯수를 구하는 것입니다. <br>

문제에서 그림으로 주어진 규칙을 살펴보면, <br>

`a` 가 `3`, 즉, 정삼각형의 경우 총 결정의 개수는 온도 `b` 에 따라서, `1`, `3`, `6`, `10`, `15`, `...`, 이며,<br>
각 항마다 증가하는 결정의 갯수는 `2`, `3`, `4`, `5`, `...` 입니다.<br>

`a` 가 `4`, 즉, 정사각형의 경우 총 결정의 개수는 온도 `b` 에 따라서, `1`, `4`, `9`, `16`, `25`, `...`, 이며,<br>
각 항마다 증가하는 결정의 갯수는 `3`, `5`, `7`, `9`, `...` 입니다.<br>

`a` 가 `5`, 즉, 정오각형의 경우 `1`, `5`, `12`, `22`, `35`, `...`, 으로 결정의 갯수가 증가합니다.<br>
각 항마다 증가하는 결정의 갯수는 `4`, `7`, `10`, `13`, `...` 입니다.<br>

따라서, 규칙을 살펴보면 온도 `b` 에 대하여, 각 항마다 증가하는 결정의 갯수는 공차가 (`a` - `2`) 인 등차수열을 이룸을 알 수 있습니다. <br>

등차수열의 합 공식을 활용하여 총 결정의 개수의 일반항을 구하면 다음과 같습니다. <br>

`온도 b 의 결정의 개수` = (`b` + `1`) / `2` * (`2` * `1` + `b` * (`a` - `2`)) <br>

하지만, (`b` + `1`) / `2` 부분이 정수의 나눗셈이므로, (`b` + `1`) 이 홀수일 경우 소숫점 부분이 절삭되어 결과가 올바르지 않을 수 있습니다. <br>

따라서, 곱셈을 먼저 수행하도록 다음과 같이 식을 변형합니다. <br>

`온도 b 의 결정의 개수` = ((`b` + `1`) * (`2` + `b` * (`a` - `2`))) / `2` <br>

최종적으로, 위 일반항을 활용하여 결과값을 계산한 후 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');

      var a = long.Parse(input[0]);
      var b = long.Parse(input[1]);

      var minCristal = ((b + 1) * (2 + b * (a - 2))) / 2;
      Console.WriteLine(minCristal);

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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b; cin >> a >> b;

  ll minCristal = ((b + 1) * (2 + b * (a - 2))) / 2;
  cout << minCristal << "\n";

  return 0;
}
  ```
