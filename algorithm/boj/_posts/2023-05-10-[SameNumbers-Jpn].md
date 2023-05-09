---
layout: single
title: "[백준 27324] ゾロ目 (Same Numbers) (C#, C++) - soo:bak"
date: "2023-05-10 00:13:00 +0900"
---

## 문제 링크
  [27324번 - ゾロ目 (Same Numbers)](https://www.acmicpc.net/problem/27324)

## 설명
입력으로 주어지는 두 자리 정수 `n` 의 십의 자리와 일의 자리가 같은지 판단하고, <br>

같으면 `1` 을, 다르다면 `0` 을 출력하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var digitTen = n / 10;
      var digitOne = n % 10;

      if (digitTen == digitOne) Console.WriteLine("1");
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

  int n; cin >> n;

  int digitTen = n / 10, digitOne = n % 10;

  if (digitTen == digitOne) cout << "1\n";
  else cout << "0\n";

  return 0;
}
  ```
