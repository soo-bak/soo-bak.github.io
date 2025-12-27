---
layout: single
title: "[백준 5768] Divide and Conquer (C#, C++) - soo:bak"
date: "2025-12-27 04:55:00 +0900"
description: 구간 [M, N]에서 약수 개수가 최대인 수 X와 그 약수 개수 Y를 찾는 문제
---

## 문제 링크
[5768번 - Divide and Conquer](https://www.acmicpc.net/problem/5768)

## 설명
1 ≤ M ≤ N ≤ 5000인 구간이 주어질 때, 약수의 개수가 가장 많은 수 X를 찾고 그 개수 Y를 함께 출력합니다. 약수 개수 최대가 여러 개면 X가 가장 큰 것을 선택합니다. 입력은 M=N=0에서 종료합니다.

<br>

## 접근법
1부터 5000까지의 약수 개수를 미리 구해 둡니다. 각 수의 배수들에 1씩 더해주면 됩니다.

각 테스트에서 구간을 순회하며 약수 개수가 더 크거나, 같으면서 값이 더 큰 경우 갱신합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    const int LIM = 5000;
    var divs = new int[LIM + 1];
    for (var i = 1; i <= LIM; i++) {
      for (var j = i; j <= LIM; j += i)
        divs[j]++;
    }

    var parts = Console.In.ReadToEnd().Split((char[])null, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var sb = new StringBuilder();
    while (idx + 1 < parts.Length) {
      var m = int.Parse(parts[idx++]);
      var n = int.Parse(parts[idx++]);
      if (m == 0 && n == 0)
        break;

      var bestX = m;
      var bestY = divs[m];
      for (var x = m; x <= n; x++) {
        var y = divs[x];
        if (y > bestY || (y == bestY && x > bestX)) {
          bestY = y;
          bestX = x;
        }
      }
      sb.AppendLine($"{bestX} {bestY}");
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  const int LIM = 5000;
  vi divs(LIM + 1, 0);
  for (int i = 1; i <= LIM; i++) {
    for (int j = i; j <= LIM; j += i)
      divs[j]++;
  }

  int m, n;
  while (cin >> m >> n) {
    if (m == 0 && n == 0)
      break;
    int bestX = m, bestY = divs[m];
    for (int x = m; x <= n; x++) {
      int y = divs[x];
      if (y > bestY || (y == bestY && x > bestX)) {
        bestY = y;
        bestX = x;
      }
    }
    cout << bestX << " " << bestY << "\n";
  }

  return 0;
}
```
