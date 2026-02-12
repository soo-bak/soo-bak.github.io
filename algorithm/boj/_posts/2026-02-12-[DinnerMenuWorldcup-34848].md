---
layout: single
title: "[백준 34848] 저녁 메뉴 월드컵 (C#, C++) - soo:bak"
date: "2026-02-12 22:18:00 +0900"
description: "백준 34848번 C#, C++ 풀이 - 토너먼트 진행 시 발생하는 부전승 횟수 구하기"
tags:
  - 백준
  - BOJ
  - 34848
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 34848, 백준 34848번, BOJ 34848, 저녁 메뉴 월드컵, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[34848번 - 저녁 메뉴 월드컵](https://www.acmicpc.net/problem/34848)

## 설명
매 라운드에서 남은 개수가 홀수이면 한 메뉴가 부전승을 하는 방ㅅ힉으로 진행되는 토너먼트에서, 마지막 1개가 남을 때까지 발생하는 부전승의 횟수를 구하는 문제입니다.

<br>

## 접근법
현재 참가자 수를 n이라 할 때, 부전승은 n이 홀수일 때 1회 발생합니다.

다음 라운드 참가자 수는 (n+1) / 2이므로 n을 갱신하며 n > 1 동안 반복해서 홀수 여부를 더하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    for (int _ = 0; _ < t; _++) {
      long n = long.Parse(Console.ReadLine()!);
      long bye = 0;
      while (n > 1) {
        if ((n & 1) == 1) bye++;
        n = (n + 1) >> 1;
      }
      sb.Append(bye).Append('\n');
    }
    Console.Write(sb.ToString());
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

  int t; cin >> t;
  while (t--) {
    ll n; cin >> n;
    ll bye = 0;
    while (n > 1) {
      if (n & 1) bye++;
      n = (n + 1) >> 1;
    }
    cout << bye << "\n";
  }
  return 0;
}
```
