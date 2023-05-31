---
layout: single
title: "[백준 26489] Gum Gum for Jay Jay (C#, C++) - soo:bak"
date: "2023-05-09 23:40:00 +0900"
description: 입력과 출력, 문자열 다루기를 주제로 하는 백준 26489번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [26489번 - Gum Gum for Jay Jay](https://www.acmicpc.net/problem/26489)

## 설명
입력으로 주어지는 데이터 파일의 줄 수를 출력하는 문제입니다. <br>

데이터 파일을 입력받으면서, 각 줄의 수를 셉니다. <br>

최종적으로 계산된 줄의 수를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      string? line; int cntLine = 0;
      while ((line = Console.ReadLine()) != null)
        cntLine++;

      Console.WriteLine(cntLine);

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

  string line = ""; int cntLine = 0;

  while (getline(cin, line))
    cntLine++;

  cout << cntLine << "\n";

  return 0;
}
  ```
