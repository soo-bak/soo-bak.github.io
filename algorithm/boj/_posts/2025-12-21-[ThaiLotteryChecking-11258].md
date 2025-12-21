---
layout: single
title: "[백준 11258] Thai Lottery Checking (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: 태국 복권 당첨 번호 6줄을 받아 각 티켓의 총 상금을 계산하는 문자열 매칭 문제
---

## 문제 링크
[11258번 - Thai Lottery Checking](https://www.acmicpc.net/problem/11258)

## 설명
태국 복권의 당첨 번호와 상금 정보가 주어질 때, 각 티켓의 총 상금을 계산하는 문제입니다.

<br>

## 접근법
당첨 조건은 1등(전체 6자리 일치), 앞 3자리 일치, 뒤 3자리 일치, 뒤 2자리 일치로 나뉩니다. 각 조건에는 별도의 상금이 있고, 한 티켓이 여러 조건을 동시에 만족하면 상금을 모두 합산합니다.

각 티켓 번호에 대해 모든 당첨 조건을 확인하고, 일치하는 조건의 상금을 더해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var firstNum = first[0];
    var firstPrize = int.Parse(first[1]);

    var front1 = Console.ReadLine()!.Split();
    var front2 = Console.ReadLine()!.Split();
    var frontNums = new[] { front1[0], front2[0] };
    var frontPrizes = new[] { int.Parse(front1[1]), int.Parse(front2[1]) };

    var back1 = Console.ReadLine()!.Split();
    var back2 = Console.ReadLine()!.Split();
    var backNums = new[] { back1[0], back2[0] };
    var backPrizes = new[] { int.Parse(back1[1]), int.Parse(back2[1]) };

    var last = Console.ReadLine()!.Split();
    var lastNum = last[0];
    var lastPrize = int.Parse(last[1]);

    var ticket = "";
    while ((ticket = Console.ReadLine()!) != "-1") {
      var sum = 0;
      if (ticket == firstNum) sum += firstPrize;

      var front = ticket.Substring(0, 3);
      for (var i = 0; i < 2; i++) {
        if (front == frontNums[i]) sum += frontPrizes[i];
      }

      var back = ticket.Substring(3, 3);
      for (var i = 0; i < 2; i++) {
        if (back == backNums[i]) sum += backPrizes[i];
      }

      var last2 = ticket.Substring(4, 2);
      if (last2 == lastNum) sum += lastPrize;

      Console.WriteLine(sum);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string firstNum; int firstPrize;
  cin >> firstNum >> firstPrize;

  string frontNum[2]; int frontPrize[2];
  cin >> frontNum[0] >> frontPrize[0];
  cin >> frontNum[1] >> frontPrize[1];

  string backNum[2]; int backPrize[2];
  cin >> backNum[0] >> backPrize[0];
  cin >> backNum[1] >> backPrize[1];

  string lastNum; int lastPrize;
  cin >> lastNum >> lastPrize;

  string ticket;
  while (cin >> ticket && ticket != "-1") {
    int sum = 0;
    if (ticket == firstNum) sum += firstPrize;

    string front = ticket.substr(0, 3);
    for (int i = 0; i < 2; i++) {
      if (front == frontNum[i]) sum += frontPrize[i];
    }

    string back = ticket.substr(3, 3);
    for (int i = 0; i < 2; i++) {
      if (back == backNum[i]) sum += backPrize[i];
    }

    string last2 = ticket.substr(4, 2);
    if (last2 == lastNum) sum += lastPrize;

    cout << sum << '\n';
  }

  return 0;
}
```
