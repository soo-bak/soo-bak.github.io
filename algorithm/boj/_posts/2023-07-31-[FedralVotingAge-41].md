---
layout: single
title: "[백준 6845] Federal Voting Age (C#, C++) - soo:bak"
date: "2023-07-31 16:37:00 +0900"
description: 수학, 조건 분기, 구현 등을 주제로 하는 백준 6845번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6845
  - C#
  - C++
  - 알고리즘
  - 구현
  - 케이스분류
keywords: "백준 6845, 백준 6845번, BOJ 6845, FedralVotingAge, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6845번 - Federal Voting Age](https://www.acmicpc.net/problem/6845)

## 설명
입력으로 주어지는 생일에 대하여 투표 날짜인 `2007` 년 `02` 월 `27` 일이 되었을 때, <br>

해당 사람이 투표를 할 수 있는 나이닌 `18` 세에 도달했는지를 판별하는 문제입니다. <br>

`2` 월의 마지막 날 날짜를 고려해야 한다는 점에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static bool EnableToVote(int year, int month, int day) {
      if (year > 2007 || (year == 2007 && month > 2) || (year == 2007 && month == 2 && day > 27))
        return false;

      if (year < 1989 || (year == 1989 && month < 2) || (year == 1989 && month == 2 && day <= 27))
        return true;

      return false;
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var year = int.Parse(input[0]);
        var month = int.Parse(input[1]);
        var day = int.Parse(input[2]!);

        if (EnableToVote(year, month, day))
          Console.WriteLine("Yes");
        else Console.WriteLine("No");
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

bool enableToVote(int year, int month, int day) {
  if (year > 2007 || (year == 2007 && month > 2) || (year == 2007 && month == 2 && day > 27))
    return false;

  if (year < 1989 || (year == 1989 && month < 2) || (year == 1989 && month == 2 && day <= 27))
    return true;

  return false;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 0; i < n; i++) {
    int year, month, day;
    cin >> year >> month >> day;

    if (enableToVote(year, month, day))
      cout << "Yes" << "\n";
    else
      cout << "No" << "\n";
  }

  return 0;
}
  ```
