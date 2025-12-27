---
layout: single
title: "[백준 6766] Big Bang Secrets (C#, C++) - soo:bak"
date: "2025-12-27 02:45:00 +0900"
description: 위치별로 다른 시프트를 역변환해 원문을 복호화하는 문제
---

## 문제 링크
[6766번 - Big Bang Secrets](https://www.acmicpc.net/problem/6766)

## 설명
각 위치 P의 문자를 3P + K 만큼 알파벳 순서로 앞당겨 암호화한 문자열이 주어집니다. 이를 다시 원문으로 복호화하는 문제입니다.

<br>

## 접근법
위치 P(1부터)마다 시프트 값 S = 3P + K 를 구하고, 해당 문자에서 S를 뒤로 이동시킵니다.

알파벳은 26자로 순환하므로 (c - 'A' - S) % 26을 이용해 복원합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var k = int.Parse(Console.ReadLine()!);
    var s = Console.ReadLine()!;
    var sb = new StringBuilder();

    for (var i = 0; i < s.Length; i++) {
      var shift = 3 * (i + 1) + k;
      var offset = (s[i] - 'A' - shift) % 26;
      if (offset < 0) offset += 26;
      sb.Append((char)('A' + offset));
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

  int k; cin >> k;
  string s; cin >> s;
  string res;
  res.reserve(s.size());

  for (int i = 0; i < (int)s.size(); i++) {
    int shift = 3 * (i + 1) + k;
    int offset = (s[i] - 'A' - shift) % 26;
    if (offset < 0) offset += 26;
    res += char('A' + offset);
  }

  cout << res << "\n";

  return 0;
}
```
