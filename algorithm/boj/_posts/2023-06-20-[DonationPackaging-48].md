---
layout: single
title: "[백준 11795] Donation Packaging (C#, C++) - soo:bak"
date: "2023-06-20 08:40:00 +0900"
description: 구현과 수학, 시뮬레이션을 주제로 하는 백준 11795번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11795
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 11795, 백준 11795번, BOJ 11795, DonationPackaging, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [11795번 - Donation Packaging](https://www.acmicpc.net/problem/11795)

## 설명
기부 패키지를 하루에 몇 개나 포장할 수 있는지 계산하는 문제입니다. <br>

각 기부 패키지에는 `A`, `B`, `C` 세 가지의 세트가 모두 포함되어야 하며, <br>

배포에는 최소 `30` 개 이상의 패키지가 필요합니다. <br>

만약, 어떤 날의 패키지 수가 최소 배포 요구량보다 작다면, `NO` 를 출력합니다. <br>

배포 요구량 보다 같거나 크다면, 그 날 배포할 수 있는 패키지 개수를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var t = int.Parse(Console.ReadLine()!);

      int setA = 0, setB = 0, setC = 0;
      for (int i = 0; i < t; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var a = int.Parse(input[0]);
        var b = int.Parse(input[1]);
        var c = int.Parse(input[2]);

        setA += a;
        setB += b;
        setC += c;

        int packages = Math.Min(Math.Min(setA, setB), setC);
        if (packages < 30) Console.WriteLine("NO");
        else {
          Console.WriteLine(packages);
          setA -= packages;
          setB -= packages;
          setC -= packages;
        }
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

  int t; cin >> t;

  int setA = 0, setB = 0, setC = 0;
  for (int i = 0; i < t; i++) {
    int a, b, c; cin >> a >> b >> c;

    setA += a;
    setB += b;
    setC += c;

    int packages = min({setA, setB, setC});
    if (packages < 30) cout << "NO\n";
    else {
      cout << packages << "\n";
      setA -= packages;
      setB -= packages;
      setC -= packages;
    }
  }

  return 0;
}
  ```
