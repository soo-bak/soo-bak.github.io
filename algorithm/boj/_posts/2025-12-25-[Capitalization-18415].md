---
layout: single
title: "[백준 18415] キャピタリゼーション (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 18415번 C#, C++ 풀이 - 문자열에서 joi를 찾아 JOI로 바꾸는 문제"
tags:
  - 백준
  - BOJ
  - 18415
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 18415, 백준 18415번, BOJ 18415, Capitalization, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18415번 - キャピタリゼーション](https://www.acmicpc.net/problem/18415)

## 설명
문자열 S에서 연속한 "joi"를 모두 "JOI"로 바꿔 출력하는 문제입니다.

<br>

## 접근법
문자열을 왼쪽부터 보면서 "joi"가 나오면 그 부분만 대문자로 바꿉니다.  

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var arr = s.ToCharArray();

    for (var i = 0; i + 2 < n; i++) {
      if (arr[i] == 'j' && arr[i + 1] == 'o' && arr[i + 2] == 'i') {
        arr[i] = 'J';
        arr[i + 1] = 'O';
        arr[i + 2] = 'I';
      }
    }

    Console.WriteLine(new string(arr));
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

  int n; cin >> n;
  string s; cin >> s;

  for (int i = 0; i + 2 < n; i++) {
    if (s[i] == 'j' && s[i + 1] == 'o' && s[i + 2] == 'i') {
      s[i] = 'J';
      s[i + 1] = 'O';
      s[i + 2] = 'I';
    }
  }

  cout << s << "\n";

  return 0;
}
```
