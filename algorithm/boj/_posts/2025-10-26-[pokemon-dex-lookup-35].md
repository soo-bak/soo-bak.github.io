---
layout: single
title: "[백준 1620] 나는야 포켓몬 마스터 이다솜 (C#, C++) - soo:bak"
date: "2025-10-26 00:20:00 +0900"
description: 포켓몬 이름과 번호를 서로 조회할 수 있는 맵을 구성해 질의에 답하는 백준 1620번 나는야 포켓몬 마스터 이다솜 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1620
  - C#
  - C++
  - 알고리즘
keywords: "백준 1620, 백준 1620번, BOJ 1620, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1620번 - 나는야 포켓몬 마스터 이다솜](https://www.acmicpc.net/problem/1620)

## 설명

포켓몬 도감에는 `N`마리의 포켓몬이 1번부터 `N`번까지 등록되어 있습니다.<br>

이름이 주어지면 번호를, 번호가 주어지면 이름을 빠르게 찾아야 합니다.<br>

포켓몬 이름은 영어 대소문자로 구성되며, 질의는 총 `M`개가 주어집니다.<br>

<br>

## 접근법

이름과 번호를 모두 즉시 찾으려면 **두 방향을 따로 준비**해두는 편이 빠릅니다.

- 이름 → 번호: 해시 맵에 이름을 키로 넣습니다.
- 번호 → 이름: 1번부터 `N`번까지 인덱스를 그대로 쓰는 배열에 이름을 담습니다.
- 질의를 읽을 때 숫자로 시작하면 번호, 그렇지 않으면 이름을 사용해 바로 찾아냅니다.

<br>
입력 크기가 최대 `100,000`이므로, 해시 맵과 배열만으로도 충분히 빠르게 응답할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    var n = tokens[0];
    var m = tokens[1];

    var nameToIdx = new Dictionary<string, int>(n);
    var indexToName = new string[n + 1];

    foreach (var idx in Enumerable.Range(1, n)) {
      var name = Console.ReadLine()!;
      nameToIdx[name] = idx;
      indexToName[idx] = name;
    }

    var output = new System.Text.StringBuilder();
    foreach (var _ in Enumerable.Range(0, m)) {
      var query = Console.ReadLine()!;
      if (char.IsDigit(query[0])) {
        var idx = int.Parse(query);
        output.AppendLine(indexToName[idx]);
      } else
        output.AppendLine(nameToIdx[query].ToString());
    }

    Console.Write(output.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef unordered_map<string, int> msi;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  msi nameToIdx;
  nameToIdx.reserve(n * 2);
  vs indexToName(n + 1);

  for (int i = 1; i <= n; ++i) {
    string name; cin >> name;
    nameToIdx[name] = i;
    indexToName[i] = name;
  }

  while (m--) {
    string query; cin >> query;
    if (isdigit(query[0])) {
      int idx = stoi(query);
      cout << indexToName[idx] << "\n";
    } else
      cout << nameToIdx[query] << "\n";
  }

  return 0;
}
```
