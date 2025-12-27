---
layout: single
title: "[백준 1007] 벡터 매칭 (C#, C++) - soo:bak"
date: "2025-12-08 02:40:00 +0900"
description: 절반을 +, 절반을 -로 선택해 벡터 합의 길이를 최소화하는 백준 1007번 벡터 매칭 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1007
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 1007, 백준 1007번, BOJ 1007, VectorMatching, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1007번 - 벡터 매칭](https://www.acmicpc.net/problem/1007)

## 설명
짝수 개의 점이 주어질 때, 절반은 시작점으로, 나머지 절반은 끝점으로 짝지어 벡터를 만들고, 이 벡터들의 합의 길이를 최소화하는 문제입니다.

<br>

## 접근법
어떤 점 집합을 시작점으로 선택하면 나머지는 자동으로 끝점이 됩니다. 벡터의 합은 끝점들의 좌표 합에서 시작점들의 좌표 합을 뺀 것입니다. 시작점으로 선택한 점들의 합을 전체 합에서 빼면 끝점들의 합이 되므로, 결국 벡터 합은 전체 합에서 시작점 합의 두 배를 뺀 것과 같습니다.

따라서 절반의 점을 선택하는 모든 경우를 확인하면서 벡터 합의 길이가 최소가 되는 경우를 찾으면 됩니다. 점의 개수가 최대 20개이므로 20개 중 10개를 고르는 조합의 수는 약 18만 개입니다. 깊이 우선 탐색으로 모든 조합을 순회하되, 남은 점으로 필요한 개수를 채울 수 없으면 더 이상 진행하지 않고 되돌아갑니다.

최소 길이 제곱을 구한 뒤 제곱근을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Globalization;

class Program {
  static int n, half;
  static long totalX, totalY;
  static int[] xs = new int[20], ys = new int[20];
  static double best;

  static void Dfs(int idx, int cnt, long sx, long sy) {
    if (cnt == half) {
      var vx = 2 * sx - totalX;
      var vy = 2 * sy - totalY;
      var len2 = (double)vx * vx + (double)vy * vy;
      if (len2 < best) best = len2;
      return;
    }
    if (idx == n) return;
    var remain = n - idx;
    if (cnt + remain < half) return;

    Dfs(idx + 1, cnt + 1, sx + xs[idx], sy + ys[idx]);
    Dfs(idx + 1, cnt, sx, sy);
  }

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      n = int.Parse(Console.ReadLine()!);
      half = n / 2;
      totalX = totalY = 0;
      for (var j = 0; j < n; j++) {
        var parts = Console.ReadLine()!.Split();
        xs[j] = int.Parse(parts[0]);
        ys[j] = int.Parse(parts[1]);
        totalX += xs[j];
        totalY += ys[j];
      }
      best = double.MaxValue;
      Dfs(0, 0, 0, 0);
      Console.WriteLine(Math.Sqrt(best).ToString("F12", CultureInfo.InvariantCulture));
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

int n, halfN;
ll totalX, totalY;
vi xs, ys;
long double best;

void dfs(int idx, int cnt, ll sx, ll sy) {
  if (cnt == halfN) {
    ll vx = 2 * sx - totalX;
    ll vy = 2 * sy - totalY;
    long double len2 = (long double)vx * vx + (long double)vy * vy;
    if (len2 < best) best = len2;
    return;
  }
  if (idx == n) return;
  int remain = n - idx;
  if (cnt + remain < halfN) return;

  dfs(idx + 1, cnt + 1, sx + xs[idx], sy + ys[idx]);
  dfs(idx + 1, cnt, sx, sy);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  cout.setf(ios::fixed);
  cout << setprecision(12);
  while (t--) {
    cin >> n;
    halfN = n / 2;
    xs.assign(n, 0);
    ys.assign(n, 0);
    totalX = totalY = 0;
    for (int i = 0; i < n; i++) {
      cin >> xs[i] >> ys[i];
      totalX += xs[i];
      totalY += ys[i];
    }
    best = numeric_limits<long double>::max();
    dfs(0, 0, 0, 0);
    cout << sqrt(best) << "\n";
  }

  return 0;
}
```
