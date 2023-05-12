---
layout: single
title: "[백준 14681] 사분면 고르기 (C#, C++) - soo:bak"
date: "2023-05-12 10:30:00 +0900"
---

## 문제 링크
  [14681번 - 사분면 고르기](https://www.acmicpc.net/problem/14681)

## 설명
입력으로 주어지는 좌표가 어느 사분면에 속하는지 판별하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var x = int.Parse(Console.ReadLine()!);
      var y = int.Parse(Console.ReadLine()!);

      if (x > 0 && y > 0) Console.WriteLine("1");
      else if (x < 0 && y > 0) Console.WriteLine("2");
      else if (x < 0 && y < 0) Console.WriteLine("3");
      else Console.WriteLine("4");

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

  int x, y; cin >> x >> y;

  if (x > 0 && y > 0) cout << 1 << "\n";
  else if (x < 0 && y > 0) cout << 2 << "\n";
  else if (x < 0 && y < 0) cout << 3 << "\n";
  else cout << 4 << "\n";

  return 0;
}
  ```
