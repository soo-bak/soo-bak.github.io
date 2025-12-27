---
layout: single
title: "[백준 21573] Кондиционер (C#, C++) - soo:bak"
date: "2024-01-30 20:06:00 +0900"
description: 구현, 문자열, 많은 조건 분기 등을 주제로 하는 백준 21573번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 21573
  - C#
  - C++
  - 알고리즘
keywords: "백준 21573, 백준 21573번, BOJ 21573, Conditioner, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [21573번 - Кондиционер](https://www.acmicpc.net/problem/21573)

## 설명
문제의 목표는 주어지는 방의 현재 온도, 에어컨의 설정 목표 온도, 그리고 에어컨의 작동 모드에 따라서, 한 시간 후 방의 온도를 계산하는 것입니다.<br>
<br>
에어컨의 작동 모드는 `freeze`, `heat`, `auto`, `fan` 의 네 가지가 있으며, 각 모드는 다음과 같이 작동합니다 : <br>
<br><br>
- `freeze` : 온도를 낮출 수만 있습니다. 만약, 방의 온도가 목표 온도보다 낮거나 같다면, 온도는 변하지 않습니다.<br>
<br>
- `heat` : 온도를 높일 수만 있습니다. 만약, 방의 온도가 목표 온도보다 높거나 같다면, 온도는 변하지 않습니다. <br>
<br>
- `auto` : 온도를 목표 온도로 정확히 맞출 수 있습니다.<br>
<br>
- `fan` : 방의 공기를 순환시키기만 하며, 온도는 변하지 않습니다.<br>
<br><br>

위 내용을 바탕으로, 각 모드에 따라 계산된 온도를 출력합니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var inputs = Console.ReadLine()!.Split(' ');

      var troom = int.Parse(inputs[0]);
      var tcond = int.Parse(inputs[1]);

      var mode = Console.ReadLine()!;

      var result = troom;
      if (mode == "freeze") result = Math.Min(troom, tcond);
      else if (mode == "heat") result = Math.Max(troom, tcond);
      else if (mode == "auto") result = tcond;

      Console.WriteLine(result);

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

  int troom, tcond;
  string mode;
  cin >> troom >> tcond >> mode;

  int result = troom;
  if (mode == "freeze") result = min(troom, tcond);
  else if (mode == "heat") result = max(troom, tcond);
  else if (mode == "auto") result = tcond;

  cout << result << "\n";

  return 0;
}
  ```
