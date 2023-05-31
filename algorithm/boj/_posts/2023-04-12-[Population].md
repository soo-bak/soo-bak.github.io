---
layout: single
title: "[백준 26561] Population (C#, C++) - soo:bak"
date: "2023-04-12 07:37:00 +0900"
description: 수학과 사칙연산을 주제로 하는 백준 26561번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [26561번 - Population](https://www.acmicpc.net/problem/26561)

## 설명
간단한 사칙연산 문제입니다. <br>

문제의 조건에 따라서 주어진 시간 동안 사람들이 얼마나 태어나고 죽는지 계산합니다. <br>

이후, 초기 인구에 태어난 사람의 수에서 죽은 사람의 수를 뺀 값을 더하여 최종 인구를 구하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var caseCnt = int.Parse(Console.ReadLine()!);

      for (var i = 0; i < caseCnt; i++) {
        var input = Console.ReadLine()?.Split(' ');
        var population = int.Parse(input![0]);
        var time = int.Parse(input![1]);

        var birth = time / 4;
        var death = time / 7;

        population += (birth - death);
        Console.WriteLine($"{population}");
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

  int caseCnt; cin >> caseCnt;

  for (int i = 0; i < caseCnt; i++) {
    int population, time; cin >> population >> time;

    int birth = time / 4, death = time / 7;

    population += (birth - death);
    cout << population << "\n";
  }

  return 0;
}
  ```
