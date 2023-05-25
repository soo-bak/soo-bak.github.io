---
layout: single
title: "[백준 5013] Death Knight Hero (C#, C++) - soo:bak"
date: "2023-05-25 12:14:00 +0900"
---

## 문제 링크
  [5013번 - Death Knight Hero](https://www.acmicpc.net/problem/5013)

## 설명
간단히, 입력으로 주어지는 각각의 문자열에 `"CD"` 문자열이 있는지 판별하는 문제입니다. <br>

영웅이 사용한 기술에 대한 문자열이 `"CD"` 를 포함하지 않고 있는 문자열이면, 해당 전투에서 영웅이 이긴 것으로 간주합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int cntWins = 0;
      for (int i = 0; i < n; i++) {
        var abilities = Console.ReadLine()!;

        if (!abilities.Contains("CD"))
          cntWins++;
      }

      Console.WriteLine(cntWins);

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

  int cntWins = 0;
  for (int i = 0; i < n; i++) {
    string abilities; cin >> abilities;

    bool hasCD = false;
    for (size_t j = 0; j < abilities.size(); j++) {
      if (abilities[j] == 'C' && abilities[j + 1] == 'D') {
        hasCD = true;
        break ;
      }
    }

    if (!hasCD) cntWins++;
  }

  cout << cntWins << "\n";

  return 0;
}
  ```
