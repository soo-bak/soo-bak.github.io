---
layout: single
title: "[백준 13304] 방 배정 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: 학년/성별 조건에 맞춰 최소 방 개수를 구하는 문제
---

## 문제 링크
[13304번 - 방 배정](https://www.acmicpc.net/problem/13304)

## 설명
학년과 성별 조건에 맞게 학생들을 방에 배정할 때 필요한 최소 방 개수를 구하는 문제입니다.

<br>

## 접근법
1~2학년은 성별과 학년을 구분하지 않고 한 그룹으로 계산합니다.

3~4학년, 5~6학년은 성별을 분리하여 각각 인원수를 세고, 인원수를 K로 나눈 뒤 올림한 방 수를 더합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Rooms(int count, int k) {
    return (count + k - 1) / k;
  }

  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var k = int.Parse(first[1]);

    var g12 = 0;
    var g34f = 0;
    var g34m = 0;
    var g56f = 0;
    var g56m = 0;

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var s = int.Parse(parts[0]);
      var y = int.Parse(parts[1]);

      if (y <= 2) g12++;
      else if (y <= 4) {
        if (s == 0) g34f++;
        else g34m++;
      } else {
        if (s == 0) g56f++;
        else g56m++;
      }
    }

    var ans = 0;
    ans += Rooms(g12, k);
    ans += Rooms(g34f, k);
    ans += Rooms(g34m, k);
    ans += Rooms(g56f, k);
    ans += Rooms(g56m, k);

    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int rooms(int count, int k) {
  return (count + k - 1) / k;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, k; cin >> n >> k;
  int g12 = 0, g34f = 0, g34m = 0, g56f = 0, g56m = 0;

  for (int i = 0; i < n; i++) {
    int s, y; cin >> s >> y;
    if (y <= 2) g12++;
    else if (y <= 4) {
      if (s == 0) g34f++;
      else g34m++;
    } else {
      if (s == 0) g56f++;
      else g56m++;
    }
  }

  int ans = 0;
  ans += rooms(g12, k);
  ans += rooms(g34f, k);
  ans += rooms(g34m, k);
  ans += rooms(g56f, k);
  ans += rooms(g56m, k);

  cout << ans << "\n";

  return 0;
}
```
