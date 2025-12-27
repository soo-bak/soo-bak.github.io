---
layout: single
title: "[백준 16099] Larger Sport Facility (C#, C++) - soo:bak"
date: "2023-05-03 19:33:00 +0900"
description: 수학과 시뮬레이션을 주제로 하는 백준 16099번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 16099
  - C#
  - C++
  - 알고리즘
keywords: "백준 16099, 백준 16099번, BOJ 16099, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [16099번 - Larger Sport Facility](https://www.acmicpc.net/problem/16099)

## 설명
간단한 수학 문제입니다. <br>

문제의 목표는 두 개의 직사각형의 면적을 비교하여, 더 큰 면적을 가진 학교의 이름을 출력하는 것입니다. <br>

만약, 두 면적이 같다면 `Tie` 를 출력합니다. <br>

문제의 조건에 따르면, 직사각형의 길이와 높이의 범위는 `int` 자료형의 범위에 포함되지만, <br>

두 값을 <b>곱하여</b> 면적을 구한다는 점에서 자료형의 크기에 주의해야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < cntCase; i++) {
        var input = Console.ReadLine()!.Split();
        var lenTel = int.Parse(input![0]);
        var widthTel = int.Parse(input![1]);
        var lenEure = int.Parse(input![2]);
        var widthEure = int.Parse(input![3]);

        long areaTel = (long)lenTel * widthTel,
             areaEure = (long)lenEure * widthEure;

        if (areaTel > areaEure) Console.WriteLine("TelecomParisTech");
        else if (areaTel < areaEure) Console.WriteLine("Eurecom");
        else Console.WriteLine("Tie");
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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase; cin >> cntCase;

  for (int i = 0; i < cntCase; i++) {
    int lenTel, widthTel, lenEure, widthEure;
    cin >> lenTel >> widthTel >> lenEure >> widthEure;

    ll areaTel = (ll)lenTel * widthTel,
       areaEure = (ll)lenEure * widthEure;

    if (areaTel > areaEure) cout << "TelecomParisTech\n";
    else if (areaTel < areaEure) cout << "Eurecom\n";
    else cout << "Tie\n";
  }

  return 0;
}
  ```
