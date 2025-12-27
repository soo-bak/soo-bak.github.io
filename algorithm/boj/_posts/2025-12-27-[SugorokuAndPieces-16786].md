---
layout: single
title: "[백준 16786] すごろくと駒 (Sugoroku and Pieces) (C#, C++) - soo:bak"
date: "2025-12-27 05:25:00 +0900"
description: "백준 16786번 C#, C++ 풀이 - 한 칸씩 전진하는 규칙으로 말을 이동시키는 시뮬레이션 문제"
tags:
  - 백준
  - BOJ
  - 16786
  - C#
  - C++
  - 알고리즘
keywords: "백준 16786, 백준 16786번, BOJ 16786, SugorokuAndPieces, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16786번 - すごろくと駒 (Sugoroku and Pieces)](https://www.acmicpc.net/problem/16786)

## 설명
1~2019번 칸에 N개의 말이 오름차순으로 놓여 있고, M번의 명령으로 지정된 말을 한 칸 앞으로 이동시킵니다.

말이 골에 있거나, 앞칸에 다른 말이 있으면 이동하지 않습니다.

모든 명령 후 각 말의 위치를 구하는 문제입니다.

<br>

## 접근법
말의 위치와 각 칸의 점유 여부를 관리합니다. 명령마다 해당 말이 골에 있지 않고 앞칸이 비어 있으면 한 칸 이동시키고 점유 상태를 갱신합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var pos = new int[n];
    var occ = new bool[2020];
    for (var i = 0; i < n; i++) {
      pos[i] = int.Parse(parts[idx++]);
      occ[pos[i]] = true;
    }

    var m = int.Parse(parts[idx++]);
    for (var i = 0; i < m; i++) {
      var a = int.Parse(parts[idx++]) - 1;
      var cur = pos[a];
      if (cur < 2019 && !occ[cur + 1]) {
        occ[cur] = false;
        occ[cur + 1] = true;
        pos[a] = cur + 1;
      }
    }

    for (var i = 0; i < n; i++)
      Console.WriteLine(pos[i]);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vi pos(n);
  vb occ(2020, false);
  for (int i = 0; i < n; i++) {
    cin >> pos[i];
    occ[pos[i]] = true;
  }

  int m; cin >> m;
  for (int i = 0; i < m; i++) {
    int a; cin >> a; a--;
    int cur = pos[a];
    if (cur < 2019 && !occ[cur + 1]) {
      occ[cur] = false;
      occ[cur + 1] = true;
      pos[a] = cur + 1;
    }
  }

  for (int v : pos)
    cout << v << "\n";

  return 0;
}
```
