---
layout: single
title: "[백준 9019] DSLR (C#, C++) - soo:bak"
date: "2025-11-15 01:35:00 +0900"
description: 0~9999 레지스터를 BFS로 탐색해 최소 명령어(D,S,L,R)를 찾는 백준 9019번 DSLR 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[9019번 - DSLR](https://www.acmicpc.net/problem/9019)

## 설명

`0`부터 `9999`까지의 값을 저장하는 레지스터에 네 가지 연산을 수행할 수 있습니다.<br>

`D`는 값을 두 배로 만들고 `10000`으로 나눈 나머지를 저장합니다. `S`는 `1`을 빼며 `0`이면 `9999`가 됩니다. `L`과 `R`은 각 자릿수를 왼쪽 또는 오른쪽으로 회전시킵니다.<br>

초기값 `A`에서 목표값 `B`로 변환하는 최소 명령어 수열을 구하는 문제입니다.<br>

<br>

## 접근법

너비 우선 탐색(BFS)을 사용하여 최단 명령어 수열을 찾습니다.

모든 연산의 비용이 동일하므로 BFS로 탐색하면 처음 목표값에 도달한 경로가 최단 경로가 됩니다.

<br>
큐에 현재 레지스터 값과 지금까지 수행한 명령어 문자열을 함께 저장합니다. 이미 탐색한 값은 중복 방문하지 않도록 체크합니다.

<br>
초기값을 큐에 넣고 BFS를 시작합니다. 큐에서 값을 꺼낼 때마다 네 가지 연산 `D`, `S`, `L`, `R`을 각각 적용하여 다음 상태를 계산합니다.

<br>
각 연산 결과가 아직 방문하지 않은 값이면 방문 처리하고 해당 명령어를 추가한 문자열과 함께 큐에 넣습니다. 목표값에 도달하면 그때까지의 명령어 문자열을 반환합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static string BFS(int start, int target) {
      var visited = new bool[10000];
      var queue = new Queue<(int value, string cmd)>();
      queue.Enqueue((start, string.Empty));
      visited[start] = true;

      while (queue.Count > 0) {
        var (value, cmd) = queue.Dequeue();
        if (value == target) return cmd;

        var d = (value * 2) % 10000;
        if (!visited[d]) {
          visited[d] = true;
          queue.Enqueue((d, cmd + "D"));
        }

        var s = value == 0 ? 9999 : value - 1;
        if (!visited[s]) {
          visited[s] = true;
          queue.Enqueue((s, cmd + "S"));
        }

        var l = (value % 1000) * 10 + value / 1000;
        if (!visited[l]) {
          visited[l] = true;
          queue.Enqueue((l, cmd + "L"));
        }

        var r = (value % 10) * 1000 + value / 10;
        if (!visited[r]) {
          visited[r] = true;
          queue.Enqueue((r, cmd + "R"));
        }
      }

      return string.Empty;
    }

    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var answers = new string[t];

      for (var i = 0; i < t; i++) {
        var tokens = Console.ReadLine()!.Split();
        var a = int.Parse(tokens[0]);
        var b = int.Parse(tokens[1]);
        answers[i] = BFS(a, b);
      }

      Console.WriteLine(string.Join("\n", answers));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string bfs(int start, int target) {
  vector<bool> visited(10000, false);
  queue<pair<int, string>> q;
  q.push({start, string()});
  visited[start] = true;

  while (!q.empty()) {
    auto [value, cmd] = q.front();
    q.pop();
    if (value == target) return cmd;

    int d = (value * 2) % 10000;
    if (!visited[d]) {
      visited[d] = true;
      q.push({d, cmd + 'D'});
    }

    int s = value == 0 ? 9999 : value - 1;
    if (!visited[s]) {
      visited[s] = true;
      q.push({s, cmd + 'S'});
    }

    int l = (value % 1000) * 10 + value / 1000;
    if (!visited[l]) {
      visited[l] = true;
      q.push({l, cmd + 'L'});
    }

    int r = (value % 10) * 1000 + value / 10;
    if (!visited[r]) {
      visited[r] = true;
      q.push({r, cmd + 'R'});
    }
  }

  return "";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int a, b; cin >> a >> b;
    cout << bfs(a, b) << "\n";
  }

  return 0;
}
```
