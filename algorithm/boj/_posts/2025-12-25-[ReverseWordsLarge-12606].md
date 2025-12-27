---
layout: single
title: "[백준 12606] Reverse Words (Large) (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 12606번 C#, C++ 풀이 - 문장을 단어 단위로 뒤집어 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 12606
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
  - 파싱
keywords: "백준 12606, 백준 12606번, BOJ 12606, ReverseWordsLarge, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12606번 - Reverse Words (Large)](https://www.acmicpc.net/problem/12606)

## 설명
각 문장을 단어 단위로 나눠 순서를 뒤집어 출력하는 문제입니다.

<br>

## 접근법
한 줄을 통째로 읽고 공백 기준으로 단어를 분리한 뒤, 뒤에서부터 이어서 출력합니다.  
각 테스트 케이스는 `Case #x: ` 형식으로 시작합니다.

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

    for (var caseNo = 1; caseNo <= t; caseNo++) {
      var line = Console.ReadLine()!;
      var words = line.Split(' ');

      sb.Append("Case #").Append(caseNo).Append(": ");
      for (var i = words.Length - 1; i >= 0; i--) {
        if (i < words.Length - 1) sb.Append(' ');
        sb.Append(words[i]);
      }
      sb.AppendLine();
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
  string line;
  getline(cin, line);

  for (int caseNo = 1; caseNo <= t; caseNo++) {
    getline(cin, line);
    stringstream ss(line);
    vector<string> words;
    string w;
    while (ss >> w) words.push_back(w);

    cout << "Case #" << caseNo << ": ";
    for (int i = (int)words.size() - 1; i >= 0; i--) {
      if (i < (int)words.size() - 1) cout << ' ';
      cout << words[i];
    }
    cout << "\n";
  }

  return 0;
}
```
