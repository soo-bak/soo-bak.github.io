---
layout: single
title: "[백준 4285] Prerequisites? (C#, C++) - soo:bak"
date: "2025-12-27 06:15:00 +0900"
description: "백준 4285번 C#, C++ 풀이 - 선택한 과목이 각 카테고리의 최소 이수 조건을 만족하는지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 4285
  - C#
  - C++
  - 알고리즘
keywords: "백준 4285, 백준 4285번, BOJ 4285, Prerequisites, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4285번 - Prerequisites?](https://www.acmicpc.net/problem/4285)

## 설명
프레디가 선택한 과목 k개와 m개의 카테고리 요구사항이 주어집니다. 각 카테고리는 c개 과목 중 r개 이상을 들어야 합니다. 프레디의 선택이 모든 카테고리를 만족하면 "yes", 아니면 "no"를 출력합니다. 입력은 0이 나오면 종료합니다.

<br>

## 접근법
프레디 선택 과목을 집합으로 저장한 뒤, 각 카테고리에서 요구 과목 리스트와의 교집합 크기가 r 이상인지 확인합니다.

모든 카테고리가 조건을 만족하면 yes, 하나라도 부족하면 no입니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

class Program {
  static void Main() {
    var sb = new StringBuilder();
    string? line;
    while ((line = Console.ReadLine()) != null) {
      if (line.Trim() == "0") break;
      var first = line.Split();
      var k = int.Parse(first[0]);
      var m = int.Parse(first[1]);

      var chosen = new HashSet<string>();
      var tokens = Console.ReadLine()!.Split();
      foreach (var t in tokens) chosen.Add(t);

      var ok = true;
      for (var i = 0; i < m; i++) {
        var parts = Console.ReadLine()!.Split();
        var c = int.Parse(parts[0]);
        var r = int.Parse(parts[1]);
        var cnt = 0;
        for (var j = 0; j < c; j++) {
          if (chosen.Contains(parts[2 + j])) cnt++;
        }
        if (cnt < r) ok = false;
      }
      sb.AppendLine(ok ? "yes" : "no");
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
    if (line == "0") break;
    stringstream ss(line);
    int k, m; ss >> k >> m;

    vector<string> chosenVec;
    chosenVec.reserve(k);
    {
      getline(cin, line);
      stringstream cs(line);
      string s;
      while (cs >> s)
        chosenVec.push_back(s);
    }
    unordered_set<string> chosen(chosenVec.begin(), chosenVec.end());

    bool ok = true;
    for (int i = 0; i < m; i++) {
      getline(cin, line);
      stringstream cat(line);
      int c, r; cat >> c >> r;
      int cnt = 0;
      for (int j = 0; j < c; j++) {
        string course; cat >> course;
        if (chosen.count(course)) cnt++;
      }
      if (cnt < r) ok = false;
    }
    cout << (ok ? "yes" : "no") << "\n";
  }
  return 0;
}
```
