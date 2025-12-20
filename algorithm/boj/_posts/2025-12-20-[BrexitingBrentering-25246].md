---
layout: single
title: "[백준 25246] Brexiting and Brentering (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 주어진 이름에서 마지막 모음 이후를 잘라내고 ntry를 붙이는 문제
---

## 문제 링크
[25246번 - Brexiting and Brentering](https://www.acmicpc.net/problem/25246)

## 설명
주어진 이름에서 마지막 모음 이후를 잘라내고 ntry를 붙이는 문제입니다.

<br>

## 접근법
문자열을 뒤에서부터 순회하며 마지막 모음의 위치를 찾습니다. 그 위치까지 포함하여 문자열을 자른 뒤 ntry를 이어 붙여 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static bool IsVowel(char c) => c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';

  static void Main() {
    var s = Console.ReadLine()!;

    var idx = -1;
    for (var i = s.Length - 1; i >= 0; i--) {
      if (IsVowel(s[i])) { idx = i; break; }
    }

    Console.WriteLine(s.Substring(0, idx + 1) + "ntry");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isVowel(char c) {
  return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string s; cin >> s;

  int idx = -1;
  for (int i = (int)s.size() - 1; i >= 0; i--) {
    if (isVowel(s[i])) { idx = i; break; }
  }

  cout << s.substr(0, idx + 1) + "ntry" << "\n";

  return 0;
}
```
