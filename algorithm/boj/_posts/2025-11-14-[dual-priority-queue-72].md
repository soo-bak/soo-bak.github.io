---
layout: single
title: "[백준 7662] 이중 우선순위 큐 (C#, C++) - soo:bak"
date: "2025-11-14 23:20:00 +0900"
description: 두 개의 우선순위 큐와 lazy deletion으로 최댓값·최솟값 삭제를 동시에 지원하는 백준 7662번 이중 우선순위 큐 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 7662
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - set
  - tree_set
  - 우선순위큐
keywords: "백준 7662, 백준 7662번, BOJ 7662, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7662번 - 이중 우선순위 큐](https://www.acmicpc.net/problem/7662)

## 설명

삽입 연산 `I`와 최댓값 또는 최솟값을 삭제하는 `D` 연산을 처리하는 이중 우선순위 큐 문제입니다.<br>

`I n`은 정수 `n`을 삽입하고, `D 1`은 최댓값을, `D -1`은 최솟값을 삭제합니다.

큐가 비어 있을 때 삭제 명령이 들어오면 무시하며, 모든 연산이 끝난 뒤 큐에 남아 있는 최댓값과 최솟값을 출력합니다.

큐가 비어 있다면 `EMPTY`를 출력합니다.<br>

<br>

## 접근법

최소 힙과 최대 힙 두 개를 동시에 유지하여 최솟값과 최댓값을 효율적으로 관리합니다.

각 원소를 삽입할 때 고유한 인덱스를 부여하여 `(값, 인덱스)` 쌍으로 두 힙에 모두 저장합니다.

삭제 연산은 즉시 힙에서 제거하지 않고, `deleted` 배열에 삭제 여부만 표시하는 지연 삭제(lazy deletion) 방식을 사용합니다.

<br>
최솟값을 삭제하는 `D -1` 연산에서는 최소 힙의 top을 확인합니다.

만약 이미 삭제된 원소라면 pop으로 제거하고 다음 원소를 확인하는 과정을 반복합니다.

유효한 원소를 찾으면 해당 인덱스를 `deleted` 배열에 표시합니다.

최댓값을 삭제하는 `D 1` 연산도 동일한 방식으로 최대 힙을 사용합니다.

<br>
모든 연산이 끝난 후, 두 힙에서 삭제된 원소들을 정리한 뒤 남아 있는 원소가 있는지 확인합니다.

두 힙 모두 비어 있지 않다면 최대 힙의 top이 최댓값, 최소 힙의 top이 최솟값입니다.

<br>
연산 수가 최대 `1,000,000`개이므로, 힙의 `O(log n)` 연산으로 효율적으로 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var results = new List<string>();

      while (t-- > 0) {
        var k = int.Parse(Console.ReadLine()!);
        var deleted = new bool[k];
        var minQ = new PriorityQueue<(long value, int idx), long>();
        var maxQ = new PriorityQueue<(long value, int idx), long>();

        for (var i = 0; i < k; i++) {
          var input = Console.ReadLine()!.Split();
          var cmd = input[0];
          var num = long.Parse(input[1]);

          if (cmd == "I") {
            minQ.Enqueue((num, i), num);
            maxQ.Enqueue((num, i), -num);
          } else {
            if (num == -1) {
              Clean(minQ, deleted);
              if (minQ.Count > 0) {
                var top = minQ.Dequeue();
                deleted[top.idx] = true;
              }
            } else {
              Clean(maxQ, deleted);
              if (maxQ.Count > 0) {
                var top = maxQ.Dequeue();
                deleted[top.idx] = true;
              }
            }
          }
        }

        Clean(minQ, deleted);
        Clean(maxQ, deleted);

        if (minQ.Count == 0 || maxQ.Count == 0) results.Add("EMPTY");
        else {
          var maxVal = maxQ.Peek().value;
          var minVal = minQ.Peek().value;
          results.Add($"{maxVal} {minVal}");
        }
      }

      Console.WriteLine(string.Join("\n", results));
    }

    static void Clean(PriorityQueue<(long value, int idx), long> pq, bool[] deleted) {
      while (pq.Count > 0 && deleted[pq.Peek().idx])
        pq.Dequeue();
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<long long, int> pli;
typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int k; cin >> k;
    priority_queue<pli, vector<pli>, greater<pli>> minQ;
    priority_queue<pli> maxQ;
    vb deleted(k, false);

    for (int i = 0; i < k; ++i) {
      char cmd; long long num;
      cin >> cmd >> num;
      if (cmd == 'I') {
        minQ.emplace(num, i);
        maxQ.emplace(num, i);
      } else if (num == -1) {
        while (!minQ.empty() && deleted[minQ.top().second]) minQ.pop();
        if (!minQ.empty()) {
          deleted[minQ.top().second] = true;
          minQ.pop();
        }
      } else {
        while (!maxQ.empty() && deleted[maxQ.top().second]) maxQ.pop();
        if (!maxQ.empty()) {
          deleted[maxQ.top().second] = true;
          maxQ.pop();
        }
      }
    }

    while (!minQ.empty() && deleted[minQ.top().second]) minQ.pop();
    while (!maxQ.empty() && deleted[maxQ.top().second]) maxQ.pop();

    if (minQ.empty() || maxQ.empty()) cout << "EMPTY\n";
    else cout << maxQ.top().first << ' ' << minQ.top().first << "\n";
  }

  return 0;
}
```

