---
layout: single
title: "[백준 7513] 준살 프로그래밍 대회 (C#, C++) - soo:bak"
date: "2025-12-26 01:23:25 +0900"
description: "백준 7513번 C#, C++ 풀이 - 단어 목록과 인덱스 순서로 비밀번호를 만드는 문제"
tags:
  - 백준
  - BOJ
  - 7513
  - C#
  - C++
  - 알고리즘
keywords: "백준 7513, 백준 7513번, BOJ 7513, JunsalProgrammingContest, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7513번 - 준살 프로그래밍 대회](https://www.acmicpc.net/problem/7513)

## 설명
단어 목록과 참가자별 인덱스 순서가 주어질 때 비밀번호를 출력하는 문제입니다.

<br>

## 접근법
먼저 단어 목록을 순서대로 저장합니다.

다음으로 참가자마다 주어진 인덱스 순서에 맞춰 단어를 이어 붙입니다.

마지막으로 시나리오 번호와 비밀번호를 순서대로 출력하고, 테스트 케이스 사이에 빈 줄을 넣습니다.

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

    for (var caseNum = 1; caseNum <= t; caseNum++) {
      var m = int.Parse(parts[idx++]);
      var words = new string[m];
      for (var i = 0; i < m; i++)
        words[i] = parts[idx++];

      var n = int.Parse(parts[idx++]);
      sb.AppendLine($"Scenario #{caseNum}:");
      for (var i = 0; i < n; i++) {
        var k = int.Parse(parts[idx++]);
        var pass = new StringBuilder();
        for (var j = 0; j < k; j++) {
          var w = int.Parse(parts[idx++]);
          pass.Append(words[w]);
        }
        sb.AppendLine(pass.ToString());
      }

      if (caseNum != t) sb.AppendLine();
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  for (int caseNum = 1; caseNum <= t; caseNum++) {
    int m; cin >> m;
    vs words(m);
    for (int i = 0; i < m; i++)
      cin >> words[i];

    int n; cin >> n;
    cout << "Scenario #" << caseNum << ":\n";
    for (int i = 0; i < n; i++) {
      int k; cin >> k;
      string pass;
      for (int j = 0; j < k; j++) {
        int w; cin >> w;
        pass += words[w];
      }
      cout << pass << "\n";
    }

    if (caseNum != t) cout << "\n";
  }

  return 0;
}
```
