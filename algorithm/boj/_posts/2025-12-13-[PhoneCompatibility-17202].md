---
layout: single
title: "[백준 17202] 핸드폰 번호 궁합 (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 두 번호를 교차해 쓰고 인접 합의 일의 자리만 남기며 2자리로 줄이는 과정을 반복해 궁합률을 구하는 백준 17202번 핸드폰 번호 궁합 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17202
  - C#
  - C++
  - 알고리즘
keywords: "백준 17202, 백준 17202번, BOJ 17202, PhoneCompatibility, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17202번 - 핸드폰 번호 궁합](https://www.acmicpc.net/problem/17202)

## 설명
두 사람의 전화번호를 이용해 궁합률을 계산하는 문제입니다.

<br>

## 접근법
먼저 두 번호의 숫자를 번갈아 적어 길이 16의 수열을 만듭니다.

이후 인접한 두 숫자를 더한 값의 일의 자리만 남기는 과정을 반복합니다.

수열의 길이가 2가 되면 그 두 숫자가 궁합률이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var a = Console.ReadLine()!;
    var b = Console.ReadLine()!;

    var cur = new List<int>(16);
    for (var i = 0; i < a.Length; i++) {
      cur.Add(a[i] - '0');
      cur.Add(b[i] - '0');
    }

    while (cur.Count > 2) {
      var next = new List<int>(cur.Count - 1);
      for (var i = 0; i + 1 < cur.Count; i++)
        next.Add((cur[i] + cur[i + 1]) % 10);
      cur = next;
    }

    Console.Write(cur[0]);
    Console.Write(cur[1]);
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

  string a, b; cin >> a >> b;
  vi cur;
  cur.reserve(16);
  for (int i = 0; i < (int)a.size(); i++) {
    cur.push_back(a[i] - '0');
    cur.push_back(b[i] - '0');
  }

  while (cur.size() > 2) {
    vi nxt;
    nxt.reserve(cur.size() - 1);
    for (int i = 0; i + 1 < (int)cur.size(); i++)
      nxt.push_back((cur[i] + cur[i + 1]) % 10);
    cur.swap(nxt);
  }

  cout << cur[0] << cur[1] << "\n";

  return 0;
}
```
