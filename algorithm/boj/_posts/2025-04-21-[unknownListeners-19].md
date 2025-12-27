---
layout: single
title: "[백준 1764] 듣보잡 (C#, C++) - soo:bak"
date: "2025-04-21 01:18:00 +0900"
description: 듣도 보도 못한 사람들의 교집합을 구해 사전 순으로 출력하는 백준 1764번 듣보잡 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1764
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 문자열
  - 정렬
  - set
  - hash_set
keywords: "백준 1764, 백준 1764번, BOJ 1764, unknownListeners, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1764번 - 듣보잡](https://www.acmicpc.net/problem/1764)

## 설명
`듣도 못한 사람들`과 `보도 못한 사람들`의 명단이 주어졌을 때, **두 조건을 모두 만족하는 사람들**의 이름을 사전 순으로 출력하는 문제입니다.<br>
<br>

- 첫 번째 줄에 듣도 못한 사람의 수 `N`과 보도 못한 사람의 수 `M`이 주어집니다.
- 이어서 `N`개의 줄에는 듣도 못한 사람의 이름이, 그 뒤 `M`개의 줄에는 보도 못한 사람의 이름이 주어집니다.
- 두 목록 모두 중복 없이 이름만으로 구성되어 있습니다.
- 두 조건을 모두 만족하는 이름을 사전 순으로 정렬하여 출력합니다.


## 접근법

- 먼저 듣지 못한 사람의 이름을 집합(`Set`)으로 저장해 빠르게 조회할 수 있도록 합니다.
- 이후 보지 못한 사람 목록을 하나씩 확인하며, `앞에서 저장한 집합에 존재하는 이름`을 결과 배열에 담습니다.
- 마지막으로 배열을 사전 순으로 정렬하여 출력합니다.
- 집합과 정렬을 활용하므로 시간 복잡도는 `O(N log N + M log M)`입니다.

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int n = tokens[0], m = tokens[1];

    var heard = new HashSet<string>();
    for (int i = 0; i < n; i++) heard.Add(Console.ReadLine());

    var result = new List<string>();
    for (int i = 0; i < m; i++) {
      var name = Console.ReadLine();
      if (heard.Contains(name)) result.Add(name);
    }

    result.Sort();

    Console.WriteLine(result.Count);
    foreach (var name in result)
      Console.WriteLine(name);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef set<string> ss;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  ss heard;
  while (n--) {
    string s; cin >> s;
    heard.insert(s);
  }

  vs ans;
  while (m--) {
    string s; cin >>  s;
    if (heard.count(s)) ans.push_back(s);
  }

  sort(ans.begin(), ans.end());

  cout << ans.size() << "\n";
  for (const auto& a : ans) cout << a << "\n";
}
```
