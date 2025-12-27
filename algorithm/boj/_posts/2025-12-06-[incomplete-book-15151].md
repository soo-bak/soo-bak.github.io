---
layout: single
title: "[백준 15151] Incomplete Book (C#, C++) - soo:bak"
date: "2025-12-06 17:52:00 +0900"
description: 첫 책부터 두 배씩 늘어나는 소요 일수로 완성 가능한 최대 책 수를 구하는 백준 15151번 Incomplete Book 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15151
  - C#
  - C++
  - 알고리즘
keywords: "백준 15151, 백준 15151번, BOJ 15151, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15151번 - Incomplete Book](https://www.acmicpc.net/problem/15151)

## 설명
첫 책은 k일이 걸리고, 이후 매 책마다 소요 일수가 2배씩 증가합니다.

시작 후 d일이 지나면 죽을 때, 완성할 수 있는 최대 책 수를 구하는 문제입니다.

<br>

## 접근법
먼저, 각 책의 소요 일수는 k, 2k, 4k, ... 순으로 기하급수적으로 증가합니다.

다음으로, 누적 합이 d를 넘지 않는 동안 책을 계속 씁니다. 다음 책까지 쓸 시간이 부족하면 중단합니다.

기하급수적으로 증가하므로 반복 횟수는 O(log(d/k))입니다. 값이 커질 수 있어 64비트 정수를 사용합니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var parts = Console.ReadLine()!.Split();
      var k = long.Parse(parts[0]);
      var d = long.Parse(parts[1]);

      var days = k;
      var used = 0L;
      var cnt = 0L;
      while (used + days <= d) {
        used += days;
        cnt++;
        days <<= 1;
      }
      Console.WriteLine(cnt);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll k, d; cin >> k >> d;
  ll cur = k, sum = 0, cnt = 0;
  while (sum + cur <= d) {
    sum += cur;
    cnt++;
    cur <<= 1;
  }
  cout << cnt << "\n";

  return 0;
}
```
