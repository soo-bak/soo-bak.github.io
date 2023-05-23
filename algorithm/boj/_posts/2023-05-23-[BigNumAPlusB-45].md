---
layout: single
title: "[백준 10757] 큰 수 A+B (C#, C++) - soo:bak"
date: "2023-05-23 09:38:00 +0900"
---

## 문제 링크
  [10757번 - 큰 수 A+B](https://www.acmicpc.net/problem/10757)

## 설명
두 개의 매우 큰 수를 입력받아서 더한 값을 구하는 문제입니다. <br>

주어진 두 수는 `C++` 의 정수형 자료형들의 범위를 넘어서므로, 문자열로 처리를 하여 해결해야 합니다. <br>

<br>
먼저, 각 숫자를 두 개의 문자열로 입력을 받고 문자열의 뒤에서부터 한 자리씩 더해갑니다. <br>

이 떄, 한 자리의 더한 값이 `10` 이상인 경우, 자리올림에 대해서 처리합니다. <br>

자리올림은 다음 수를 더할 때 `1` 을 추가적으로 더해주는 방식으로 구현할 수 있습니다. <br>

<br>
마지막으로, 문자열을 역순으로 출력하면 정답을 구할 수 있습니다. <br>

<br>
`C#` 에서는 `BigInteger` 자료형을 활용하여 풀이하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  using System.Numerics;
  class Program {
    static void Main(string[] args) {

      var nums = Console.ReadLine()!.Split(' ').Select(BigInteger.Parse).ToArray();

      Console.WriteLine(nums[0] + nums[1]);

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

  string a, b; cin >> a >> b;

  while (a.length() < b.length())
    a = "0" + a;
  while (b.length() < a.length())
    b = "0" + b;

  string res = "";
  int carryOver = 0;
  for (int i = a.length() - 1; i >= 0; i--) {
    int tmp = a[i] - '0' + b[i] - '0' + carryOver;
    carryOver = tmp / 10;
    res += (char)(tmp % 10 + '0');
  }

  if (carryOver > 0)
    res += (char)(carryOver + '0');

  reverse(res.begin(), res.end());

  cout << res << "\n";

  return 0;
}
  ```
