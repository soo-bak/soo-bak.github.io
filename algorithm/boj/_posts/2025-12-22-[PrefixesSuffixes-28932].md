---
layout: single
title: "[백준 28932] Префиксы-суффиксы (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 28932번 C#, C++ 풀이 - 두 수의 접두사와 접미사가 일치하는 쌍을 찾아 인덱스를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 28932
  - C#
  - C++
  - 알고리즘
keywords: "백준 28932, 백준 28932번, BOJ 28932, PrefixesSuffixes, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[28932번 - Префиксы-суффиксы](https://www.acmicpc.net/problem/28932)

## 설명
수열에서 어떤 수의 접두사와 다른 수의 접미사가 같은 쌍이 있는지 찾는 문제입니다.

<br>

## 접근법
각 수를 문자열로 보고 모든 쌍을 확인합니다. 두 문자열의 길이 중 작은 값까지 길이를 늘려가며 접두사와 접미사를 비교합니다.

하나라도 같으면 해당 인덱스를 출력하고, 끝까지 없으면 -1을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();
    var a = new string[n];
    for (var i = 0; i < n; i++)
      a[i] = parts[i];

    for (var i = 0; i < n; i++) {
      for (var j = 0; j < n; j++) {
        var len = a[i].Length < a[j].Length ? a[i].Length : a[j].Length;
        for (var k = 1; k <= len; k++) {
          if (a[i].Substring(0, k) == a[j].Substring(a[j].Length - k)) {
            Console.WriteLine($"{i + 1} {j + 1}");
            return;
          }
        }
      }
    }

    Console.WriteLine(-1);
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
  vs a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      int len = min((int)a[i].size(), (int)a[j].size());
      for (int k = 1; k <= len; k++) {
        if (a[i].substr(0, k) == a[j].substr(a[j].size() - k)) {
          cout << i + 1 << " " << j + 1 << "\n";
          return 0;
        }
      }
    }
  }

  cout << -1 << "\n";

  return 0;
}
```
