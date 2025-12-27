---
layout: single
title: "[백준 6794] What is n, Daddy? (C#, C++) - soo:bak"
date: "2023-06-21 08:48:00 +0900"
description: 수학, 전처리 등을 주제로 하는 백준 6794번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6794
  - C#
  - C++
  - 알고리즘
keywords: "백준 6794, 백준 6794번, BOJ 6794, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6794번 - What is n, Daddy?](https://www.acmicpc.net/problem/6794)

## 설명
주어진 숫자를 양손의 총 `10` 개의 손가락으로 표현한다고 할 때, <br>

총 몇 가지 방법으로 표현할 수 있는지를 계산하는 문제입니다. <br>

표현하는 손가락의 개수가 같고 손의 위치만 다른 경우에 대해서는 하나의 경우로 취급한다는 점에 주의합니다. <br>

에를 들어, 숫자 `4` 를 왼손 `3`, 오른손 `1` 로 표현하는 경우와 왼손 `1`, 오른손 `3` 으로 표현하는 경우는 하나로 취급합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int cnt = 0;
      for (int i = 0; i <= 5; i++)
        if (n - i <= 5 && n - i >= i) cnt++;

      Console.WriteLine(cnt);

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

  int cnt = 0;
  for (int i = 0; i <= 5; i++)
    if (n - i <= 5 && n - i >= i) cnt++;

  cout << cnt << "\n";

  return 0;
}
  ```
