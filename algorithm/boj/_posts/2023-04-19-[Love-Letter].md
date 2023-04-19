---
layout: single
title: "[백준 27541] 末尾の文字 (Last Letter) (C#, C++) - soo:bak"
date: "2023-04-19 15:40:00 +0900"
---

## 문제 링크
  [27541번 - 末尾の文字 (Last Letter)](https://www.acmicpc.net/problem/27541)

## 설명
문자열을 다루는 구현 문제입니다. <br>

문제의 조건에 따라, 문자열의 끝에 `G` 문자가 있다면, 문자열의 끝에 `G` 를 제거합니다. <br>

만약, 문자열의 끝에 `G` 문자가 없다면, 반대로 문자열의 끝에 `G` 를 추가합니다. <br>

이후, 최종적인 문자열을 문제의 출력 조건에 따라 적절히 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);
      var input = Console.ReadLine();

      if (input![n - 1] == 'G') input = input.Remove(n - 1, 1);
      else input += 'G';

      Console.WriteLine(input);

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
  string input; cin >> input;

  if (input[n - 1] == 'G') input.erase(n - 1, 1);
  else input.push_back('G');

  cout << input << "\n";

  return 0;
}
  ```
