---
layout: single
title: "[백준 27219] Робинзон Крузо (C#, C++) - soo:bak"
date: "2023-05-10 00:10:00 +0900"
description: 수학과 사칙 연산, 날짜 계산을 주제로 하는 백준 27219번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27219
  - C#
  - C++
  - 알고리즘
keywords: "백준 27219, 백준 27219번, BOJ 27219, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27219번 - Робинзон Крузо](https://www.acmicpc.net/problem/27219)

## 설명
로빈슨 크루소가 `n` 번째 날에 벽에 그리는 눈금을 출력한다는 컨셉의 문제입니다. <br>

입력으로 받은 `n` 을 기준으로, 벽에 그릴 `V` 의 개수를 계산하고, 마찬가지로 벽에 그릴 `I` 의 개수를 계산합니다. <br>

이후, `V` 와 `I` 를 이어서 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var cntV = n / 5;
      var cntI = n % 5;

      for (int i = 0; i < cntV; i++)
        Console.Write("V");
      for (int i = 0; i < cntI; i++)
        Console.Write("I");
      Console.WriteLine();

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

  int cntV = n / 5, cntI = n % 5;

  for (int i = 0; i < cntV; i++)
    cout << "V";
  for (int i = 0; i < cntI; i++)
    cout << "I";
  cout << "\n";

  return 0;
}
  ```
