---
layout: single
title: "[백준 21553] 암호 만들기 (C#, C++) - soo:bak"
date: "2023-06-19 08:52:00 +0900"
description: 구현과 문자열 다루기, 애드혹을 주제로 하는 백준 21553번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 21553
  - C#
  - C++
  - 알고리즘
  - 애드혹
keywords: "백준 21553, 백준 21553번, BOJ 21553, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [21553번 - 암호 만들기](https://www.acmicpc.net/problem/21553)

## 설명
문자열 `A` 와 `B` 가 공통으로 가지는 부분 문자열 중, 길이가 `K` 인 비밀번호를 `P` 라고 할 때, <br>

입력으로 문자열 `A` 와 비밀번호 `P` 가 주어질 때 가능한 문자열 `B` 를 구하는 문제입니다. <br>

다만, 공통으로 가지는 부분 문자열 중 길이가 `K` 인 문자열은 비밀번호 `P` 로 유일해야 합니다. <br>

따라서, 가장 단순한 풀이 방법은 문자열 `B` 를 비밀번호 `P` 로 하는 것입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var a = Console.ReadLine()!;
      var p = Console.ReadLine()!;

      var b = p;
      Console.WriteLine(b);

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

  string a, p; cin >> a >> p;

  string b = p;
  cout << b << "\n";

  return 0;
}
  ```
