---
layout: single
title: "[백준 24264] 알고리즘의 수행 시간 3 (C#, C++) - soo:bak"
date: "2023-01-30 06:03:00 +0900"
description: 알고리즘의 수행 시간에 대하여 백준 24264번 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 24264
  - C#
  - C++
  - 알고리즘
keywords: "백준 24264, 백준 24264번, BOJ 24264, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [24264번 - 알고리즘의 수행 시간 3](https://www.acmicpc.net/problem/24264)

## 설명
  알고리즘 시간 복잡도의 기본 개념에 대한 문제입니다.

  문제에서 주어진 `코드 1` 을 보면, 각각의 반복문에서 `n` 번씩 연산을 실행하는 `이중 반복문` 의 알고리즘이 수행됩니다.

  따라서, 시간 복잡도는 빅오 표기법으로 <b>O(n<sup>2</sup>)</b> 으로 나타낼 수 있으며, <br>
  `코드 1` 의 결과값과 <b>O(n<sup>2</sup>)</b> 의 시간복잡도에 해당되는 상수를 문제의 조건에 따라 출력합니다.

  <br>
  입력으로 주어지는 `n` 의 크기는 최대 `500,000` 이지만, <br>
  `코드 1` 을 수행한 후의 결과값은 `int` 자료형의 크기를 초과할 수 있다는 점을 주의해야 합니다.


- - -

## Code
<br>
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      long.TryParse(Console.ReadLine(), out long n);

      Console.WriteLine("{0}\n{1}", n * n, 2);

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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n; cin >> n;

  cout << n * n << "\n" << 2 << "\n";

  return 0;
}
  ```
