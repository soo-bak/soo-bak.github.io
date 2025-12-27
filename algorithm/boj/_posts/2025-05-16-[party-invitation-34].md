---
layout: single
title: "[백준 10104] Party Invitation (C#, C++) - soo:bak"
date: "2025-05-16 19:15:00 +0900"
description: 수학적 규칙에 따라 친구를 제거하며 남은 번호를 출력하는 백준 10104번 Party Invitation 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10104
  - C#
  - C++
  - 알고리즘
keywords: "백준 10104, 백준 10104번, BOJ 10104, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10104번 - Party Invitation](https://www.acmicpc.net/problem/10104)

## 설명

번호가 매겨진 친구들 중, **특정한 규칙에 따라 제거를 반복한 뒤 남는 번호를 출력하는 문제입니다.**

처음에는 `1`번부터 `K`번까지 모든 친구가 초대 대상이며,

이후 `m`번에 걸쳐 **특정 간격으로 친구를 제거하는 작업**을 반복합니다.

<br>
예를 들어, 어떤 라운드에서 숫자 `r`이 주어졌다면,

현재 남은 목록 중 **위치가 `r`의 배수인 친구**들을 모두 제거합니다.

<br>
입력으로 주어지는 `m`개의 숫자에 대해 차례대로 위 작업을 수행한 후,

모든 라운드가 끝난 뒤 **남아 있는 친구들의 번호**를 한 줄에 하나씩 출력해야 합니다.

<br>

## 접근법

먼저 `1`번부터 `K`번까지의 번호를 순서대로 리스트에 넣습니다.

그다음 `m`개의 라운드 정보를 입력받고, 각 라운드마다 다음 작업을 수행합니다:
- 남아 있는 리스트를 처음부터 끝까지 순회하며,
- 현재 위치가 해당 라운드의 숫자의 배수인지 확인합니다.
- 배수에 해당하면 제거하고, 그렇지 않으면 다음 요소로 넘어갑니다.

<br>
중요한 점은, **요소를 제거할 때마다 리스트가 앞으로 당겨지므로**,

반복문 안에서 인덱스를 별도로 관리하거나, 반복자 기반 순회에서 주의해야 한다는 점입니다.

<br>
모든 라운드가 끝나면, 최종적으로 남은 친구 번호들을 그대로 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    int k = int.Parse(Console.ReadLine());
    int m = int.Parse(Console.ReadLine());

    var list = new List<int>();
    for (int i = 1; i <= k; i++)
      list.Add(i);

    for (int t = 0; t < m; t++) {
      int r = int.Parse(Console.ReadLine());
      int pos = 1;
      for (int i = 0; i < list.Count; ) {
        if (pos % r == 0) list.RemoveAt(i);
        else i++;
        pos++;
      }
    }

    foreach (var val in list)
      Console.WriteLine(val);
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

  int k, m; cin >> k >> m;

  vi v;
  for (int i = 1; i <= k; ++i)
    v.push_back(i);

  while (m--) {
    int r; cin >> r;
    int i = 1;
    auto it = v.begin();
    while (it != v.end()) {
      if (i++ % r == 0) it = v.erase(it);
      else ++it;
    }
  }

  for (int x : v)
    cout << x << "\n";

  return 0;
}
```
