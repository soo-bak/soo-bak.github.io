---
layout: single
title: "[백준 32860] 수수수수퍼노바 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 초신성 관측 순서를 표기 규칙에 맞게 변환하는 문제
---

## 문제 링크
[32860번 - 수수수수퍼노바](https://www.acmicpc.net/problem/32860)

## 설명
연도와 관측 순서가 주어질 때, 초신성 표기 규칙에 맞는 이름을 출력하는 문제입니다.

<br>

## 접근법
M이 1~26이면 대문자 A~Z로 표시하고, 27 이상이면 두 자리 소문자 조합으로 표시합니다.  
M≥27일 때는 `M-27`을 0부터 시작하는 인덱스로 두고 26진수처럼 계산해 앞/뒤 글자를 만듭니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var m = int.Parse(parts[1]);

    string code;
    if (m <= 26) code = ((char)('A' + m - 1)).ToString();
    else {
      var idx = m - 27;
      var first = (char)('a' + idx / 26);
      var second = (char)('a' + idx % 26);
      code = new string(new[] { first, second });
    }

    Console.WriteLine($"SN {n}{code}");
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

  int n, m; cin >> n >> m;
  string code;
  if (m <= 26) code.push_back(char('A' + m - 1));
  else {
    int idx = m - 27;
    code.push_back(char('a' + idx / 26));
    code.push_back(char('a' + idx % 26));
  }

  cout << "SN " << n << code << "\n";

  return 0;
}
```
