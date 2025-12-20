---
layout: single
title: "[백준 30958] 서울사이버대학을 다니고 성공 (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: 문자열에서 알파벳만 세어 가장 많이 등장한 글자의 빈도를 구하는 문제
---

## 문제 링크
[30958번 - 서울사이버대학을 다니고 성공](https://www.acmicpc.net/problem/30958)

## 설명
로고송 문자열이 주어질 때, 알파벳 소문자만 세어 가장 많이 등장한 글자의 빈도를 구하는 문제입니다. 공백, 쉼표, 마침표는 제외합니다.

<br>

## 접근법
문자열을 순회하며 알파벳 소문자인 경우에만 해당 문자의 빈도를 증가시킵니다. 26개 크기의 배열에 각 알파벳의 등장 횟수를 기록한 뒤, 그중 최댓값을 출력하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    Console.ReadLine();
    var s = Console.ReadLine()!;

    var cnt = new int[26];
    foreach (var ch in s) {
      if (ch >= 'a' && ch <= 'z')
        cnt[ch - 'a']++;
    }

    var max = 0;
    foreach (var c in cnt)
      if (c > max) max = c;

    Console.WriteLine(max);
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
  cin.ignore();
  string s; getline(cin, s);

  int cnt[26] = {0};
  for (char c : s) {
    if ('a' <= c && c <= 'z')
      cnt[c - 'a']++;
  }

  int mx = 0;
  for (int i = 0; i < 26; i++)
    mx = max(mx, cnt[i]);

  cout << mx << "\n";

  return 0;
}
```
