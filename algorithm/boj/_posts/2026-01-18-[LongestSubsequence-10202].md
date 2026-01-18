---
layout: single
title: "[백준 10202] Longest Subsequence (C#, C++) - soo:bak"
date: "2026-01-18 19:10:00 +0900"
description: "백준 10202번 C#, C++ 풀이 - 문자열에서 연속된 X로만 이루어진 가장 긴 구간의 길이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 10202
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 10202, 백준 10202번, BOJ 10202, Longest Subsequence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10202번 - Longest Subsequence](https://www.acmicpc.net/problem/10202)

## 설명
각 테스트 케이스마다 X와 O로 이루어진 문자열이 주어질 때, 연속된 X로만 이루어진 가장 긴 구간의 길이를 구하는 문제입니다.

<br>

## 접근법
먼저 문자열을 앞에서부터 순회하며 각 문자가 X인지 확인합니다.

X가 나오면 연속 길이를 증가시키고, O가 나오면 연속 길이를 0으로 초기화하며 최대 길이를 갱신합니다.

모든 문자들을 확인하여 최대 길이를 구한 후 주어진 형식에 맞게 출력합니다.

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
    for (var tc = 0; tc < t; tc++) {
      var parts = Console.ReadLine()!.Split();
      var n = int.Parse(parts[0]);
      var cnt = 0;
      var best = 0;
      for (var i = 1; i <= n; i++) {
        if (parts[i] == "X") {
          cnt++;
          if (cnt > best)
            best = cnt;
        } else cnt = 0;
      }
      sb.Append("The longest contiguous subsequence of X's is of length ")
        .Append(best).Append('\n');
    }
    Console.Write(sb);
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

  int t; cin >> t;
  for (int tc = 0; tc < t; tc++) {
    int n; cin >> n;
    int cnt = 0, best = 0;
    for (int i = 0; i < n; i++) {
      string token; cin >> token;
      if (token == "X") {
        cnt++;
        best = max(best, cnt);
      } else cnt = 0;
    }
    cout << "The longest contiguous subsequence of X's is of length " << best << "\n";
  }

  return 0;
}
```
