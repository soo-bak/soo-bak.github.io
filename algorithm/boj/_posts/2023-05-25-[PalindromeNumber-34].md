---
layout: single
title: "[백준 1259] 펠린드롬수 (C#, C++) - soo:bak"
date: "2023-05-25 12:22:00 +0900"
---

## 문제 링크
  [1259번 - 펠린드롬수](https://www.acmicpc.net/problem/1259)

## 설명
주어진 숫자가 회문 구조를 가지고 있는지 아닌지 판별하는 문제입니다. <br>

회문 구조는 단어나 문장, 숫자 등이 앞에서부터 읽었을 때와 뒤에서부터 읽었을 때가 동일한 구조입니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var str = Console.ReadLine()!;

        if (str == "0") break ;

        var reversedStr = new string(str.Reverse().ToArray());

        if (str == reversedStr) Console.WriteLine("yes");
        else Console.WriteLine("no");
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

  while (true) {
    string str; cin >> str;

    if (str == "0") break ;

    string reversedStr = str;
    reverse(reversedStr.begin(), reversedStr.end());

    if (str == reversedStr) cout << "yes\n";
    else cout << "no\n";
  }

  return 0;
}
  ```
