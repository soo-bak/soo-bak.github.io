---
layout: single
title: "[백준 10864] 친구 (C#, C++) - soo:bak"
date: "2025-05-02 18:39:00 +0900"
description: 학생 간의 친구 관계를 통해 각 사람의 친구 수를 계산하는 백준 10864번 친구 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10864
  - C#
  - C++
  - 알고리즘
keywords: "백준 10864, 백준 10864번, BOJ 10864, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10864번 - 친구](https://www.acmicpc.net/problem/10864)

## 설명
학생들 사이의 친구 관계가 주어졌을 때, 각 학생이 가진 친구의 수를 출력하는 문제입니다.

- 총 `N명`의 학생이 있으며, 각 학생은 `1번`부터 `N번`까지 번호가 매겨져 있습니다.
- `M개`의 친구 관계가 주어지며, **각 관계는 서로 쌍방입니다**.
  즉, `A`와 `B`가 친구라면 `B`도 `A`의 친구입니다.

<br>

## 접근법

- 크기가 `N + 1`인 정수 배열을 만들어 각 학생의 친구 수를 카운트합니다.
- 친구 관계가 주어질 때마다 두 사람의 친구 수를 각각 `1`씩 증가시킵니다.
- 마지막에 `1번` 학생부터 `N번` 학생까지 친구 수를 출력합니다.

<br>
문제의 조건에 따라 **중복 관계**나 **자기 자신과의 관계**는 주어지지 않기 때문에,

단순한 카운팅만으로 해결할 수 있습니다.

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine().Split();
    int n = int.Parse(parts[0]);
    int m = int.Parse(parts[1]);

    int[] friends = new int[n + 1];
    for (int i = 0; i < m; i++) {
      var line = Console.ReadLine().Split();
      int a = int.Parse(line[0]);
      int b = int.Parse(line[1]);

      friends[a]++;
      friends[b]++;
    }

    for (int i = 1; i <= n; i++)
      Console.WriteLine(friends[i]);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vi friends(n + 1);
  while (m--) {
    int a, b; cin >> a >> b;
    friends[a]++;
    friends[b]++;
  }

  for (int i = 1; i <= n; i++)
    cout << friends[i] << "\n";

  return 0;
}
```
