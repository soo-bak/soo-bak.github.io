---
layout: single
title: "[백준 3778] 애너그램 거리 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: 두 단어의 알파벳 개수 차이 합으로 애너그램 거리를 구하는 문제
---

## 문제 링크
[3778번 - 애너그램 거리](https://www.acmicpc.net/problem/3778)

## 설명
두 단어가 애너그램이 되기 위해 삭제해야 하는 문자 수의 최소합을 구하는 문제입니다.

<br>

## 접근법
각 단어의 알파벳 빈도를 세어 차이를 구합니다.

따라서 알파벳별 차이의 절댓값을 모두 더하면 애너그램 거리가 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    for (var tc = 1; tc <= t; tc++) {
      var a = Console.ReadLine();
      var b = Console.ReadLine();
      if (a == null) a = "";
      if (b == null) b = "";

      var cnt = new int[26];
      foreach (var ch in a)
        cnt[ch - 'a']++;
      foreach (var ch in b)
        cnt[ch - 'a']--;

      var dist = 0;
      for (var i = 0; i < 26; i++)
        dist += Math.Abs(cnt[i]);

      sb.AppendLine($"Case #{tc}: {dist}");
    }

    Console.Write(sb.ToString());
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

  int t; cin >> t;
  string a, b;
  getline(cin, a);

  for (int tc = 1; tc <= t; tc++) {
    getline(cin, a);
    getline(cin, b);

    int cnt[26] = {};
    for (char ch : a)
      cnt[ch - 'a']++;
    for (char ch : b)
      cnt[ch - 'a']--;

    int dist = 0;
    for (int i = 0; i < 26; i++)
      dist += abs(cnt[i]);

    cout << "Case #" << tc << ": " << dist << "\n";
  }

  return 0;
}
```
