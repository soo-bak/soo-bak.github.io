---
layout: single
title: "[백준 15780] 멀티탭 충분하니? (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 멀티탭 구 수를 절반 올림으로 더해 꽂을 수 있는 자리 수를 계산하고 학생 수와 비교하는 백준 15780번 멀티탭 충분하니? 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[15780번 - 멀티탭 충분하니?](https://www.acmicpc.net/problem/15780)

## 설명
멀티탭들의 구 수가 주어질 때, 모든 학생이 충전할 수 있는지 판단하는 문제입니다.

<br>

## 접근법
같은 멀티탭에서 2구 연속으로 꽂을 수 없으므로, 구 수가 A인 멀티탭에서는 절반을 올림한 만큼만 사용할 수 있습니다.

모든 멀티탭에서 사용 가능한 자리 수를 더한 값이 학생 수 이상이면 충분합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var nk = Console.ReadLine()!.Split();
    var n = int.Parse(nk[0]);
    var k = int.Parse(nk[1]);
    var line = Console.ReadLine()!.Split();
    var seats = 0;
    for (var i = 0; i < k; i++) {
      var a = int.Parse(line[i]);
      seats += (a + 1) / 2;
    }
    Console.WriteLine(seats >= n ? "YES" : "NO");
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

  int n, k; cin >> n >> k;
  int seats = 0;
  for (int i = 0; i < k; i++) {
    int a; cin >> a;
    seats += (a + 1) / 2;
  }
  cout << (seats >= n ? "YES" : "NO") << "\n";

  return 0;
}
```
