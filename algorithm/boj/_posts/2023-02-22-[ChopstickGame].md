---
layout: single
title: "[백준 25642] 젓가락 게임 (C#, C++) - soo:bak"
date: "2023-02-22 15:13:00 +0900"
description: 시뮬레이션을 주제로한 백준 25642번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [25642번 - 젓가락 게임](https://www.acmicpc.net/problem/25642)

## 설명
  간단한 시뮬레이션 및 구현 문제입니다. <br>

  문제에서 주어진 `게임의 진행 과정` 에 따라서 시뮬레이션을 구현합니다.<br>

  문제의 게임 진행과정 설명은 다소 딱딱하게 설명되어 있지만, <br>
  문제의 제목처럼, 어렸을 때 친구들과 즐겨 했던 `젓가락 게임` 을 연상하시면 쉽게 이해가 가능합니다.
  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      string[]? input = Console.ReadLine()?.Split();

      int.TryParse(input![0], out int a);
      int.TryParse(input![1], out int b);

      while (true) {
        b += a;
        if (b >= 5) {
          Console.WriteLine("yt");
          return ;
        }

        a += b;
        if (a >= 5) {
          Console.WriteLine("yj");
          return ;
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

  int a, b; cin >> a >> b;

  while (true) {
    b += a;
    if (b >= 5) {
      cout << "yt\n"; return 0;
    }

    a += b;
    if (a >= 5) {
      cout << "yj\n"; return 0;
    }
  }

  return 0;
}
  ```
