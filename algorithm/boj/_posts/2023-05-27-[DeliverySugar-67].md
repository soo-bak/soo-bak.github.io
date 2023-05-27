---
layout: single
title: "[백준 2839] 설탕 배달 (C#, C++) - soo:bak"
date: "2023-05-27 13:33:00 +0900"
---

## 문제 링크
  [2839번 - 설탕 배달](https://www.acmicpc.net/problem/2839)

## 설명
`5kg` 과 `3kg` 의 설탕 봉지들의 개수를 최소화하여 정확히 `n kg` 의 설탕을 배달하는 것에 대한 문제입니다. <br>

<br>
`5kg` 의 봉지를 최대한 많이 사용하는 것이 봉지의 수를 최소화하는 방법입니다. <br>

따라서, 먼저 `n` 을 `5` 로 나눈 뒤, 나머지를 `3` 으로 나누어서 추가로 필요한 `3kg` 의 봉지의 개수를 구하면 됩니다. <br>

<br>
다만, `n` 이 `4kg` 혹은 `7kg` 과 같이 `5` 와 `3` 의 배수로 표현할 수 없는 경우에는 `-1` 을 출력해야 함에 주의합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var cntFiveKgBags = n / 5;

      n %= 5;
      while (cntFiveKgBags >= 0) {
        if (n % 3 == 0) {
          Console.WriteLine(cntFiveKgBags + (n / 3));
          return ;
        }
        cntFiveKgBags--;
        n += 5;
      }

      Console.WriteLine(-1);

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

  int cntFiveKgBags = n / 5;

  n %= 5;
  while (cntFiveKgBags >= 0) {
    if (n % 3 == 0) {
      cout << cntFiveKgBags + (n / 3) << "\n";
      return 0;
    }
    cntFiveKgBags--;
    n += 5;
  }

  cout << -1 << "\n";

  return 0;
}
  ```
