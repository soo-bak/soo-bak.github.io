---
layout: single
title: "[백준 28455] Union Maplestory (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 상위 42명의 레벨 합과 상승 능력치 합을 구하는 문제
---

## 문제 링크
[28455번 - Union Maplestory](https://www.acmicpc.net/problem/28455)

## 설명
캐릭터 레벨이 주어질 때, 레벨 내림차순으로 최대 42명을 뽑아 레벨 합과 능력치 증가 합을 출력하는 문제입니다.

<br>

## 접근법
레벨을 내림차순으로 정렬한 뒤 상위 42명(또는 전체)을 선택합니다.  
각 캐릭터는 레벨이 60, 100, 140, 200, 250 이상일 때마다 능력치가 1씩 증가하므로, 이 기준을 세어 합산합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Stat(int level) {
    var cnt = 0;
    if (level >= 60) cnt++;
    if (level >= 100) cnt++;
    if (level >= 140) cnt++;
    if (level >= 200) cnt++;
    if (level >= 250) cnt++;
    return cnt;
  }

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var levels = new int[n];
    for (var i = 0; i < n; i++)
      levels[i] = int.Parse(Console.ReadLine()!);

    Array.Sort(levels);
    Array.Reverse(levels);

    var take = Math.Min(42, n);
    var sumLevel = 0;
    var sumStat = 0;
    for (var i = 0; i < take; i++) {
      var lvl = levels[i];
      sumLevel += lvl;
      sumStat += Stat(lvl);
    }

    Console.WriteLine($"{sumLevel} {sumStat}");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int stat(int level) {
  int cnt = 0;
  if (level >= 60) cnt++;
  if (level >= 100) cnt++;
  if (level >= 140) cnt++;
  if (level >= 200) cnt++;
  if (level >= 250) cnt++;
  return cnt;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi levels(n);
  for (int i = 0; i < n; i++)
    cin >> levels[i];

  sort(levels.begin(), levels.end(), greater<int>());

  int take = min(42, n);
  int sumLevel = 0, sumStat = 0;
  for (int i = 0; i < take; i++) {
    sumLevel += levels[i];
    sumStat += stat(levels[i]);
  }

  cout << sumLevel << " " << sumStat << "\n";

  return 0;
}
```
