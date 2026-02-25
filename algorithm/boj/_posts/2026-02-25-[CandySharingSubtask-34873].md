---
layout: single
title: "[백준 34873] 사탕 나눠주기 서브태스크 (C#, C++) - soo:bak"
date: "2026-02-25 20:33:00 +0900"
description: "백준 34873번 C#, C++ 풀이 - 두 사람이 모두 중복 없는 N개 사탕을 갖도록 나눌 수 있는지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 34873
  - C#
  - C++
  - 알고리즘
  - 구현
  - 카운팅
keywords: "백준 34873, 백준 34873번, BOJ 34873, 사탕 나눠주기 서브태스크, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[34873번 - 사탕 나눠주기 서브태스크](https://www.acmicpc.net/problem/34873)

## 설명
총 2N개의 사탕을 나누어 나와 친구가 각각 N개씩 가지되, 두 사람 모두 같은 맛을 두 개 이상 갖지 않도록 나눌 수 있는지 판단하는 문제입니다.

<br>

## 접근법
한 맛이 3개 이상 있으면 두 사람이 각각 최대 1개씩만 가질 수 있으므로 반드시 남는 사탕이 생겨 불가능합니다.  
반대로 모든 맛의 개수가 2개 이하라면, 2개인 맛은 한 개씩 나눠 갖고 1개인 맛은 필요한 쪽에 배치하면 항상 정확히 N개씩 맞출 수 있습니다.  
따라서 각 맛의 개수를 세어 최대 빈도가 2를 넘는지만 확인하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine()!);
    var p = Console.ReadLine()!.Split();

    int[] cnt = new int[2 * n + 1];
    bool ok = true;

    for (int i = 0; i < 2 * n; i++) {
      int x = int.Parse(p[i]);
      cnt[x]++;
      if (cnt[x] > 2)
        ok = false;
    }

    Console.WriteLine(ok ? "Yes" : "No");
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
  vector<int> cnt(2 * n + 1, 0);
  bool ok = true;

  for (int i = 0; i < 2 * n; i++) {
    int x; cin >> x;
    cnt[x]++;
    if (cnt[x] > 2)
      ok = false;
  }

  cout << (ok ? "Yes" : "No") << "\n";

  return 0;
}
```
