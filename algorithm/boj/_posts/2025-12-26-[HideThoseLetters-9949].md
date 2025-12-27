---
layout: single
title: "[백준 9949] Hide those Letters (C#, C++) - soo:bak"
date: "2025-12-26 00:30:09 +0900"
description: "백준 9949번 C#, C++ 풀이 - 두 글자를 대소문자 구분 없이 밑줄로 바꾸는 문제"
tags:
  - 백준
  - BOJ
  - 9949
  - C#
  - C++
  - 알고리즘
keywords: "백준 9949, 백준 9949번, BOJ 9949, HideThoseLetters, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9949번 - Hide those Letters](https://www.acmicpc.net/problem/9949)

## 설명
두 문자와 여러 줄의 문장이 주어질 때 해당 문자를 대소문자 구분 없이 밑줄로 치환하는 문제입니다.

<br>

## 접근법
먼저 두 문자를 읽고 종료 표식인지 확인합니다.

다음으로 각 줄을 순회하며 해당 문자와 같으면 밑줄로 바꿉니다.

이후 케이스 번호와 변환된 문장을 출력하고, 케이스 사이에 빈 줄을 넣습니다.

마지막으로 모든 케이스를 처리합니다.

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
    var caseNum = 1;

    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      if (line == "# #") break;

      var parts = line.Split();
      var c1 = parts[0][0];
      var c2 = parts[1][0];
      var n = int.Parse(Console.ReadLine()!);

      sb.AppendLine($"Case {caseNum}");
      for (var i = 0; i < n; i++) {
        var text = Console.ReadLine()!;
        var arr = text.ToCharArray();
        for (var j = 0; j < arr.Length; j++) {
          var ch = arr[j];
          if (ch == c1 || ch == c2 || ch == char.ToUpper(c1) || ch == char.ToUpper(c2))
            arr[j] = '_';
        }
        sb.AppendLine(new string(arr));
      }

      sb.AppendLine();
      caseNum++;
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
  int caseNum = 1;
  bool first = true;

  while (getline(cin, line)) {
    if (line == "# #") break;
    stringstream ss(line);
    char c1, c2;
    ss >> c1 >> c2;

    string nLine;
    getline(cin, nLine);
    int n = stoi(nLine);

    if (!first) cout << "\n";
    first = false;
    cout << "Case " << caseNum << "\n";
    for (int i = 0; i < n; i++) {
      string text;
      getline(cin, text);
      for (char &ch : text) {
        if (ch == c1 || ch == c2 || ch == toupper(c1) || ch == toupper(c2))
          ch = '_';
      }
      cout << text << "\n";
    }

    caseNum++;
  }

  return 0;
}
```
