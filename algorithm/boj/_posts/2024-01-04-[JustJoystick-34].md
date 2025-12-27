---
layout: single
title: "[백준 30314] Just a Joystick (C#, C++) - soo:bak"
date: "2024-01-04 08:31:00 +0900"
description: 그리디 알고리즘, 문자열 등을 주제로 하는 백준 30314번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 30314
  - C#
  - C++
  - 알고리즘
  - 그리디
  - 문자열
keywords: "백준 30314, 백준 30314번, BOJ 30314, JustJoystick, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [30314번 - Just a Joystick](https://www.acmicpc.net/problem/30314)

## 설명
문제의 목표는 조이스틱을 사용하여 현재 문자에서 목표 문자로 가장 효율적으로 이동하는 횟수를 계산하는 것입니다.<br>
<br>
알파벳은 `A` 에서 `Z` 까지 순환하며, 각 문자 간의 거리를 계산하여 최소 이동 횟수를 찾아야 합니다.<br>
<br>
각 문자 간의 거리 계산을 위해 현재 문자와 목표 문자 간의 거리를 계산합니다.<br>
<br>
이 때, 알파벳이 순환하는 것을 고려하여 두 방향 모두의 거리를 계산합니다.<br>
<br>
이후, 각 문자 쌍에 대해 위 아래로 이동하는 최소 거리를 찾습니다.<br>
<br>
마지막으로, 모든 문자 쌍에 대한 최소 이동거리의 합을 계산합니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int n = int.Parse(Console.ReadLine()!);

      string currentInitials = Console.ReadLine()!;
      string targetInitials = Console.ReadLine()!;

      int totalMoves = Enumerable.Range(0, n).Sum(i => {
        int currentChar = currentInitials[i];
        int targetChar = targetInitials[i];
        int distance = Math.Abs(currentChar - targetChar);
        return Math.Min(distance, 26 - distance);
      });

      Console.WriteLine(totalMoves);

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

  string currentInitials, targetInitials;
  cin >> currentInitials >> targetInitials;

  int totalMoves = 0;
  for (int i = 0; i < n; i++) {
    int currentChar = currentInitials[i];
    int targetChar = targetInitials[i];
    int distance = abs(currentChar - targetChar);
    totalMoves += min(distance, 26 - distance);
  }

  cout << totalMoves << "\n";

  return 0;
}
  ```
