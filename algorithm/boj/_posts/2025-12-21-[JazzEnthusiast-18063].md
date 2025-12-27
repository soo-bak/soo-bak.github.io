---
layout: single
title: "[백준 18063] Jazz Enthusiast (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: "백준 18063번 C#, C++ 풀이 - 곡 길이와 크로스페이드 시간을 이용해 전체 청취 시간을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 18063
  - C#
  - C++
  - 알고리즘
keywords: "백준 18063, 백준 18063번, BOJ 18063, JazzEnthusiast, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18063번 - Jazz Enthusiast](https://www.acmicpc.net/problem/18063)

## 설명
곡 목록과 크로스페이드 시간이 주어질 때 전체 청취 시간을 계산하는 문제입니다.

<br>

## 접근법
크로스페이드는 인접한 두 곡이 겹쳐서 재생되는 시간입니다. 모든 곡의 길이를 초 단위로 변환해 합산합니다. 곡이 n개일 때 크로스페이드가 적용되는 구간은 n-1개이므로, 총 시간에서 크로스페이드 시간과 구간 수를 곱한 값을 빼면 됩니다. 계산된 총 초를 시, 분, 초로 변환하여 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var c = int.Parse(first[1]);

    var total = 0;
    for (var i = 0; i < n; i++) {
      var s = Console.ReadLine()!;
      var parts = s.Split(':');
      var m = int.Parse(parts[0]);
      var sec = int.Parse(parts[1]);
      total += m * 60 + sec;
    }

    total -= c * (n - 1);

    var h = total / 3600;
    total %= 3600;
    var m2 = total / 60;
    var s2 = total % 60;

    Console.WriteLine($"{h:D2}:{m2:D2}:{s2:D2}");
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

  int n, c; cin >> n >> c;
  int total = 0;
  for (int i = 0; i < n; i++) {
    string s; cin >> s;
    int pos = s.find(':');
    int m = stoi(s.substr(0, pos));
    int sec = stoi(s.substr(pos + 1));
    total += m * 60 + sec;
  }

  total -= c * (n - 1);

  int h = total / 3600;
  total %= 3600;
  int m2 = total / 60;
  int s2 = total % 60;

  cout << setw(2) << setfill('0') << h << ':'
       << setw(2) << setfill('0') << m2 << ':'
       << setw(2) << setfill('0') << s2 << "\n";

  return 0;
}
```
