---
layout: single
title: "[백준 2965] 캥거루 세마리 (C#, C++) - soo:bak"
date: "2025-05-06 08:54:00 +0900"
description: 세 마리의 캥거루가 최대한 점프할 수 있는 횟수를 구하는 백준 2965번 캥거루 세마리 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2965
  - C#
  - C++
  - 알고리즘
  - 수학
keywords: "백준 2965, 백준 2965번, BOJ 2965, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2965번 - 캥거루 세마리](https://www.acmicpc.net/problem/2965)

## 설명
**세 마리의 캥거루가 최대 몇 번 움직일 수 있는지**를 구하는 문제입니다.

수직선 위의 서로 다른 세 좌표에 캥거루가 있고, 매 번 이동에서는 양 끝에 있는 캥거루 중 하나만 선택합니다.

이 때 선택된 캥거루를 다른 두 캥거루 사이의 정수 좌표로만 이동시킬 수 있습니다.

이 조건에서 캥거루가 최대로 이동할 수 있는 횟수를 계산합니다.

## 접근법
- 세 마리의 위치를 오름차순으로 정렬한 후, **양쪽 간격 중 더 넓은 쪽**을 기준으로 점프 횟수를 계산합니다.
  - 이는 각 이동에서 항상 가운데 칸을 채우는 방식으로 점프하므로,<br>
    더 넓은 간격 쪽에서 더 많은 이동이 가능하기 때문입니다.
- 각 간격에서 **가운데 칸을 계속 채워가는 방식**이므로, <br>
  최댓값은 $$ \max(B - A, C - B) - 1 $$ 이 됩니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var cord = Console.ReadLine().Split().Select(int.Parse).ToArray();
    Array.Sort(cord);

    int leftGap = cord[1] - cord[0];
    int rightGap = cord[2] - cord[1];
    int ans = Math.Max(leftGap, rightGap) - 1;

    Console.WriteLine(ans);
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

  int cord[3];
  for (int i = 0; i < 3; i++)
    cin >> cord[i];

  int ans = ((cord[1] - cord[0]) > (cord[2] - cord[1]) ?
    cord[1] - cord[0] - 1 :
    cord[2] - cord[1] - 1);

  cout << ans << "\n";

  return 0;
}
```
