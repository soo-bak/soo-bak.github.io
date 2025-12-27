---
layout: single
title: "[백준 27213] Граничные клетки (C#, C++) - soo:bak"
date: "2023-03-29 16:18:00 +0900"
description: 수학과 구현을 주제로 하는 백준 27213번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27213
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 27213, 백준 27213번, BOJ 27213, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27213번 - Граничные клетки](https://www.acmicpc.net/problem/27213)

## 설명
간단한 수학 문제입니다. <br>

문제의 목표는 격자 무늬 종이에 `m * n` 크기의 사각형을 그렸을 때, 테두리에 존재하는 사각형의 개수를 구하는 것입니다. <br>

`m * n` 크기의 사각형에서 테두리에 존재하는 사각형의 개수는 다음과 같은 공식이 적용됩니다. <br>

`(2 * m) + (2 * n) - 4`<br>

여기서 `-4` 는 사각형의 네 꼭지점의 개수를 세는 과정에서, `가로` 와 `세로` 의 중복되는 부분에 대한 것입니다. <br>

다만, `m` 이 `1` 일 경우, &nbsp; 또는 `n` 이 `1` 일 경우에는<br>


중복되는 부분의 개수가 `1` 개 뿐이므로 해당 부분에 대한 예외 처리를 해야 합니다. <br>

위 식에 맞게 계산한 결과값을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var m = int.Parse(Console.ReadLine()!);
      var n = int.Parse(Console.ReadLine()!);

      var ans = (2 * m) + (2 * n) - 4;

      if (m == 1 || n == 1) ans = (m + n) - 1;

      Console.WriteLine(ans);

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

  int m, n; cin >> m >> n;

  int ans = (2 * m) + (2 * n) - 4;

  if (m == 1 || n == 1) ans = (m + n) - 1;

  cout << ans << "\n";

  return 0;
}
  ```
