---
layout: single
title: "[백준 31520] Champernowne Verification (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 정수 n이 1부터 k까지 이어 붙인 챔퍼나운 수인지 확인해 맞으면 k, 아니면 -1을 출력하는 문제
tags:
  - 백준
  - BOJ
  - 31520
  - C#
  - C++
  - 알고리즘
keywords: "백준 31520, 백준 31520번, BOJ 31520, ChampernowneVerification, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31520번 - Champernowne Verification](https://www.acmicpc.net/problem/31520)

## 설명
입력된 수가 1부터 k까지 숫자를 이어 붙인 값과 정확히 같으면 k를, 그렇지 않으면 -1을 출력하는 문제입니다.

<br>

## 접근법
입력을 문자열로 받아 길이를 맞춰가며 1부터 순서대로 이어 붙입니다. 누적 문자열 길이가 입력 길이와 같아지면 내용을 비교해 일치하면 그때의 k를, 일치하지 않으면 -1을 출력합니다. 길이를 초과하면 더 이상 맞을 수 없으므로 -1을 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var target = Console.ReadLine()!;
    var sb = new StringBuilder();
    var ans = -1;

    for (int i = 1; ; i++) {
      sb.Append(i);
      if (sb.Length == target.Length) {
        if (sb.ToString() == target) ans = i;
        break;
      }
      if (sb.Length > target.Length) break;
    }

    Console.WriteLine(ans);
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

  string target;
  if (!(cin >> target)) return 0;

  string s;
  int ans = -1;
  for (int i = 1;; i++) {
    s += to_string(i);
    if ((int)s.size() == (int)target.size()) {
      if (s == target) ans = i;
      break;
    }
    if ((int)s.size() > (int)target.size()) break;
  }

  cout << ans << "\n";

  return 0;
}
```
