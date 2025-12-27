---
layout: single
title: "[백준 20336] Haughty Cuisine (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 20336번 C#, C++ 풀이 - 세트 메뉴 중 하나를 그대로 골라 추천 목록으로 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 20336
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 20336, 백준 20336번, BOJ 20336, HaughtyCuisine, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20336번 - Haughty Cuisine](https://www.acmicpc.net/problem/20336)

## 설명
여러 세트 메뉴 중 하나를 골라 그 구성 그대로 추천 목록을 출력하는 문제입니다.

<br>

## 접근법
아무 세트 메뉴 하나를 그대로 출력하면 됩니다. 첫 번째 메뉴를 읽어 저장한 뒤, 나머지는 입력만 소비합니다. 저장한 메뉴의 개수와 항목을 그대로 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var first = new List<string>();

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var d = int.Parse(parts[0]);
      if (i == 0) {
        for (var j = 0; j < d; j++)
          first.Add(parts[j + 1]);
      }
    }

    Console.WriteLine(first.Count);
    foreach (var item in first)
      Console.WriteLine(item);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  int d; cin >> d;
  vs first(d);
  for (int i = 0; i < d; i++)
    cin >> first[i];

  for (int i = 1; i < n; i++) {
    cin >> d;
    for (int j = 0; j < d; j++) {
      string tmp; cin >> tmp;
    }
  }

  cout << first.size() << "\n";
  for (const auto& item : first)
    cout << item << "\n";

  return 0;
}
```
