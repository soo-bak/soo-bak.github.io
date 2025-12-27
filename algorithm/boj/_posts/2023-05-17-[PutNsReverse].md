---
layout: single
title: "[백준 2742] 기찍 N (C#, C++) - soo:bak"
date: "2023-05-17 12:41:00 +0900"
description: 반복문과 구현을 주제로 하는 백준 2742번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2742
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 2742, 백준 2742번, BOJ 2742, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2742번 - 기찍 N](https://www.acmicpc.net/problem/2742)

## 설명
반복문을 이용하여 입력으로 주어지는 `n` 부터 `1` 까지의 숫자를 내림 차순으로 출력하는 간단한 문제입니다. <br>

`C#` 에서는 `StringBuilder` 를 사용하지 않으면 `시간 초과` 가 됨에 주의합니다. <br>

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

      var sb = new StringBuilder();

      for (int i = n; i >= 1; i--)
        sb.AppendLine(i.ToString());

      Console.Write(sb);

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

  for (int i = n; i >= 1; i--)
    cout << i << "\n";

  return 0;
}
  ```
