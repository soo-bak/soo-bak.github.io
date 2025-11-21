---
layout: single
title: "[백준 11403] 경로 찾기 (C#, C++) - soo:bak"
date: "2025-11-21 23:32:00 +0900"
description: 플로이드-워셜 방식으로 모든 정점 쌍의 도달 가능성을 구하는 백준 11403번 경로 찾기 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[11403번 - 경로 찾기](https://www.acmicpc.net/problem/11403)

## 설명

`N`개의 정점으로 이루어진 방향 그래프의 인접 행렬이 주어집니다.<br>

각 정점 쌍 `(i, j)`에 대해 `i`에서 `j`로 가는 경로가 존재하는지 판별해야 합니다.

경로는 길이가 양수여야 하므로 직접 연결된 간선이나, 다른 정점을 거쳐서 도달하는 경우를 모두 포함합니다.<br>

결과는 `N × N` 행렬로 출력하며, 경로가 있으면 `1`, 없으면 `0`입니다.<br>

<br>

## 접근법

플로이드-워셜 알고리즘을 사용하여 모든 정점 쌍의 도달 가능성을 구합니다.

각 정점 `k`를 경유지로 삼아, `i`에서 `k`로 가는 경로와 `k`에서 `j`로 가는 경로가 모두 존재하면 `i`에서 `j`로도 갈 수 있다고 판단합니다.<br>

모든 정점을 차례로 경유지로 고려하며, 경유를 통해 새로운 경로가 발견되면 해당 경로를 표시합니다.

입력받은 인접 행렬을 갱신하여 최종적으로 모든 도달 가능성을 기록합니다.<br>

모든 경유 가능성을 확인한 후 결과 행렬을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var graph = new int[n, n];

      for (var i = 0; i < n; i++) {
        var row = Console.ReadLine()!.Split();
        for (var j = 0; j < n; j++)
          graph[i, j] = int.Parse(row[j]);
      }

      for (var k = 0; k < n; k++)
        for (var i = 0; i < n; i++)
          for (var j = 0; j < n; j++)
            if (graph[i, k] == 1 && graph[k, j] == 1)
              graph[i, j] = 1;

      for (var i = 0; i < n; i++) {
        for (var j = 0; j < n; j++) {
          Console.Write(graph[i, j]);
          if (j != n - 1) Console.Write(" ");
        }
        Console.WriteLine();
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<vector<int>> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvi graph(n, vector<int>(n));

  for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j)
      cin >> graph[i][j];

  for (int k = 0; k < n; ++k)
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < n; ++j)
        if (graph[i][k] && graph[k][j])
          graph[i][j] = 1;

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      cout << graph[i][j];
      if (j != n - 1) cout << ' ';
    }
    cout << '\n';
  }

  return 0;
}
```

