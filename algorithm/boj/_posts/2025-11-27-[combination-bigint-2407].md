---
layout: single
title: "[백준 2407] 조합 (C#, C++) - soo:bak"
date: "2025-11-27 01:00:00 +0900"
description: 파스칼 삼각형 점화식과 문자열 덧셈으로 큰 조합 값을 동적 프로그래밍으로 계산하는 백준 2407번 조합 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 2407
  - C#
  - C++
  - 알고리즘
  - 수학
  - 조합론
  - arbitrary_precision
keywords: "백준 2407, 백준 2407번, BOJ 2407, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2407번 - 조합](https://www.acmicpc.net/problem/2407)

## 설명

두 정수 `n`과 `m` (`5 ≤ n ≤ 100`, `5 ≤ m ≤ 100`, `m ≤ n`)이 주어질 때, 조합 `nCm`을 구하는 문제입니다.

`n`과 `m`이 100 이하로 작지만 조합 값은 매우 커질 수 있어 일반 정수 자료형으로는 표현할 수 없으므로, 큰 수 처리가 필요합니다.

<br>

## 접근법

조합 값을 일반 정수로 계산하면 오버플로가 발생하므로, 파스칼 삼각형의 점화식 `nCm = (n-1)C(m-1) + (n-1)Cm`을 이용한 동적 프로그래밍으로 계산합니다.

각 조합 값을 문자열로 저장하고, 두 문자열을 더하는 큰 수 덧셈 함수를 구현하여 사용합니다.

기저 조건은 `nC0 = 1`과 `nCn = 1`이며, 메모이제이션을 통해 이미 계산된 값을 재사용하여 중복 계산을 방지합니다.

<br>
예를 들어, `4C2 = 3C1 + 3C2 = (2C0 + 2C1) + (2C1 + 2C2) = 1 + 2 + 2 + 1 = 6`과 같이 재귀적으로 계산되며, 문자열 덧셈으로 큰 값도 정확히 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static string[,] dp = new string[101, 101];

    static string Add(string a, string b) {
      var res = new List<char>();
      var i = a.Length - 1;
      var j = b.Length - 1;
      var carry = 0;

      while (i >= 0 || j >= 0 || carry > 0) {
        var sum = carry;

        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';

        res.Add((char)('0' + (sum % 10)));
        carry = sum / 10;
      }

      res.Reverse();
      return new string(res.ToArray());
    }

    static string Comb(int n, int r) {
      if (r == 0 || n == r) return "1";
      if (dp[n, r] != null) return dp[n, r];

      dp[n, r] = Add(Comb(n - 1, r - 1), Comb(n - 1, r));
      return dp[n, r];
    }

    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var n = int.Parse(tokens[0]);
      var r = int.Parse(tokens[1]);

      Console.WriteLine(Comb(n, r));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string addBig(const string& a, const string& b) {
  string res;
  int i = (int)a.size() - 1, j = (int)b.size() - 1, carry = 0;

  while (i >= 0 || j >= 0 || carry) {
    int sum = carry;

    if (i >= 0) sum += a[i--] - '0';
    if (j >= 0) sum += b[j--] - '0';

    res.push_back(char('0' + (sum % 10)));
    carry = sum / 10;
  }

  reverse(res.begin(), res.end());
  return res;
}

string dp[101][101];

string comb(int n, int r) {
  if (r == 0 || n == r) return "1";

  string& ret = dp[n][r];
  if (!ret.empty()) return ret;

  ret = addBig(comb(n - 1, r - 1), comb(n - 1, r));
  return ret;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  cout << comb(n, m) << "\n";

  return 0;
}
```

