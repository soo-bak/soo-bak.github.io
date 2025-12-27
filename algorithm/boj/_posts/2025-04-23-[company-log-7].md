---
layout: single
title: "[백준 7785] 회사에 있는 사람 (C#, C++) - soo:bak"
date: "2025-04-23 07:01:00 +0900"
description: 사람들의 출입 기록을 기반으로 현재 회사에 남아 있는 사람들의 이름을 사전 역순으로 출력하는 백준 7785번 회사에 있는 사람 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 7785
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - set
  - hash_set
keywords: "백준 7785, 백준 7785번, BOJ 7785, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7785번 - 회사에 있는 사람](https://www.acmicpc.net/problem/7785)

## 설명
사람들의 출입 기록이 주어졌을 때, **현재 회사에 남아 있는 사람들의 이름을 사전 역순으로 출력하는 문제**입니다.<br><br>

각 기록은 이름과 함께 `"enter"` 또는 `"leave"`로 구성됩니다.<br>
- `"enter"`는 출근을 의미하고,
- `"leave"`는 퇴근을 의미합니다.

같은 사람이 여러 번 출입할 수 있으며, 최종적으로 `"enter"`만 있고 `"leave"`가 없는 사람만 출력 대상입니다.

## 접근법
- 이름을 키로 하고, 현재 회사에 있는지를 숫자로 표시하는 딕셔너리를 사용합니다.
  - `"enter"` → `+1`
  - `"leave"` → `-1`
- 최종적으로 값이 `1`인 사람만 리스트에 담고, **사전 역순**으로 정렬해 출력합니다.


## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var log = new Dictionary<string, int>();

    for (int i = 0; i < n; i++) {
      var parts = Console.ReadLine().Split();
      string name = parts[0], status = parts[1];
      if (!log.ContainsKey(name)) log[name] = 0;
      log[name] += status == "enter" ? 1 : -1;
    }

    var result = log.Where(p => p.Value == 1)
      .Select(p => p.Key)
      .OrderByDescending(x => x);

    var sb = new StringBuilder();
    foreach (var name in result)
      sb.AppendLine(name);

    Console.Write(sb.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef map<string, int> msi;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  msi log;
  while (n--) {
    string name, status; cin >> name >> status;
    log[name] += (status == "enter" ? 1 : -1);
  }

  vs ans;
  for (const auto& p : log)
    if (p.second == 1) ans.push_back(p.first);

  sort(ans.rbegin(), ans.rend());

  for (const auto& name : ans)
    cout << name << "\n";

  return 0;
}
```
