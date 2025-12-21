---
layout: single
title: "[백준 18813] Divisionals Spelling (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: 대회 문제 A..(m개)로 중복 없는 단어를 만들 수 있는지 판단해 가능한 단어 수를 세는 문제
---

## 문제 링크
[18813번 - Divisionals Spelling](https://www.acmicpc.net/problem/18813)

## 설명
A부터 m번째 문자까지만 사용해 중복 없이 단어를 만들 수 있는지 판단하는 문제입니다.

<br>

## 접근법
각 단어가 조건을 만족하려면 세 가지를 확인해야 합니다. 단어의 길이가 m 이하여야 하고, 단어 내에 같은 글자가 두 번 이상 나오면 안 되며, 모든 글자가 A부터 m번째 문자 범위 안에 있어야 합니다.

각 단어를 순회하면서 세 조건을 모두 만족하면 개수를 증가시킵니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var m = int.Parse(first[1]);
    var ans = 0;

    for (var i = 0; i < n; i++) {
      var w = Console.ReadLine()!;
      if (w.Length > m) continue;

      var seen = new HashSet<char>();
      var ok = true;
      foreach (var ch in w) {
        if (seen.Contains(ch) || ch - 'A' >= m) { ok = false; break; }
        seen.Add(ch);
      }
      if (ok) ans++;
    }

    Console.WriteLine(ans);
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
  int ans = 0;

  for (int i = 0; i < n; i++) {
    string w; cin >> w;
    if ((int)w.size() > m) continue;

    bool used[26] = {};
    bool ok = true;
    for (char c : w) {
      int idx = c - 'A';
      if (idx >= m || used[idx]) { ok = false; break; }
      used[idx] = true;
    }
    if (ok) ans++;
  }

  cout << ans << "\n";

  return 0;
}
```
