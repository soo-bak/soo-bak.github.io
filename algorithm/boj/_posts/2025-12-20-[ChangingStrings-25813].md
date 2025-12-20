---
layout: single
title: "[백준 25813] Changing Strings (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 문자열에서 좌측 U와 우측 F 사이를 규칙에 따라 U,C,F와 하이픈으로 변환하는 문제
---

## 문제 링크
[25813번 - Changing Strings](https://www.acmicpc.net/problem/25813)

## 설명
문자열에서 가장 왼쪽의 U와 가장 오른쪽의 F를 찾아 규칙에 따라 변환하는 문제입니다.

U 이전과 F 이후는 하이픈으로, U와 F 사이의 문자는 모두 C로 바꿉니다.

<br>

## 접근법
가장 왼쪽 U의 위치와 가장 오른쪽 F의 위치를 찾습니다. 각 인덱스에 대해 U 이전이거나 F 이후면 하이픈, U 위치면 U, F 위치면 F, 그 사이면 C를 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var l = s.IndexOf('U');
    var r = s.LastIndexOf('F');

    var sb = new StringBuilder(s.Length);
    for (var i = 0; i < s.Length; i++) {
      char ch;
      if (i < l || i > r) ch = '-';
      else if (i == l) ch = 'U';
      else if (i == r) ch = 'F';
      else ch = 'C';
      sb.Append(ch);
    }

    Console.WriteLine(sb.ToString());
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
  int l = s.find('U');
  int r = s.rfind('F');

  string out;
  out.reserve(s.size());
  for (int i = 0; i < (int)s.size(); i++) {
    char ch;
    if (i < l || i > r) ch = '-';
    else if (i == l) ch = 'U';
    else if (i == r) ch = 'F';
    else ch = 'C';
    out.push_back(ch);
  }

  cout << out << "\n";

  return 0;
}
```
