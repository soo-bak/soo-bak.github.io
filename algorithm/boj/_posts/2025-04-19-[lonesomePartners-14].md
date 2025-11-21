---
layout: single
title: "[백준 6013] Lonesome Partners (C#, C++) - soo:bak"
date: "2025-04-19 00:17:10 +0900"
description: 2차원 평면 위 N개의 점 중 가장 거리가 먼 두 점의 번호를 찾는 백준 6013번 Lonesome Partners 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[6013번 - Lonesome Partners](https://www.acmicpc.net/problem/6013)

## 설명
**2차원 평면 상에 존재하는 여러 점들 중에서 가장 거리가 먼 두 점의 번호를 구하는 문제**입니다.<br>
<br>

- `N`개의 점이 주어지고, 각 점의 좌표는 정수입니다.<br>
- 두 점 사이의 거리 중 가장 큰 값을 가지는 쌍을 찾아 **해당 점들의 번호(1-based index)**를 출력해야 합니다.<br>
- 유클리드 거리의 제곱을 비교하여 계산할 수 있으며, 제곱근 없이 정수 비교만으로도 충분합니다.<br>

### 접근법
- 모든 점 쌍을 이중 반복문으로 순회하며 두 점 사이의 거리의 제곱을 계산합니다.<br>
- 가장 큰 거리 값을 갱신할 때마다 해당 점들의 인덱스를 저장합니다.<br>
- 입력 시 인덱스는 `1`부터 시작함에 유의합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var points = new (int x, int y)[n];

    for (int i = 0; i < n; i++) {
      var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
      points[i] = (input[0], input[1]);
    }

    int maxDist = -1, a = 0, b = 0;
    for (int i = 0; i < n; i++) {
      for (int j = i + 1; j < n; j++) {
        int dx = points[i].x - points[j].x;
        int dy = points[i].y - points[j].y;
        int dist = dx * dx + dy * dy;

        if (dist > maxDist) {
          maxDist = dist;
          a = i + 1;
          b = j + 1;
        }
      }
    }

    Console.WriteLine($"{a} {b}");
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef pair<int, int> pii;
typedef vector<pii> vpii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vpii points(n);
  for (auto& [x, y] : points)
    cin >> x >> y;

  int maxDist = -1, a = 0, b = 0;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      int dx = points[i].first - points[j].first;
      int dy = points[i].second - points[j].second;
      int dist = dx * dx + dy * dy;

      if (dist > maxDist) {
        maxDist = dist;
        a = i + 1;
        b = j + 1;
      }
    }
  }

  cout << a << " " << b << "\n";

  return 0;
}
```
