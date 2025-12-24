---
layout: single
title: "[백준 32288] 바코드 닉네임 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 문자열에서 l과 I의 대소문자를 서로 뒤집어 출력하는 문제
---

## 문제 링크
[32288번 - 바코드 닉네임](https://www.acmicpc.net/problem/32288)

## 설명
문자 l과 I로만 이루어진 문자열의 대소문자를 서로 바꿔 출력하는 문제입니다.

<br>

## 접근법
문자열을 순회하며 l은 L로, I는 i로 바꿔 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var sb = new StringBuilder();

    for (var i = 0; i < n; i++) {
      var ch = s[i];
      sb.Append(ch == 'l' ? 'L' : 'i');
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

  int n; cin >> n;
  string s; cin >> s;
  for (int i = 0; i < n; i++) {
    if (s[i] == 'l') s[i] = 'L';
    else s[i] = 'i';
  }

  cout << s << "\n";

  return 0;
}
```
