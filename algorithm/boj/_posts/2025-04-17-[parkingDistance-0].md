---
layout: single
title: "[백준 5054] 주차의 신 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 상점들의 위치를 기준으로 왕복 주차 거리의 최소값을 구하는 백준 5054번 주차의 신 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5054번 - 주차의 신](https://www.acmicpc.net/problem/5054)

## 설명
**여러 상점의 위치가 주어졌을 때, 최소 이동 거리로 왕복 주차를 하는 문제**입니다.<br>
<br>

- 테스트케이스마다 여러 상점의 위치가 주어집니다.<br>
- 자동차를 세우고 모든 상점을 방문한 후 다시 돌아오는 왕복 경로를 고려해야 합니다.<br>
- 가장 효율적인 주차 위치는 상점들 사이 가장 끝에 있는 곳에 주차한 뒤 전체를 오가는 경로입니다.<br>
- 즉, **가장 먼 두 상점 사이의 거리 × 2**가 최소 왕복 거리입니다.<br>

### 접근법
- 각 테스트케이스마다 모든 상점의 위치를 입력받습니다.<br>
- 가장 왼쪽(min)과 가장 오른쪽(max)의 위치를 찾습니다.<br>
- 왕복 거리 = `(max - min) * 2`로 계산하여 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int n = int.Parse(Console.ReadLine());
      var arr = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int min = arr.Min(), max = arr.Max();
      Console.WriteLine((max - min) * 2);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int cntStore; cin >> cntStore;
    int min = 99, max = 0;
    for (int i = 0; i < cntStore; i++) {
      int cordi; cin >> cordi;
      if (min > cordi) min = cordi;
      if (max < cordi) max = cordi;
    }
    cout << 2 * (max - min) << "\n";
  }

  return 0;
}
```
