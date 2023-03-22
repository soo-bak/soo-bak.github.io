---
layout: single
title: "[백준 27257] Любитель нулей (C#, C++) - soo:bak"
date: "2023-03-22 10:51:00 +0900"
---

## 문제 링크
  [27257번 - Любитель нулей](https://www.acmicpc.net/problem/27257)

## 설명
  간단한 구현 문제입니다. <br>

  입력으로 주어지는 숫자에 등장하는 `0` 중에서, 끝에 위치한 `0` 을 제외한 `0` 의 총 갯수를 구하는 문제입니다.<br>

  입력은 숫자로 주어지지만, 간단한 구현으로 위하여 문자열로 입력을 받고 처리했습니다.<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var numStr  = Console.ReadLine()!;

      var ans = 0;
      for (int i = 0; i < numStr.Length; i++)
        if (numStr[i] == '0') ans++;

      for (int i = numStr.Length - 1; i != 0; i--) {
        if (numStr[i] == '0') ans--;
        else break ;
      }

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

  string numStr; cin >> numStr;

  int ans = 0;
  for (size_t i = 0; i < numStr.length(); i++)
    if (numStr[i] == '0') ans++;

  for (size_t i = numStr.length() - 1; i != 0; i--) {
    if (numStr[i] == '0') ans--;
    else break ;
  }

  cout << ans << "\n";

  return 0;
}
  ```
