---
layout: single
title: "[백준 1021] 회전하는 큐 (C#, C++) - soo:bak"
date: "2025-12-07 03:20:00 +0900"
description: 덱에서 목표 원소를 꺼낼 때 좌우 회전 횟수 중 작은 쪽을 선택하는 백준 1021번 회전하는 큐 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1021번 - 회전하는 큐](https://www.acmicpc.net/problem/1021)

## 설명
양방향 순환 큐에서 주어진 순서대로 원소를 뽑을 때, 왼쪽 또는 오른쪽 회전의 최소 총 횟수를 구하는 문제입니다.

<br>

## 접근법
덱을 사용하여 양방향 순환 큐를 구현합니다. 먼저 1부터 N까지의 원소를 순서대로 덱에 넣습니다.

각 목표 원소에 대해 현재 덱에서의 위치를 찾습니다. 왼쪽으로 회전하면 해당 위치만큼, 오른쪽으로 회전하면 전체 크기에서 위치를 뺀 만큼 회전이 필요합니다. 두 값 중 작은 쪽을 선택하여 회전시키고 횟수를 누적합니다.

회전을 마치면 목표 원소가 맨 앞에 오게 되므로 이를 꺼내고 다음 목표로 진행합니다.

<br>

- - -

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var m = int.Parse(first[1]);

    var dq = new LinkedList<int>();
    for (var i = 1; i <= n; i++) dq.AddLast(i);

    var ops = 0;
    var targets = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    foreach (var target in targets) {
      var idx = 0;
      var node = dq.First;
      while (node != null && node.Value != target) { idx++; node = node.Next; }
      var left = idx;
      var right = dq.Count - idx;
      if (left <= right) {
        for (var i = 0; i < left; i++) {
          var val = dq.First!.Value;
          dq.RemoveFirst();
          dq.AddLast(val);
          ops++;
        }
      } else {
        for (var i = 0; i < right; i++) {
          var val = dq.Last!.Value;
          dq.RemoveLast();
          dq.AddFirst(val);
          ops++;
        }
      }
      dq.RemoveFirst();
    }

    Console.WriteLine(ops);
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

  int n, m; cin >> n >> m;
  deque<int> dq;
  for (int i = 1; i <= n; i++)
    dq.push_back(i);

  int ops = 0;
  for (int k = 0; k < m; k++) {
    int target; cin >> target;
    int idx = 0;
    for (; idx < (int)dq.size(); idx++) if (dq[idx] == target) break;
    int left = idx;
    int right = dq.size() - idx;
    if (left <= right) {
      for (int i = 0; i < left; i++) {
        dq.push_back(dq.front());
        dq.pop_front();
        ops++;
      }
    } else {
      for (int i = 0; i < right; i++) {
        dq.push_front(dq.back());
        dq.pop_back();
        ops++;
      }
    }
    dq.pop_front();
  }

  cout << ops << "\n";

  return 0;
}
```
