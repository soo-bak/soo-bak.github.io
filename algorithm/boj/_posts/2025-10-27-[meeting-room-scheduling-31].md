---
layout: single
title: "[백준 1931] 회의실 배정 (C#, C++) - soo:bak"
date: "2025-10-27 22:15:00 +0900"
description: 끝나는 시간 기준으로 정렬해 최대한 많은 회의를 배치하는 백준 1931번 회의실 배정 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1931
  - C#
  - C++
  - 알고리즘
keywords: "백준 1931, 백준 1931번, BOJ 1931, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1931번 - 회의실 배정](https://www.acmicpc.net/problem/1931)

## 설명

한 개의 회의실에서 회의가 겹치지 않도록 최대한 많은 회의를 배치하는 문제입니다.<br>

회의는 끝나는 시간이 빠른 순서대로 선택하는 것이 최선이며, 시작 시간과 끝나는 시간이 동일할 수도 있습니다.<br>

회의가 끝나는 순간 바로 다음 회의를 시작할 수 있습니다.<br>

<br>

## 접근법

그리디 알고리즘을 적용합니다.

회의를 **끝나는 시간 기준으로 오름차순 정렬**한 후, 이전 회의가 끝난 시점 이후에 시작하는 회의를 순차적으로 선택하면 최대 개수를 얻을 수 있습니다.

끝나는 시간이 같을 경우 시작 시간이 빠른 순서로 정렬하여, 회의 시간이 `0`인 경우도 정확히 처리할 수 있습니다.

<br>
시간 복잡도는 정렬에 $$O(n \log n)$$, 순회에 $$O(n)$$으로 최대 `100,000`개의 회의도 충분히 처리할 수 있습니다.

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
    var n = int.Parse(Console.ReadLine()!);
    var meetings = new List<(int start, int end)>(n);
    foreach (var _ in Enumerable.Range(0, n)) {
      var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      meetings.Add((tokens[0], tokens[1]));
    }

    meetings.Sort((a, b) => {
      if (a.end == b.end) return a.start.CompareTo(b.start);
      return a.end.CompareTo(b.end);
    });

    var count = 0;
    var currentEnd = 0;
    foreach (var (start, end) in meetings) {
      if (start < currentEnd) continue;
      currentEnd = end;
      count++;
    }

    Console.WriteLine(count);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<int, int> pii;
typedef vector<pii> vpii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vpii meetings(n);
  for (int i = 0; i < n; ++i)
    cin >> meetings[i].first >> meetings[i].second;

  sort(meetings.begin(), meetings.end(), [](const pii& a, const pii& b) {
    if (a.second == b.second) return a.first < b.first;
    return a.second < b.second;
  });

  int count = 0, currentEnd = 0;
  for (const auto& meeting : meetings) {
    if (meeting.first < currentEnd) continue;
    currentEnd = meeting.second;
    ++count;
  }

  cout << count << "\n";
  
  return 0;
}
```

