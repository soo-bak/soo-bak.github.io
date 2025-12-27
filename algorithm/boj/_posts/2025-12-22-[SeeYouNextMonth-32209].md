---
layout: single
title: "[백준 32209] 다음 달에 봐요 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 32209번 C#, C++ 풀이 - 문제 포럼의 남은 문제 수를 누적하며 해산 여부를 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 32209
  - C#
  - C++
  - 알고리즘
keywords: "백준 32209, 백준 32209번, BOJ 32209, SeeYouNextMonth, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32209번 - 다음 달에 봐요](https://www.acmicpc.net/problem/32209)

## 설명
이벤트를 순서대로 처리하며 문제 포럼의 남은 문제 수가 부족해지는지 확인하는 문제입니다.

<br>

## 접근법
현재 남은 문제 수를 누적하며, 문제가 추가되면 더하고 풀면 뺍니다.

음수가 되는 순간 해산이므로 Adios를 출력하고, 끝까지 버티면 See you next month를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var q = int.Parse(Console.ReadLine()!);
    var cur = 0;
    for (var i = 0; i < q; i++) {
      var parts = Console.ReadLine()!.Split();
      var type = int.Parse(parts[0]);
      var val = int.Parse(parts[1]);
      if (type == 1) cur += val;
      else {
        cur -= val;
        if (cur < 0) {
          Console.WriteLine("Adios");
          return;
        }
      }
    }

    Console.WriteLine("See you next month");
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

  int q; cin >> q;
  int cur = 0;
  for (int i = 0; i < q; i++) {
    int type, val; cin >> type >> val;
    if (type == 1) cur += val;
    else {
      cur -= val;
      if (cur < 0) {
        cout << "Adios\n";
        return 0;
      }
    }
  }

  cout << "See you next month\n";

  return 0;
}
```
