---
layout: single
title: "[백준 27328] 三方比較 (Three-Way Comparison) (C#, C++) - soo:bak"
date: "2023-05-05 18:25:00 +0900"
description: 수학과 두 정수의 비교를 주제로 하는 백준 27328번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [27328번 - 三方比較 (Three-Way Comparison)](https://www.acmicpc.net/problem/27328)

## 설명
두 정수를 비교하는 간단한 문제입니다. <br>

입력으로 정수 `a` 와 정수 `b` 를 비교하여, 다음과 같이 출력합니다. <br>

- `a` 가 `b` 보다 작은 경우 `-1` 을 출력 <br>
- `a` 가 `b` 보다 큰 경우 `1` 을 출력 <br>
- `a` 와 `b` 가 같은 경우 `0` 을 출력 <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var a = int.Parse(Console.ReadLine()!);
      var b = int.Parse(Console.ReadLine()!);

      if (a < b) Console.WriteLine("-1");
      else if (a > b) Console.WriteLine("1");
      else Console.WriteLine("0");
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

  if (a < b) cout << "-1\n";
  else if (a > b) cout << "1\n";
  else cout << "0\n";

  return 0;
}
  ```
