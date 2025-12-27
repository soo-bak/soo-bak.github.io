---
layout: single
title: "[백준 11531] ACM 대회 채점 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 11531번 C#, C++ 풀이 - 제출 로그를 바탕으로 해결 수와 페널티 합을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 11531
  - C#
  - C++
  - 알고리즘
keywords: "백준 11531, 백준 11531번, BOJ 11531, ACMContestScoring, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11531번 - ACM 대회 채점](https://www.acmicpc.net/problem/11531)

## 설명
제출 로그가 주어질 때 해결한 문제 수와 총 페널티를 계산하는 문제입니다.

<br>

## 접근법
문제별로 틀린 횟수와 해결 여부를 저장합니다.  
right가 처음 나올 때만 해결 처리하고, 그 시각과 틀린 횟수×20을 합산합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var wrong = new Dictionary<string, int>();
    var solved = new HashSet<string>();
    var solvedCnt = 0;
    var penalty = 0;

    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      if (line == "-1") break;
      var parts = line.Split();
      var time = int.Parse(parts[0]);
      var prob = parts[1];
      var res = parts[2];

      if (solved.Contains(prob)) continue;
      if (res == "right") {
        solvedCnt++;
        var w = wrong.ContainsKey(prob) ? wrong[prob] : 0;
        penalty += time + w * 20;
        solved.Add(prob);
      } else {
        if (!wrong.ContainsKey(prob)) wrong[prob] = 0;
        wrong[prob]++;
      }
    }

    Console.WriteLine($"{solvedCnt} {penalty}");
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

  map<string, int> wrong;
  set<string> solved;
  int solvedCnt = 0, penalty = 0;

  while (true) {
    string line;
    if (!getline(cin, line)) break;
    if (line == "-1") break;
    stringstream ss(line);
    int time;
    string prob, res;
    ss >> time >> prob >> res;

    if (solved.count(prob)) continue;
    if (res == "right") {
      solvedCnt++;
      penalty += time + wrong[prob] * 20;
      solved.insert(prob);
    } else {
      wrong[prob]++;
    }
  }

  cout << solvedCnt << " " << penalty << "\n";

  return 0;
}
```
