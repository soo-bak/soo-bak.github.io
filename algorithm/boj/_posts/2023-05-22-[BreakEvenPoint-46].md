---
layout: single
title: "[백준 1712] 손익분기점 (C#, C++) - soo:bak"
date: "2023-05-22 15:33:00 +0900"
---

## 문제 링크
  [1712번 - 손익분기점](https://www.acmicpc.net/problem/1712)

## 설명
단순히 수학적인 계산을 이용하는 문제입니다. <br>

고정 비용 `A`, 가변 비용 `B`, 판매 가격 `C` 가 주어졌을 때,<br>

판매 수량 `x` 에 대한 총 비용은 `A` + (`B` * `x`) 이며, 총 수익은 (`C` * `x`) 입니다. <br>

<br>
이익이 발생하기 시작하는 시점, 즉, 손익분기점을 구하기 위해서는 총 수익이 총 비용을 초과하기 시작하는 판매 수량을 찾아야 합니다. <br>

그러므로, `A` + (`B` * `x`) < (`C` * `x`) 을 만족하는 가장 작은 `x` 를 찾아야 합니다. <br>

위 부등식을 `x` 에 대하여 정리하면, `x` > `A` / (`C` - `B`) 가 됩니다. <br>

<br>
`C` 가 `B` 보다 작거나 같은 경우에는 판매 가격이 가변 비용보다 작거나 같게 되므로, 손익분기점이 존재하지 않음에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');

      var A = long.Parse(input[0]);
      var B = long.Parse(input[1]);
      var C = long.Parse(input[2]);

      if (C <= B) Console.WriteLine(-1);
      else Console.WriteLine(A / (C - B) + 1);

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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll A, B, C; cin >> A >> B >> C;

  if (C <= B) cout << -1 << "\n";
  else cout << A / (C - B) + 1 << "\n";

  return 0;
}
  ```
