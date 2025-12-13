---
layout: single
title: "[백준 12840] 창용이의 시계 (C#, C++) - soo:bak"
date: "2025-12-13 22:20:00 +0900"
description: 하루 86400초를 기준으로 시계를 앞뒤로 이동시킨 뒤 쿼리 시점의 시각을 출력하는 백준 12840번 창용이의 시계 문제의 C#/C++ 풀이
---

## 문제 링크
[12840번 - 창용이의 시계](https://www.acmicpc.net/problem/12840)

## 설명
시각을 앞뒤로 이동시킨 뒤 쿼리 시점의 시각을 출력하는 문제입니다.

<br>

## 접근법
시각을 초 단위로 변환해 저장합니다.

쿼리마다 초를 더하거나 빼고, 하루 총 초수 86400으로 나눈 나머지를 취합니다.

뺄셈 결과가 음수면 86400을 더해 보정합니다.

조회 시에는 초를 다시 시, 분, 초로 나눠 출력합니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var daySec = 86400;
    var line = Console.ReadLine()!.Split();
    var h = int.Parse(line[0]);
    var m = int.Parse(line[1]);
    var s = int.Parse(line[2]);
    var q = int.Parse(Console.ReadLine()!);

    var time = h * 3600 + m * 60 + s;
    for (var i = 0; i < q; i++) {
      var cmd = Console.ReadLine()!.Split();
      var t = int.Parse(cmd[0]);
      if (t == 1) {
        var c = int.Parse(cmd[1]);
        time = (time + c) % daySec;
      } else if (t == 2) {
        var c = int.Parse(cmd[1]);
        time = (time - c) % daySec;
        if (time < 0) time += daySec;
      } else {
        var oh = time / 3600;
        var om = (time / 60) % 60;
        var os = time % 60;
        Console.WriteLine($"{oh} {om} {os}");
      }
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

  int daySec = 86400;
  int h, m, s;
  if (!(cin >> h >> m >> s)) return 0;
  int q; cin >> q;
  int time = h * 3600 + m * 60 + s;

  for (int i = 0; i < q; i++) {
    int t; cin >> t;
    if (t == 1) {
      int c; cin >> c;
      time = (time + c) % daySec;
    } else if (t == 2) {
      int c; cin >> c;
      time = (time - c) % daySec;
      if (time < 0) time += daySec;
    } else {
      int oh = time / 3600;
      int om = (time / 60) % 60;
      int os = time % 60;
      cout << oh << " " << om << " " << os << "\n";
    }
  }

  return 0;
}
```
