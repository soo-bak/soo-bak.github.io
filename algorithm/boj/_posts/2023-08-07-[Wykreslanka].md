---
layout: single
title: "[백준 8721] Wykreślanka (C#, C++) - soo:bak"
date: "2023-08-07 15:11:00 +0900"
description: 수학, 구현 등을 주제로 하는 백준 8721번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 8721
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 8721, 백준 8721번, BOJ 8721, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [8721번 - Wykreślanka](https://www.acmicpc.net/problem/8721)

## 설명
숫자 `1` 부터 시작하여, 연속된 자연수들로 이루어지는 수열을 만들기위해 몇 개의 원소를 제거해야 하는지 계산하는 문제입니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  using System.Text;
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var a = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

      int num = 1, cntDeletes = 0;
      for (int i = 0; i < n; i++) {
        if (a[i] != num) cntDeletes++;
        else num++;
      }

      Console.WriteLine(cntDeletes);

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

  vector<int> a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int num = 1, cntDeletes = 0;
  for (int i = 0; i < n; i++) {
    if (a[i] != num) cntDeletes++;
    else num++;
  }

  cout << cntDeletes << "\n";

  return 0;
}
  ```
