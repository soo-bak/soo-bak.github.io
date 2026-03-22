---
layout: single
title: "[백준 27622] Suspicious Event (C#, C++) - soo:bak"
date: "2026-03-22 18:52:00 +0900"
description: "백준 27622번 C#, C++ 풀이 - 로그인 상태를 집합으로 관리하며 수상한 로그아웃 횟수를 세는 문제"
tags:
  - 백준
  - BOJ
  - 27622
  - C#
  - C++
  - 알고리즘
  - 구현
  - 자료 구조
keywords: "백준 27622, 백준 27622번, BOJ 27622, Suspicious Event, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27622번 - Suspicious Event](https://www.acmicpc.net/problem/27622)

## 설명
로그인과 로그아웃 기록이 시간 순서대로 주어질 때, 이전에 로그인한 적이 없는 사용자의 로그아웃 횟수를 세는 문제입니다.

<br>

## 접근법
현재 로그인되어 있는 사용자만 집합에 저장하며 기록을 앞에서부터 순서대로 처리합니다.

양수 `x`가 나오면 사용자 `x`가 로그인한 것이므로 집합에 넣습니다. 음수 `-x`가 나오면 사용자 `x`의 로그아웃인데, 이 사용자가 집합에 없으면 수상한 이벤트입니다. 반대로 집합에 있으면 정상 로그아웃이므로 집합에서 제거합니다.

모든 기록에 대해 이 과정을 반복하면서 수상한 로그아웃만 세면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine()!);
    int[] events = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    var loggedIn = new HashSet<int>();
    int answer = 0;

    foreach (int ev in events) {
      if (ev > 0) {
        loggedIn.Add(ev);
      } else {
        int user = -ev;
        if (loggedIn.Contains(user))
          loggedIn.Remove(user);
        else
          answer++;
      }
    }

    Console.WriteLine(answer);
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

  int n;
  cin >> n;

  unordered_set<int> logged_in;
  int answer = 0;

  for (int i = 0; i < n; i++) {
    int ev;
    cin >> ev;

    if (ev > 0) {
      logged_in.insert(ev);
    } else {
      int user = -ev;
      if (logged_in.find(user) != logged_in.end())
        logged_in.erase(user);
      else
        answer++;
    }
  }

  cout << answer << "\n";

  return 0;
}
```
