---
layout: single
title: "[백준 31994] 강당 대관 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 7개 세미나 중 신청자 수가 가장 많은 세미나 이름을 출력하는 문제
---

## 문제 링크
[31994번 - 강당 대관](https://www.acmicpc.net/problem/31994)

## 설명
7개 세미나의 이름과 신청자 수가 주어질 때, 가장 많은 신청자를 가진 세미나 이름을 출력하는 문제입니다.

<br>

## 접근법
7줄을 모두 읽으면서 신청자 수가 가장 큰 세미나를 갱신합니다. 최댓값을 가진 세미나 이름을 출력하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var bestName = "";
    var best = -1;
    for (var i = 0; i < 7; i++) {
      var parts = Console.ReadLine()!.Split();
      var name = parts[0];
      var val = int.Parse(parts[1]);
      if (val > best) {
        best = val;
        bestName = name;
      }
    }

    Console.WriteLine(bestName);
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

  string bestName;
  int best = -1;
  for (int i = 0; i < 7; i++) {
    string name; int val;
    cin >> name >> val;
    if (val > best) {
      best = val;
      bestName = name;
    }
  }

  cout << bestName << "\n";

  return 0;
}
```
