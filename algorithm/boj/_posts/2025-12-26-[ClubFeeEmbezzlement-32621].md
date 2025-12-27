---
layout: single
title: "[백준 32621] 동아리비 횡령 (C#, C++) - soo:bak"
date: "2025-12-26 00:25:12 +0900"
description: "백준 32621번 C#, C++ 풀이 - 같은 수를 더한 꼴인지 판별해 결과를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 32621
  - C#
  - C++
  - 알고리즘
keywords: "백준 32621, 백준 32621번, BOJ 32621, ClubFeeEmbezzlement, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32621번 - 동아리비 횡령](https://www.acmicpc.net/problem/32621)

## 설명
문자열이 같은 양의 정수를 더한 형태인지 판단해 결과를 출력하는 문제입니다.

<br>

## 접근법
먼저 문자열에 더하기 기호가 정확히 하나인지 확인합니다.

다음으로 기호의 양쪽 문자열이 비어 있지 않고 서로 같은지 확인합니다.

이후 양쪽이 숫자로만 이루어졌고 앞자리가 0이 아닌지 검사합니다.

마지막으로 모든 조건을 만족하면 CUTE, 아니면 No Money를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var ok = true;

    var p = s.IndexOf('+');
    if (p < 0 || p != s.LastIndexOf('+')) ok = false;
    else if (p == 0 || p == s.Length - 1) ok = false;
    else {
      var left = s.Substring(0, p);
      var right = s.Substring(p + 1);
      if (left != right) ok = false;
      else if (left[0] == '0') ok = false;
      else {
        for (var i = 0; i < left.Length; i++) {
          var c = left[i];
          if (c < '0' || c > '9') { ok = false; break; }
        }
      }
    }

    Console.WriteLine(ok ? "CUTE" : "No Money");
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
  bool ok = true;

  int p = (int)s.find('+');
  if (p == (int)string::npos || p != (int)s.rfind('+')) ok = false;
  else if (p == 0 || p == (int)s.size() - 1) ok = false;
  else {
    string left = s.substr(0, p);
    string right = s.substr(p + 1);
    if (left != right) ok = false;
    else if (left[0] == '0') ok = false;
    else {
      for (char c : left) {
        if (c < '0' || c > '9') { ok = false; break; }
      }
    }
  }

  cout << (ok ? "CUTE" : "No Money") << "\n";
  return 0;
}
```
