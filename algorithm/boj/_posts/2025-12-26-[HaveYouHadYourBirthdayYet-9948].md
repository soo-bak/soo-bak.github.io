---
layout: single
title: "[백준 9948] Have you had your birthday yet? (C#, C++) - soo:bak"
date: "2025-12-26 01:03:01 +0900"
description: "백준 9948번 C#, C++ 풀이 - 기준 날짜와 생일을 비교해 상태를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 9948
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 9948, 백준 9948번, BOJ 9948, HaveYouHadYourBirthdayYet, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9948번 - Have you had your birthday yet?](https://www.acmicpc.net/problem/9948)

## 설명
2007년 8월 4일 기준으로 생일이 지났는지 여부를 출력하는 문제입니다.

<br>

## 접근법
먼저 종료 표식을 만나면 입력을 끝냅니다.

다음으로 2월 29일은 윤년이 아니므로 바로 Unlucky를 출력합니다.

이후 8월 4일이면 Happy birthday를 출력합니다.

마지막으로 그 외 날짜는 기준 날짜와 비교해 Yes 또는 No를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var monthMap = new Dictionary<string, int> {
      ["January"] = 1, ["February"] = 2, ["March"] = 3, ["April"] = 4,
      ["May"] = 5, ["June"] = 6, ["July"] = 7, ["August"] = 8,
      ["September"] = 9, ["October"] = 10, ["November"] = 11, ["December"] = 12
    };

    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      if (line == "0 #") break;

      var parts = line.Split();
      var day = int.Parse(parts[0]);
      var month = monthMap[parts[1]];

      if (month == 2 && day == 29) {
        Console.WriteLine("Unlucky");
        continue;
      }
      if (month == 8 && day == 4) {
        Console.WriteLine("Happy birthday");
        continue;
      }

      if (month < 8 || (month == 8 && day < 4)) Console.WriteLine("Yes");
      else Console.WriteLine("No");
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

  map<string, int> monthMap = {
    {"January", 1}, {"February", 2}, {"March", 3}, {"April", 4},
    {"May", 5}, {"June", 6}, {"July", 7}, {"August", 8},
    {"September", 9}, {"October", 10}, {"November", 11}, {"December", 12}
  };

  string line;
  while (getline(cin, line)) {
    if (line == "0 #") break;
    stringstream ss(line);
    int day; string month;
    ss >> day >> month;

    int m = monthMap[month];
    if (m == 2 && day == 29) {
      cout << "Unlucky\n";
      continue;
    }
    if (m == 8 && day == 4) {
      cout << "Happy birthday\n";
      continue;
    }

    if (m < 8 || (m == 8 && day < 4)) cout << "Yes\n";
    else cout << "No\n";
  }

  return 0;
}
```
