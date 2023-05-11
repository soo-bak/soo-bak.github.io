---
layout: single
title: "[백준 1330] 두 수 비교하기 (C#, C++) - soo:bak"
date: "2023-05-12 08:54:00 +0900"
---

## 문제 링크
  [1330번 - 두 수 비교하기](https://www.acmicpc.net/problem/1330)

## 설명
입력으로 주어지는 두 수를 비교하는 문제입니다. <br>

두 수를 비교하여 문제의 조건에 맞는 기호를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var a = int.Parse(input[0]);
      var b = int.Parse(input[1]);

      if (a > b) Console.WriteLine(">");
      else if (a < b) Console.WriteLine("<");
      else Console.WriteLine("==");

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

  int a, b; cin >> a >> b;

  if (a > b) cout << ">\n";
  else if (a < b) cout << "<\n";
  else cout << "==\n";

  return 0;
}
  ```
