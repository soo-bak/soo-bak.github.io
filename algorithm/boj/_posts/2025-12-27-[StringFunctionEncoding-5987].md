---
layout: single
title: "[백준 5987] String Function Encoding (C#, C++) - soo:bak"
date: "2025-12-27 00:55:00 +0900"
description: 문자열 변환 함수를 반복 적용하는 백준 5987번 String Function Encoding 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5987
  - C#
  - C++
  - 알고리즘
keywords: "백준 5987, 백준 5987번, BOJ 5987, StringFunctionEncoding, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5987번 - String Function Encoding](https://www.acmicpc.net/problem/5987)

## 설명
문자열 S에 대해 N번째 이후 부분을 앞으로 보내고 원래 문자열을 뒤에 붙이는 연산을 C번 반복한 결과를 출력하는 문제입니다.

<br>

## 접근법
현재 문자열에서 N번째 이후 부분을 잘라서 앞에 붙이고, 원래 문자열 전체를 뒤에 붙입니다.

이 과정을 C번 반복하면 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var z = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var t = 0; t < z; t++) {
      var n = int.Parse(parts[idx++]);
      var c = int.Parse(parts[idx++]);
      var s = parts[idx++];

      for (var i = 0; i < c; i++)
        s = s.Substring(n) + s;

      sb.AppendLine(s);
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

  int z; cin >> z;
  for (int t = 0; t < z; t++) {
    int n, c; string s; cin >> n >> c >> s;
    for (int i = 0; i < c; i++)
      s = s.substr(n) + s;
    cout << s << "\n";
  }

  return 0;
}
```
