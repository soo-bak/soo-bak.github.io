---
layout: single
title: "[백준 17930] Hanging Out on the Terrace (C#, C++) - soo:bak"
date: "2026-02-28 20:04:00 +0900"
description: "백준 17930번 C#, C++ 풀이 - 테라스 인원 제한을 넘겨 입장이 거절된 그룹 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 17930
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 17930, 백준 17930번, BOJ 17930, Hanging Out on the Terrace, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17930번 - Hanging Out on the Terrace](https://www.acmicpc.net/problem/17930)

## 설명
테라스의 최대 수용 인원과 입장, 퇴장 기록이 주어질 때, 수용 인원을 넘겨 입장이 거절된 그룹이 몇 번 있었는지 구하는 문제입니다.

<br>

## 접근법
현재 테라스에 있는 사람 수를 변수 하나로 관리하며 순서대로 시뮬레이션하면 됩니다.  
`enter`인 경우 현재 인원에 그룹 인원을 더했을 때 제한을 넘지 않으면 입장시키고, 넘으면 거절 횟수를 1 증가시킵니다.  
`leave`인 경우에는 현재 인원에서 해당 수만큼 빼면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var limit = int.Parse(first[0]);
    var x = int.Parse(first[1]);

    var cur = 0;
    var denied = 0;

    for (var i = 0; i < x; i++) {
      var parts = Console.ReadLine()!.Split();
      var type = parts[0];
      var p = int.Parse(parts[1]);

      if (type == "enter") {
        if (cur + p <= limit)
          cur += p;
        else
          denied++;
      } else {
        cur -= p;
      }
    }

    Console.WriteLine(denied);
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

  int limit, x;
  cin >> limit >> x;

  int cur = 0;
  int denied = 0;

  for (int i = 0; i < x; i++) {
    string type;
    int p;
    cin >> type >> p;

    if (type == "enter") {
      if (cur + p <= limit)
        cur += p;
      else
        denied++;
    } else {
      cur -= p;
    }
  }

  cout << denied << "\n";

  return 0;
}
```
