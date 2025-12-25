---
layout: single
title: "[백준 30700] KOREA 문자열 만들기 성공 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 삭제로 만들 수 있는 가장 긴 KOREA 반복 문자열의 길이를 구하는 문제
---

## 문제 링크
[30700번 - KOREA 문자열 만들기 성공](https://www.acmicpc.net/problem/30700)

## 설명
K, O, R, E, A로만 이루어진 문자열 S에서 문자를 지워 `KOREA` 순서를 반복하는 문자열을 만들 때 가능한 최대 길이를 구하는 문제입니다.

<br>

## 접근법
`KOREA` 패턴의 현재 위치를 가리키는 인덱스를 두고 문자열을 왼쪽부터 확인합니다.  
문자가 일치할 때마다 길이를 늘리고 인덱스를 다음 문자로 옮기며, A 다음은 K로 돌아갑니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var pattern = "KOREA";
    var idx = 0;
    var len = 0;

    foreach (var ch in s) {
      if (ch == pattern[idx]) {
        len++;
        idx = (idx + 1) % 5;
      }
    }

    Console.WriteLine(len);
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

  string s; cin >> s;
  string pattern = "KOREA";
  int idx = 0, len = 0;

  for (char ch : s) {
    if (ch == pattern[idx]) {
      len++;
      idx = (idx + 1) % 5;
    }
  }

  cout << len << "\n";

  return 0;
}
```
