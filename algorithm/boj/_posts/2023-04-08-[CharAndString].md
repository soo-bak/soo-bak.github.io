---
layout: single
title: "[백준 27866] 문자와 문자열 (C#, C++) - soo:bak"
date: "2023-04-08 01:30:00 +0900"
---

## 문제 링크
  [27866번 - 문자와 문자열](https://www.acmicpc.net/problem/27866)

## 설명
문자와 문자열의 기본 개념에 대한 문제입니다. <br>

문자열은 일종의 문자의 배열이라고 할 수 있으므로, 배열 접근자 `[ ]` 을 통하여 쉽게 접근할 수 있습니다. <br>

따라서, 입력으로 받은 `문자열` 과 `index` 에 대해서 적절히 처리하여 출력 합니다. <br>

다만, 아직 `index` 와 `순번` 에 익숙하지 않으신 분들은 `index` 와 `순번` 의 관계에 주의해야 합니다. <br>

`1` 번째 문자의 `index` 는 `0` 입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var str = Console.ReadLine()!;
      var idx = int.Parse(Console.ReadLine()!);

      Console.WriteLine(str[idx - 1]);

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

  string str; int idx; cin >> str >> idx;
  cout << str[idx - 1] << "\n";

  return 0;
}
  ```
