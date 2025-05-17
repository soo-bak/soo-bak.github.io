---
layout: single
title: "[백준 10865] 친구 친구 (C#, C++) - soo:bak"
date: "2025-05-18 00:29:00 +0900"
description: 각 학생의 친구 수를 인접 리스트로 계산하여 출력하는 백준 10865번 친구 친구 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크

[10865번 - 친구 친구](https://www.acmicpc.net/problem/10865)

## 설명

**학생들의 친구 관계가 주어졌을 때, 각 학생이 몇 명의 친구를 갖고 있는지 출력하는 문제입니다.**

* 총 `N`명의 학생이 있으며, 학생 번호는 `1`번부터 `N`번까지 부여되어 있습니다.
* `M`개의 친구 관계가 주어지며, 각각 두 학생 `A`, `B`가 친구임을 의미합니다.
* 입력에 같은 쌍이 반복되지 않으며, 자기 자신과 친구인 경우는 없습니다.

각 학생마다 친구 수를 출력하되, **학생 번호 순서대로 한 줄에 하나씩** 출력해야 합니다.

<br>

## 접근법

친구 관계는 **무방향 그래프**의 간선으로 볼 수 있으며,

각 학생의 친구 수는 해당 정점의 연결된 간선 수, 즉 **차수(degree)**와 같습니다.

<br>
따라서, 각 학생마다 **연결된 친구를 저장하는 리스트(인접 리스트)**를 만들고,

친구 관계를 읽을 때마다 양쪽 학생의 리스트에 서로를 추가합니다:
* 학생 수 `N`만큼 리스트를 초기화
* 친구 관계가 주어질 때마다 두 학생의 리스트에 서로를 등록
* 모든 입력이 끝난 뒤, 각 학생의 리스트 길이를 출력

<br>

---

## Code

### C\#

```csharp
using System;
using System.Collections.Generic;
using System.Text;

class Program {
  static void Main() {
    var tokens = Console.ReadLine().Split();
    int n = int.Parse(tokens[0]);
    int m = int.Parse(tokens[1]);

    var friends = new List<int>[n + 1];
    for (int i = 1; i <= n; i++)
      friends[i] = new List<int>();

    for (int i = 0; i < m; i++) {
      var pair = Console.ReadLine().Split();
      int a = int.Parse(pair[0]);
      int b = int.Parse(pair[1]);
      friends[a].Add(b);
      friends[b].Add(a);
    }

    var sb = new StringBuilder();
    for (int i = 1; i <= n; i++)
      sb.AppendLine(friends[i].Count.ToString());

    Console.Write(sb.ToString());
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvi adj(n + 1);

  int m; cin >> m;
  while (m--) {
    int u, v; cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }

  for (int i = 1; i <= n; ++i)
    cout << adj[i].size() << "\n";

  return 0;
}
```
