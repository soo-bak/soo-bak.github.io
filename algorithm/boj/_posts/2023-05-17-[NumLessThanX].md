---
layout: single
title: "[백준 2439] 별 찍기 - 2 (C#, C++) - soo:bak"
date: "2023-05-17 14:41:00 +0900"
---

## 문제 링크
  [2439번 - 별 찍기 - 1](https://www.acmicpc.net/problem/2439)

## 설명
`1` 번쨰 줄부터 `n` 번쨰 줄까지, 각 줄에 공백 문자와 `*` 문자를 출력하는 문제입니다. <br>

각 줄에 출력해야하는 `*` 의 개수는 줄의 행 번호와 일치합니다. <br>

다만, `*` 문자가 우측으로 정렬되도록, 즉, 공백 문자를 `n - 행번호` 만큼 먼저 출력하여야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
          if (j <= (n - i)) Console.Write(" ");
          else Console.Write("*");
        }
        Console.WriteLine();
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

  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
      if (j <= (n - i)) cout << " ";
      else cout << "*";
    }
    cout << "\n";
  }

  return 0;
}
  ```
