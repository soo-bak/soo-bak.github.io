---
layout: single
title: "[백준 31609] 現れている数字 (Appearing Numbers) (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: 수열에 등장한 0~9를 오름차순으로 출력하는 문제
---

## 문제 링크
[31609번 - 現れている数字 (Appearing Numbers)](https://www.acmicpc.net/problem/31609)

## 설명
0~9 사이의 수열이 주어질 때, 한 번이라도 등장한 숫자를 오름차순으로 출력하는 문제입니다.

<br>

## 접근법
길이 10의 배열로 각 숫자의 등장 여부를 기록합니다.

이후 입력을 모두 확인한 뒤 0부터 9까지 순회하며 등장한 숫자만 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();

    var seen = new bool[10];
    for (var i = 0; i < n; i++) {
      var v = int.Parse(parts[i]);
      seen[v] = true;
    }

    for (var i = 0; i <= 9; i++) {
      if (seen[i]) Console.WriteLine(i);
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

  int n; cin >> n;
  bool seen[10] = {};
  for (int i = 0; i < n; i++) {
    int v; cin >> v;
    seen[v] = true;
  }

  for (int i = 0; i <= 9; i++) {
    if (seen[i]) cout << i << "\n";
  }

  return 0;
}
```
