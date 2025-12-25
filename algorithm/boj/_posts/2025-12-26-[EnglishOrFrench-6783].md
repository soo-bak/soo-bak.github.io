---
layout: single
title: "[백준 6783] English or French? (C#, C++) - soo:bak"
date: "2025-12-26 02:31:00 +0900"
description: t와 s의 등장 횟수를 비교하는 문제
---

## 문제 링크
[6783번 - English or French?](https://www.acmicpc.net/problem/6783)

## 설명
여러 줄의 문장에서 t/T와 s/S의 등장 횟수를 비교해 언어를 판별하는 문제입니다.

<br>

## 접근법
먼저 모든 줄을 순회하며 t/T와 s/S의 개수를 셉니다.

다음으로 두 개수를 비교해 규칙에 맞는 결과를 선택합니다.

마지막으로 English 또는 French를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var tCnt = 0;
    var sCnt = 0;

    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!;
      for (var j = 0; j < line.Length; j++) {
        var c = line[j];
        if (c == 't' || c == 'T') tCnt++;
        else if (c == 's' || c == 'S') sCnt++;
      }
    }

    if (tCnt > sCnt) Console.WriteLine("English");
    else Console.WriteLine("French");
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
  string line; getline(cin, line);

  int tCnt = 0;
  int sCnt = 0;
  for (int i = 0; i < n; i++) {
    getline(cin, line);
    for (int j = 0; j < (int)line.size(); j++) {
      char c = line[j];
      if (c == 't' || c == 'T') tCnt++;
      else if (c == 's' || c == 'S') sCnt++;
    }
  }

  if (tCnt > sCnt) cout << "English\n";
  else cout << "French\n";
  return 0;
}
```
