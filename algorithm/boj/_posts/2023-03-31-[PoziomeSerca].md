---
layout: single
title: "[백준 26772] Poziome serca (C#, C++) - soo:bak"
date: "2023-03-31 20:24:00 +0900"
description: 구현을 주제로 하는 백준 26772번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [26772번 - Poziome serca](https://www.acmicpc.net/problem/26772)

## 설명
간단한 구현 문제입니다. <br>

문제에 나타나 있는 하트 모양 문자열을 입력으로 주어지는 `n` 개 만큼 가로로 출력합니다. <br>

주의해야 할 점은 <b>하트와 하트 사이가 반드시 1개의 공백으로 구분되어져야 된다는 점</b> 입니다. <br>

또한, <b>C#</b> 으로 풀이할 시 `StringBuilder` 를 사용하지 않으면 <b>시간 초과</b>가 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      string[] heart = {
        " @@@   @@@ ",
        "@   @ @   @",
        "@    @    @",
        "@         @",
        " @       @ ",
        "  @     @  ",
        "   @   @   ",
        "    @ @    ",
        "     @     "
      };

      var sb = new System.Text.StringBuilder();

      var n = int.Parse(Console.ReadLine()!);

      for (var i = 0; i < 9; i++) {
        for (var j = 0; j < n; j++) {
          sb.Append(heart[i]);
          if (j != n - 1) sb.Append(" ");
        }
        sb.AppendLine();
      }

      Console.Write(sb.ToString());

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

  const string heart[9] = {
    " @@@   @@@ ",
    "@   @ @   @",
    "@    @    @",
    "@         @",
    " @       @ ",
    "  @     @  ",
    "   @   @   ",
    "    @ @    ",
    "     @     "
  };

  int n; cin >> n;

  for (int i = 0; i < 9; i++) {
    for (int j = 0; j < n; j++) {
      cout << heart[i];
      if (j != n - 1) cout << " ";
    }
    cout << "\n";
  }

  return 0;
}
  ```
