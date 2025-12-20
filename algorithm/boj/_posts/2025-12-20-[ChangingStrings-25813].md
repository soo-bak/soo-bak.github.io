---
layout: single
title: "[백준 25813] Changing Strings (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 문자열에서 좌측 U와 우측 F 사이를 규칙에 따라 U,C,F와 하이픈으로 변환하는 문제
---

## 문제 링크
[25813번 - Changing Strings](https://www.acmicpc.net/problem/25813)

## 설명
문자열에서 가장 왼쪽의 U와 가장 오른쪽의 F를 찾습니다. 왼쪽 U 이전은 '-', 오른쪽 F 이후도 '-', U~F 사이(양 끝 포함)는 'U','F'를 제외하고 모두 'C'로 바꿉니다. 입력엔 항상 U가 있고, 그 이후에 F가 있으며, 그 사이에 최소 한 문자가 있습니다.

<br>

## 접근법
`l = s.IndexOf('U')`, `r = s.LastIndexOf('F')`를 찾습니다. 새 문자열을 만들 때:
- i < l 또는 i > r ⇒ '-'
- i == l ⇒ 'U'
- i == r ⇒ 'F'
- 그 사이 ⇒ 'C'
길이가 최대 50이므로 간단히 O(n)으로 처리합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    int l = s.IndexOf('U');
    int r = s.LastIndexOf('F');

    var sb = new StringBuilder(s.Length);
    for (int i = 0; i < s.Length; i++) {
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

  string s;
  if (!(cin >> s)) return 0;
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
