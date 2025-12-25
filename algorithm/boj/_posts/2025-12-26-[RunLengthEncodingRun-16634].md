---
layout: single
title: "[백준 16634] Run-Length Encoding, Run! (C#, C++) - soo:bak"
date: "2025-12-26 02:44:00 +0900"
description: 문자열을 RLE로 인코딩/디코딩하는 문제
---

## 문제 링크
[16634번 - Run-Length Encoding, Run!](https://www.acmicpc.net/problem/16634)

## 설명
입력이 E면 연속 문자를 개수로 압축하고, D면 압축된 문자열을 원래 문자열로 복원하는 문제입니다.

<br>

## 접근법
먼저 첫 글자로 인코딩인지 디코딩인지 구분합니다.

인코딩은 같은 문자가 이어지는 구간을 세어 문자와 개수를 순서대로 이어 붙입니다.

디코딩은 문자와 숫자를 한 쌍씩 읽어 숫자만큼 문자를 반복해 이어 붙입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var line = Console.ReadLine()!;
    var mode = line[0];
    var s = line.Substring(2);

    if (mode == 'E') {
      var sb = new StringBuilder();
      var i = 0;
      while (i < s.Length) {
        var j = i + 1;
        while (j < s.Length && s[j] == s[i])
          j++;

        sb.Append(s[i]);
        sb.Append(j - i);
        i = j;
      }
      Console.WriteLine(sb.ToString());
    } else {
      var sb = new StringBuilder();
      for (var i = 0; i < s.Length; i += 2) {
        var ch = s[i];
        var cnt = s[i + 1] - '0';
        for (var k = 0; k < cnt; k++)
          sb.Append(ch);
      }
      Console.WriteLine(sb.ToString());
    }
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

  string line; getline(cin, line);

  char mode = line[0];
  string s = line.substr(2);

  if (mode == 'E') {
    string out;
    int i = 0;
    while (i < (int)s.size()) {
      int j = i + 1;
      while (j < (int)s.size() && s[j] == s[i])
        j++;

      out.push_back(s[i]);
      out.push_back(char('0' + (j - i)));
      i = j;
    }
    cout << out << "\n";
  } else {
    string out;
    for (int i = 0; i < (int)s.size(); i += 2) {
      char ch = s[i];
      int cnt = s[i + 1] - '0';
      for (int k = 0; k < cnt; k++)
        out.push_back(ch);
    }
    cout << out << "\n";
  }

  return 0;
}
```
