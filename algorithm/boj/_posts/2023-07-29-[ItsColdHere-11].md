---
layout: single
title: "[백준 6830] It's Cold Here! (C#, C++) - soo:bak"
date: "2023-07-29 14:09:00 +0900"
description: 문자열, 구현 등을 주제로 하는 백준 6830번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6830
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 6830, 백준 6830번, BOJ 6830, ItsColdHere, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6830번 - It's Cold Here!](https://www.acmicpc.net/problem/6830)

## 설명
입력으로 주어지는 도시들 중 가장 추운 온도를 가진 도시의 이름을 출력하는 문제입니다. <br>

<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int minTemp = 201;
      string coldestCity = "";
      while (true) {
        var input = Console.ReadLine()!.Split(' ');
        string city = input[0];
        var temp = int.Parse(input[1]);

        if (temp < minTemp) {
          minTemp = temp;
          coldestCity = city;
        }

        if (city == "Waterloo") break ;
      }

      Console.WriteLine(coldestCity);

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

  int minTemp = 201;
  string coldestCity;
  while (true) {
    string city; int temp; cin >> city >> temp;

    if (temp < minTemp) {
      minTemp = temp;
      coldestCity = city;
    }

    if (city == "Waterloo") break ;
  }

  cout << coldestCity << "\n";

  return 0;
}
  ```
