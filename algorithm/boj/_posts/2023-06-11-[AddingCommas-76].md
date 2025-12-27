---
layout: single
title: "[백준 5949] Adding Commas (C#, C++) - soo:bak"
date: "2023-06-11 21:55:00 +0900"
description: 문자열 다루기와 구현을 주제로 하는 백준 5949번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5949
  - C#
  - C++
  - 알고리즘
keywords: "백준 5949, 백준 5949번, BOJ 5949, AddingCommas, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [5949번 - Adding Commas](https://www.acmicpc.net/problem/5949)

## 설명
주어진 숫자의 적절한 위치에 `,` 를 추가하는 문제입니다. <br>

입력으로 주어진 수를 문자열로 변환하여, 뒤에서 부터 세 자릿수마다 `,` 을 추가하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var strNum = new string(n.ToString().Reverse().ToArray());

      string ans = "";
      for (int i = 0; i < strNum.Length; i++) {
        if (i != 0 && i % 3 == 0) ans += ",";
        ans += strNum[i];
      }

      ans = new string(ans.Reverse().ToArray());
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

  int n; cin >> n;

  string strNum = to_string(n);

  reverse(strNum.begin(), strNum.end());

  string ans = "";
  for (size_t i = 0; i < strNum.size(); i++) {
    if (i != 0 && i % 3 == 0)
      ans += ",";
    ans += strNum[i];
  }

  reverse(ans.begin(), ans.end());

  cout << ans << "\n";

  return 0;
}
  ```
