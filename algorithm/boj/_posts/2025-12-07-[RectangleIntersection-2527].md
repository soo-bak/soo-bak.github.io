---
layout: single
title: "[백준 2527] 직사각형 (C#, C++) - soo:bak"
date: "2025-12-07 02:25:00 +0900"
description: 두 직사각형의 교차 형태를 겹치는 구간 길이로 판별하는 백준 2527번 직사각형 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[2527번 - 직사각형](https://www.acmicpc.net/problem/2527)

## 설명
두 직사각형이 주어질 때, 겹치는 부분이 직사각형이면 a, 선분이면 b, 점이면 c, 없으면 d를 출력하는 문제입니다. 4개의 테스트케이스가 주어집니다.

<br>

## 접근법
두 직사각형이 겹치는 부분의 형태는 가로와 세로 방향에서 각각 겹치는 길이로 판단할 수 있습니다.

가로 방향 겹침 길이는 두 직사각형의 오른쪽 끝 중 작은 값에서 왼쪽 끝 중 큰 값을 뺀 것입니다. 세로 방향도 마찬가지로 위쪽 끝 중 작은 값에서 아래쪽 끝 중 큰 값을 뺍니다.

가로와 세로 겹침 길이가 모두 양수이면 직사각형으로 겹칩니다. 둘 중 하나라도 음수이면 겹치지 않습니다. 둘 다 0이면 한 점에서만 만납니다. 하나만 0이면 선분으로 겹칩니다.

<br>

- - -

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    for (var t = 0; t < 4; t++) {
      var s = Console.ReadLine()!.Split();
      var x1 = int.Parse(s[0]);
      var y1 = int.Parse(s[1]);
      var p1 = int.Parse(s[2]);
      var q1 = int.Parse(s[3]);
      var x2 = int.Parse(s[4]);
      var y2 = int.Parse(s[5]);
      var p2 = int.Parse(s[6]);
      var q2 = int.Parse(s[7]);

      var dx = Math.Min(p1, p2) - Math.Max(x1, x2);
      var dy = Math.Min(q1, q2) - Math.Max(y1, y2);

      if (dx > 0 && dy > 0) Console.WriteLine("a");
      else if (dx < 0 || dy < 0) Console.WriteLine("d");
      else if (dx == 0 && dy == 0) Console.WriteLine("c");
      else Console.WriteLine("b");
    }
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

  for (int t = 0; t < 4; t++) {
    int x1, y1, p1, q1, x2, y2, p2, q2;
    cin >> x1 >> y1 >> p1 >> q1 >> x2 >> y2 >> p2 >> q2;

    int dx = min(p1, p2) - max(x1, x2);
    int dy = min(q1, q2) - max(y1, y2);

    if (dx > 0 && dy > 0) cout << "a\n";
    else if (dx < 0 || dy < 0) cout << "d\n";
    else if (dx == 0 && dy == 0) cout << "c\n";
    else cout << "b\n";
  }

  return 0;
}
```
