---
layout: single
title: "[백준 6721] Backward numbers (C#, C++) - soo:bak"
date: "2023-07-24 20:44:00 +0900"
description: 구현, 문자열, 수학 등을 주제로 하는 백준 6721번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6721
  - C#
  - C++
  - 알고리즘
keywords: "백준 6721, 백준 6721번, BOJ 6721, BackwardNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6721번 - Backward numbers](https://www.acmicpc.net/problem/6721)

## 설명
입력으로 주어지는 두 개의 수를 역순으로 읽어 더한 후, <br>

그 합을 다시 역순으로 출력하는 문제입니다. <br>

예를 들어, 입력이 `24` `1` 이면, 이를 역순으로 읽어 `42` 와 `1` 을 더하여 `43`을 얻고, <br>

이를 다시 역순으로 바꿔 `34` 를 출력합니다. <br>

<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static int ReverseNum(int num) {
      return int.Parse(new string(num.ToString().Reverse().ToArray()));
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var a = int.Parse(input[0]);
        var b = int.Parse(input[1]);

        var reversedA = ReverseNum(a);
        var reversedB = ReverseNum(b);
        var sum = reversedA + reversedB;

        Console.WriteLine(ReverseNum(sum));
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

int reverseNum(int num) {
  string str = to_string(num);
  reverse(str.begin(), str.end());

  return stoi(str);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 0; i < n; i++) {
    int a, b; cin >> a >> b;

    int reversedA = reverseNum(a);
    int reversedB = reverseNum(b);
    int sum = reversedA + reversedB;

    cout << reverseNum(sum) << "\n";
  }

  return 0;
}
  ```
