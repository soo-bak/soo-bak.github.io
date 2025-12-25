---
layout: single
title: "[백준 9954] Cedric's Cypher (C#, C++) - soo:bak"
date: "2025-12-26 00:56:05 +0900"
description: 마지막 문자로 이동량을 알아내 평문을 복원하는 문제
---

## 문제 링크
[9954번 - Cedric's Cypher](https://www.acmicpc.net/problem/9954)

## 설명
각 줄의 마지막 문자를 이용해 시프트 값을 알아내고 암호문을 복호화하는 문제입니다.

<br>

## 접근법
먼저 한 줄의 마지막 문자를 읽어 이동량을 결정합니다.

다음으로 그 문자를 제외한 나머지 부분을 한 글자씩 복호화합니다.

이후 알파벳은 대소문자를 유지하며 순환하도록 처리하고, 그 외 문자는 그대로 둡니다.

마지막으로 #이 나올 때까지 각 줄을 변환해 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var sb = new StringBuilder();
    while (true) {
      var line = Console.ReadLine();
      if (line == null || line == "#") break;
      var shift = line[line.Length - 1] - 'A';

      var outSb = new StringBuilder();
      for (var i = 0; i < line.Length - 1; i++) {
        var c = line[i];
        if (c >= 'A' && c <= 'Z') {
          var v = c - 'A' - shift;
          if (v < 0) v += 26;
          outSb.Append((char)('A' + v));
        } else if (c >= 'a' && c <= 'z') {
          var v = c - 'a' - shift;
          if (v < 0) v += 26;
          outSb.Append((char)('a' + v));
        } else outSb.Append(c);
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

  string line;
  while (getline(cin, line)) {
    if (line == "#") break;
    int shift = line.back() - 'A';
    string out;
    for (int i = 0; i + 1 < (int)line.size(); i++) {
      char c = line[i];
      if (c >= 'A' && c <= 'Z') {
        int v = c - 'A' - shift;
        if (v < 0) v += 26;
        out.push_back(char('A' + v));
      } else if (c >= 'a' && c <= 'z') {
        int v = c - 'a' - shift;
        if (v < 0) v += 26;
        out.push_back(char('a' + v));
      } else out.push_back(c);
    }
    cout << out << "\n";
  }

  return 0;
}
```
