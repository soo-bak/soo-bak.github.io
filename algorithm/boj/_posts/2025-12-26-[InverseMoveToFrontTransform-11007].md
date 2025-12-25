---
layout: single
title: "[백준 11007] Inverse Move-to-Front Transform (C#, C++) - soo:bak"
date: "2025-12-26 01:01:26 +0900"
description: 인덱스 수열로부터 원래 문자열을 복원하는 문제
---

## 문제 링크
[11007번 - Inverse Move-to-Front Transform](https://www.acmicpc.net/problem/11007)

## 설명
알파벳 리스트의 인덱스 수열이 주어질 때 원래 문자열을 복원하는 문제입니다.

<br>

## 접근법
먼저 알파벳 리스트를 a부터 z까지로 초기화합니다.

다음으로 인덱스를 하나 읽고 해당 위치의 문자를 출력한 뒤 그 문자를 맨 앞으로 옮깁니다.

이후 모든 인덱스를 처리하면 원래 문자열이 완성됩니다.

마지막으로 각 테스트 케이스의 문자열을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var tc = 0; tc < t; tc++) {
      var n = int.Parse(parts[idx++]);
      var list = new char[26];
      for (var i = 0; i < 26; i++)
        list[i] = (char)('a' + i);

      var outSb = new StringBuilder();
      for (var i = 0; i < n; i++) {
        var k = int.Parse(parts[idx++]);
        var ch = list[k];
        outSb.Append(ch);
        for (var j = k; j > 0; j--)
          list[j] = list[j - 1];
        list[0] = ch;
      }

      sb.AppendLine(outSb.ToString());
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

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    vector<char> list(26);
    for (int i = 0; i < 26; i++)
      list[i] = char('a' + i);

    string out;
    out.reserve(n);
    for (int i = 0; i < n; i++) {
      int k; cin >> k;
      char ch = list[k];
      out.push_back(ch);
      for (int j = k; j > 0; j--)
        list[j] = list[j - 1];
      list[0] = ch;
    }

    cout << out << "\n";
  }

  return 0;
}
```
