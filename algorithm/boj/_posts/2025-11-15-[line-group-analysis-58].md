---
layout: single
title: "[백준 2162] 선분 그룹 (C#, C++) - soo:bak"
date: "2025-11-15 01:45:00 +0900"
description: 모든 선분 쌍의 교차 여부를 판별해 그래프를 만든 뒤 DFS로 그룹 수와 최댓값을 구하는 백준 2162번 선분 그룹 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2162
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 기하학
  - disjoint_set
  - line_intersection
keywords: "백준 2162, 백준 2162번, BOJ 2162, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2162번 - 선분 그룹](https://www.acmicpc.net/problem/2162)

## 설명

`N`개의 선분이 주어질 때, 서로 교차하는 선분들을 하나의 그룹으로 묶는 문제입니다.<br>

두 선분이 교차한다는 것은 한 점에서 만나거나 일부가 겹치는 경우를 모두 포함합니다. 끝점끼리 스치듯 만나는 경우도 교차로 간주합니다.<br>

또한 직접 교차하지 않더라도 간접적으로 연결된 경우도 같은 그룹입니다. 예를 들어 선분 A가 B와 교차하고 B가 C와 교차하면 A, B, C는 모두 같은 그룹에 속합니다.<br>

총 몇 개의 그룹이 존재하는지와 가장 큰 그룹에 속한 선분의 개수를 구하는 문제입니다.<br>

`N`은 최대 `3,000`까지 주어지며, 좌표는 `-5,000` 이상 `5,000` 이하의 정수입니다.<br>

<br>

## 접근법

CCW를 이용한 선분 교차 판정과 그래프 탐색을 결합하여 해결합니다.

먼저 모든 선분 쌍에 대해 교차 여부를 판정합니다. CCW 알고리즘으로 두 선분의 위치 관계를 계산하고, 일직선상에 있는 경우는 구간의 겹침을 확인합니다.

<br>
교차하는 선분들을 간선으로 연결하여 그래프를 구성합니다. 각 선분을 정점으로 보고, 교차하는 선분 사이에 간선을 만듭니다.

<br>
DFS나 BFS로 연결 요소를 찾습니다. 방문하지 않은 정점에서 탐색을 시작할 때마다 새로운 그룹을 발견한 것이고, 탐색 중 방문한 정점의 개수가 해당 그룹의 크기입니다.

<br>
모든 정점을 탐색하면서 그룹 개수를 세고, 각 그룹의 크기 중 최댓값을 기록합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    struct Point {
      public long X, Y;
      public Point(long x, long y) { X = x; Y = y; }
    }

    static long CCW(Point a, Point b, Point c) {
      return (b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X);
    }

    static bool Overlap(ref Point a, ref Point b, ref Point c, ref Point d) {
      if (ComparePoint(b, a) < 0) (a, b) = (b, a);
      if (ComparePoint(d, c) < 0) (c, d) = (d, c);
      return ComparePoint(c, b) <= 0 && ComparePoint(a, d) <= 0;
    }

    static int ComparePoint(Point p1, Point p2) {
      if (p1.X != p2.X) return p1.X.CompareTo(p2.X);
      return p1.Y.CompareTo(p2.Y);
    }

    static bool IsIntersect(Point a, Point b, Point c, Point d) {
      var abC = CCW(a, b, c);
      var abD = CCW(a, b, d);
      var cdA = CCW(c, d, a);
      var cdB = CCW(c, d, b);

      if (abC == 0 && abD == 0)
        return Overlap(ref a, ref b, ref c, ref d);

      return (abC * abD <= 0) && (cdA * cdB <= 0);
    }

    static int DFS(int start, List<int>[] graph, bool[] visited) {
      var stack = new Stack<int>();
      stack.Push(start);
      visited[start] = true;
      var count = 0;

      while (stack.Count > 0) {
        var cur = stack.Pop();
        count++;
        foreach (var next in graph[cur]) {
          if (visited[next]) continue;
          visited[next] = true;
          stack.Push(next);
        }
      }

      return count;
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var lines = new Point[n][];

      for (var i = 0; i < n; i++) {
        var tokens = Console.ReadLine()!.Split();
        var p1 = new Point(long.Parse(tokens[0]), long.Parse(tokens[1]));
        var p2 = new Point(long.Parse(tokens[2]), long.Parse(tokens[3]));
        lines[i] = new[] { p1, p2 };
      }

      var graph = new List<int>[n];
      for (var i = 0; i < n; i++)
        graph[i] = new List<int>();

      for (var i = 0; i < n - 1; i++) {
        for (var j = i + 1; j < n; j++) {
          if (IsIntersect(lines[i][0], lines[i][1], lines[j][0], lines[j][1])) {
            graph[i].Add(j);
            graph[j].Add(i);
          }
        }
      }

      var visited = new bool[n];
      var groupCount = 0;
      var maxSize = 0;

      for (var i = 0; i < n; i++) {
        if (visited[i]) continue;
        var size = DFS(i, graph, visited);
        groupCount++;
        if (size > maxSize) maxSize = size;
      }

      Console.WriteLine(groupCount);
      Console.WriteLine(maxSize);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef vector<int> vi;
typedef vector<vi> vvi;
typedef vector<bool> vb;

struct Point {
  ll x, y;
};

ll ccw(const Point& a, const Point& b, const Point& c) {
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

int compare(const Point& p1, const Point& p2) {
  if (p1.x != p2.x) return p1.x < p2.x ? -1 : 1;
  if (p1.y != p2.y) return p1.y < p2.y ? -1 : 1;
  return 0;
}

bool overlap(Point a, Point b, Point c, Point d) {
  if (compare(b, a) < 0) swap(a, b);
  if (compare(d, c) < 0) swap(c, d);
  return compare(c, b) <= 0 && compare(a, d) <= 0;
}

bool isIntersect(Point a, Point b, Point c, Point d) {
  ll abC = ccw(a, b, c);
  ll abD = ccw(a, b, d);
  ll cdA = ccw(c, d, a);
  ll cdB = ccw(c, d, b);

  if (abC == 0 && abD == 0)
    return overlap(a, b, c, d);

  return (abC * abD <= 0) && (cdA * cdB <= 0);
}

int dfs(int start, const vvi& graph, vb& visited) {
  stack<int> st;
  st.push(start);
  visited[start] = true;
  int size = 0;

  while (!st.empty()) {
    int cur = st.top(); st.pop();
    ++size;
    for (int nxt : graph[cur]) {
      if (visited[nxt]) continue;
      visited[nxt] = true;
      st.push(nxt);
    }
  }

  return size;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<pair<Point, Point>> lines(n);
  for (int i = 0; i < n; ++i)
    cin >> lines[i].first.x >> lines[i].first.y >> lines[i].second.x >> lines[i].second.y;

  vvi graph(n);
  for (int i = 0; i < n - 1; ++i) {
    for (int j = i + 1; j < n; ++j) {
      if (isIntersect(lines[i].first, lines[i].second, lines[j].first, lines[j].second)) {
        graph[i].push_back(j);
        graph[j].push_back(i);
      }
    }
  }

  vb visited(n, false);
  int groupCount = 0, maxSize = 0;

  for (int i = 0; i < n; ++i) {
    if (visited[i]) continue;
    int size = dfs(i, graph, visited);
    ++groupCount;
    maxSize = max(maxSize, size);
  }

  cout << groupCount << "\n" << maxSize << "\n";

  return 0;
}
```

