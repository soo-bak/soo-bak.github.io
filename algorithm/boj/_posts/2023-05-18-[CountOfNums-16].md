---
layout: single
title: "[백준 2577] 숫자의 개수 (C#, C++) - soo:bak"
date: "2023-05-18 14:02:00 +0900"
---

## 문제 링크
  [2577번 - 숫자의 개수](https://www.acmicpc.net/problem/2577)

## 설명
입력으로 주어지는 세 개의 숫자의 곱에 대하여, `0` 부터 `9` 까지의 숫자가 각각 몇 번 등장하는지 구하는 문제입니다. <br>

주어진 세 숫자를 곱한 결과를 문자열로 변환한 후, <br>

해당 문자열에서 `0` 부터 `9` 까지의 문자가 몇 번 등장하는지 세는 방법으로 풀이하였습니다. <br>

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
      var c = int.Parse(Console.ReadLine()!);

      var res = a * b * c;
      var strRes = res.ToString();

      for (int i = 0; i <= 9; i++) {
        var cntNum = strRes.Count(ch => ch == '0' + i);
        Console.WriteLine(cntNum);
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

  int a, b, c; cin >> a >> b >> c;

  int res = a * b * c;
  string strRes = to_string(res);

  for (int i = 0; i <= 9; i++) {
    int cntNum = count(strRes.begin(), strRes.end(), '0' + i);
    cout << cntNum << "\n";
  }

  return 0;
}
  ```
