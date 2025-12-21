---
layout: single
title: "[백준 9783] Easy Encryption (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: 문자별 매핑과 숫자 앞 # 규칙에 따라 문자열을 암호화하는 문제
---

## 문제 링크
[9783번 - Easy Encryption](https://www.acmicpc.net/problem/9783)

## 설명
문자별 매핑 규칙에 따라 문자열을 암호화하는 문제입니다.

<br>

## 접근법
소문자는 a부터 z까지 01부터 26으로, 대문자는 A부터 Z까지 27부터 52로 치환합니다. 숫자는 앞에 #을 붙여 그대로 출력하고, 그 외 문자는 변환 없이 그대로 둡니다.

각 문자를 순회하면서 해당하는 규칙을 적용해 결과 문자열에 누적한 뒤 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var s = Console.ReadLine()!;
    var sb = new StringBuilder();

    foreach (var ch in s) {
      if (ch >= 'a' && ch <= 'z') {
        var v = ch - 'a' + 1;
        sb.Append(v.ToString("D2"));
      } else if (ch >= 'A' && ch <= 'Z') {
        var v = ch - 'A' + 27;
        sb.Append(v.ToString("D2"));
      } else if (ch >= '0' && ch <= '9') {
        sb.Append('#').Append(ch);
      } else sb.Append(ch);
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

  string s; getline(cin, s);
  string out;

  for (char c : s) {
    if (c >= 'a' && c <= 'z') {
      int v = c - 'a' + 1;
      if (v < 10) out.push_back('0');
      out += to_string(v);
    } else if (c >= 'A' && c <= 'Z') {
      int v = c - 'A' + 27;
      out += to_string(v);
    } else if (c >= '0' && c <= '9') {
      out.push_back('#');
      out.push_back(c);
    } else out.push_back(c);
  }

  cout << out << "\n";

  return 0;
}
```
