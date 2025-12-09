---
layout: single
title: "[백준 1434] 책 정리 (C#, C++) - soo:bak"
date: "2025-12-09 10:32:00 +0900"
description: 주어진 순서대로 책을 상자에 넣으며 남은 용량(낭비)을 계산하는 백준 1434번 책 정리 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1434번 - 책 정리](https://www.acmicpc.net/problem/1434)

## 설명
박스와 책이 순서대로 주어지고, 책을 순서대로 박스에 넣을 때 낭비되는 용량의 합을 구하는 문제입니다. 책이 현재 박스에 들어가지 않으면 그 박스를 봉인하고 다음 박스를 사용합니다.

<br>

## 접근법
첫 번째 박스부터 시작해서 각 책을 순서대로 넣습니다. 현재 박스에 책이 들어가면 박스 용량에서 책 크기를 빼고, 들어가지 않으면 현재 박스의 남은 용량을 낭비에 더한 뒤 다음 박스로 넘어갑니다. 모든 책을 넣은 후 사용하지 않은 박스들의 용량도 낭비에 더하여 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var nm = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    var n = nm[0];
    var m = nm[1];
    var box = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    var book = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    var waste = 0;
    var idx = 0;
    foreach (var b in book) {
      while (idx < n && box[idx] < b) {
        waste += box[idx];
        box[idx] = 0;
        idx++;
      }
      if (idx < n) box[idx] -= b;
    }
    while (idx < n) {
      waste += box[idx];
      idx++;
    }
    Console.WriteLine(waste);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vi box(n), book(m);
  for (int i = 0; i < n; i++)
    cin >> box[i];
  for (int i = 0; i < m; i++)
    cin >> book[i];

  int waste = 0;
  int idx = 0;
  for (int b : book) {
    while (idx < n && box[idx] < b) {
      waste += box[idx];
      box[idx] = 0;
      idx++;
    }
    if (idx < n) box[idx] -= b;
  }
  while (idx < n) {
    waste += box[idx];
    idx++;
  }
  cout << waste << "\n";

  return 0;
}
```
