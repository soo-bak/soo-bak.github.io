---
layout: single
title: "[백준 17783] Breaking Branches (C#, C++) - soo:bak"
date: "2023-09-09 12:46:00 +0900"
description: 수학, 게임 이론, 구현 등을 주제로 하는 백준 17783번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 17783
  - C#
  - C++
  - 알고리즘
keywords: "백준 17783, 백준 17783번, BOJ 17783, BreakingBranches, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [17783번 - Breaking Branches](https://www.acmicpc.net/problem/17783)

## 설명
문제의 목표는 주어진 각 재료의 양을 사용하여 최대 몇 개의 케이크를 만들 수 있는지를 결정하는 것입니다. <br>
<br>
이를 위해서, 각 재료에 대하여 `주방에 있는 재료의 양` / `케이크 당 필요한 재료의 양` 의 최솟값을 계산하여 출력합니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      if (n % 2 == 1)
        Console.WriteLine("Bob");
      else {
        Console.WriteLine("Alice");
        Console.WriteLine(1);
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

  int n; cin >> n;

  if (n % 2 == 1) cout << "Bob\n";
  else {
    cout << "Alice\n";
    cout << 1 << "\n";
  }

  return 0;
}
  ```
