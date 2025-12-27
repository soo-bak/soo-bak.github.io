---
layout: single
title: "[백준 9777] Birthday Statistics (C#, C++) - soo:bak"
date: "2025-12-27 12:45:00 +0900"
description: 직원들의 생일 데이터에서 월별 인원 수를 집계하는 문제
---

## 문제 링크
[9777번 - Birthday Statistics](https://www.acmicpc.net/problem/9777)

## 설명
직원들의 생일이 주어질 때, 월별로 생일인 인원 수를 세어 출력하는 문제입니다.

<br>

## 접근법
월별 카운트를 저장할 배열을 두고, 각 날짜에서 월만 추출해 해당 인덱스를 증가시킵니다.

모든 입력을 처리한 뒤 1월부터 12월까지 순서대로 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var cnt = new int[13];
    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!;
      var parts = line.Split(' ');
      var date = parts[1];
      var dm = date.Split('/');
      var month = int.Parse(dm[1]);
      cnt[month]++;
    }

    for (var m = 1; m <= 12; m++)
      Console.WriteLine($"{m} {cnt[m]}");
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

  int n; cin >> n;
  vi cnt(13, 0);
  for (int i = 0; i < n; i++) {
    string id, date;
    cin >> id >> date;
    int day, month, year;
    char slash;
    stringstream ss(date);
    ss >> day >> slash >> month >> slash >> year;
    cnt[month]++;
  }

  for (int m = 1; m <= 12; m++)
    cout << m << " " << cnt[m] << "\n";

  return 0;
}
```
