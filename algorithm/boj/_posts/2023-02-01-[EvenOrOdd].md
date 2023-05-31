---
layout: single
title: "[백준 18005] Even or Odd? (C#) - soo:bak"
date: "2023-02-01 21:52:00 +0900"
description: 연속된 정수의 합에 대한 홀수와 짝수 판정 관련 백준 18005번 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [18005번 - Even or Odd?](https://www.acmicpc.net/problem/18005)

## 설명
  연속된 정수 `n` 개의 합이 `짝수` 인지, `홀수` 인지, `둘 다 가능한 지` 를 판별하는 문제입니다.

  [[ 21185번 - Some sum ](https://soo-bak.github.io/algorithm/boj/21185/#page-title)] 문제와 출력 형식만 다를 뿐, &nbsp;완전히 동일한 문제입니다.

  자세한 설명은 [[ 21185번 - Some sum ](https://soo-bak.github.io/algorithm/boj/21185/#page-title)] 에서의 설명을 참고하시면 좋을 것 같습니다.<br>

- - -

## Code
  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int.TryParse(Console.ReadLine(), out int n);

      string ans = "0";
      if (n % 2 == 0) {
        if ((n / 2) % 2 == 1) ans = "1";
        else ans = "2";
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

  int n; cin >> n;

  string ans = "0";
  if (n % 2 == 0) {
    if ((n / 2) % 2 == 1) ans = "1";
    else ans = "2";
  }

  cout << ans << "\n";

  return 0;
}
  ```
