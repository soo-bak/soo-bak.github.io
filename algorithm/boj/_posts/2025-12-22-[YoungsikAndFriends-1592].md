---
layout: single
title: "[백준 1592] 영식이와 친구들 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 1592번 C#, C++ 풀이 - 공을 받은 횟수의 홀짝에 따라 방향을 바꿔 던질 때 총 던진 횟수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 1592
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 1592, 백준 1592번, BOJ 1592, YoungsikAndFriends, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1592번 - 영식이와 친구들](https://www.acmicpc.net/problem/1592)

## 설명
원형으로 앉아 공을 던질 때, 한 사람이 M번 받을 때까지 던진 횟수를 구하는 문제입니다.

<br>

## 접근법
각 자리의 받은 횟수를 배열로 관리합니다. 현재 사람이 공을 받은 횟수가 홀수면 시계 방향으로, 짝수면 반시계 방향으로 주어진 칸 수만큼 이동합니다.

이후 누군가 목표 횟수만큼 받으면 종료하고 던진 횟수를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var m = int.Parse(parts[1]);
    var l = int.Parse(parts[2]);

    var cnt = new int[n];
    var cur = 0;
    cnt[cur] = 1;
    var throws = 0;

    while (cnt[cur] < m) {
      if (cnt[cur] % 2 == 1) cur = (cur + l) % n;
      else cur = (cur - l + n) % n;
      cnt[cur]++;
      throws++;
    }

    Console.WriteLine(throws);
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

  int n, m, l; cin >> n >> m >> l;
  vi cnt(n, 0);
  int cur = 0;
  cnt[cur] = 1;
  int throws = 0;

  while (cnt[cur] < m) {
    if (cnt[cur] % 2 == 1) cur = (cur + l) % n;
    else cur = (cur - l + n) % n;
    cnt[cur]++;
    throws++;
  }

  cout << throws << "\n";

  return 0;
}
```
