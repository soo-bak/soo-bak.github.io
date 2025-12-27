---
layout: single
title: "[백준 1436] 영화감독 숌 (C#, C++) - soo:bak"
date: "2023-05-30 18:05:00 +0900"
description: 문자열과 시뮬레이션, 탐색 등을 주제로 하는 백준 1436번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1436
  - C#
  - C++
  - 알고리즘
keywords: "백준 1436, 백준 1436번, BOJ 1436, MovieDirectorShom, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [1436번 - 영화감독 숌](https://www.acmicpc.net/problem/1436)

## 설명
`666` 을 포함하는 숫자들을 작은 순서대로 생성하고, 그 중에서 `n` 번째 숫자를 찾는 문제입니다. <br>

`666` 을 포함하는 숫자는 다음과 같은 방식으로 생성될 수 있습니다. <br>

- `666` 부터 시작 <br>
- `1666` , `2666` , `3666` , `...` , `9666` <br>
- `10666` , `11666` , `12666` , `...` , `19666` <br>
- `20666` , `21666` , `22666` , `...` , `29666` <br>

이런 식으로 계속해서 `666` 을 포함하는 숫자들을 생성할 수 있습니다. <br>

따라서, 먼저 `n` 을 입력으로 받고 정답으로 출력할 정수를 `666` 으로 초기화 합니다. <br>

이후, 해당 정수 자료형을 문자열로 변환한 후 `666` 이 포함되어 있는지 확인합니다. <br>

문자열에 `666` 이 포함되어 있으면 `n` 을 `1` 감소시킵니다. <br>

`n` 이 `0` 이 될 때까지 정답으로 출력할 정수를 `1` 씩 증가시킵니다. <br>

이 과정을 `n` 이 `0` 이 될 때 까지, 즉, 순서에 맞는 `666` 이 들어간 숫자를 찾을 때까지 반복하며 탐색합니다. <br>

마지막 반복문을 빠져나올 때 출력할 정수에 `+1` 이 된 상태로 빠져나오게 되므로, 정답을 출력하기 전에 `-1` 을 해주어야 함에 주의합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int title = 666;
      while (n > 0) {
        string strTitle = title.ToString();
        if (strTitle.Contains("666"))
          n--;
        title++;
      }

      Console.WriteLine(title - 1);

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

  int title = 666;
  while (n > 0) {
    string strTitle = to_string(title);
    if (strTitle.find("666") != string::npos)
      n--;
    title++;
  }

  cout << title - 1 << "\n";

  return 0;
}
  ```
