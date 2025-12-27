---
layout: single
title: "[백준 15121] Star Arrangements (C#, C++) - soo:bak"
date: "2025-12-27 03:15:00 +0900"
description: 두 줄의 별 개수 x,y로 번갈아 배치할 때 별 총합이 S가 되는 모든 패턴을 찾는 문제
---

## 문제 링크
[15121번 - Star Arrangements](https://www.acmicpc.net/problem/15121)

## 설명
첫 줄에 x개, 둘째 줄에 y개 별을 두고 x,y,x,y… 식으로 번갈아 배치합니다. 인접 줄 차이는 1 이하이고 첫 줄이 둘째 줄보다 적을 수 없습니다. 총 별의 수가 S가 되는 모든 패턴을 찾아 출력하는 문제입니다. (1,1)과 같은 자명한 패턴은 제외합니다.

<br>

## 접근법
두 줄의 별 개수는 같거나 1 차이이며, 첫 줄이 둘째 줄보다 크거나 같아야 합니다. 두 줄의 개수가 같을 때는 별 총합이 해당 개수로 나누어떨어지고 줄 수가 2 이상이면 가능합니다. 1 차이일 때는 두 줄 합의 배수이거나 거기에 첫 줄 개수를 더한 형태로 표현되면 가능합니다.

가능한 모든 패턴을 찾아 첫 줄 개수 오름차순, 같으면 둘째 줄 개수 오름차순으로 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Text;

class Program {
  static void Main() {
    var s = int.Parse(Console.ReadLine()!);
    var list = new List<(int x, int y)>();

    for (var x = 2; x <= s; x++) {
      if (s % x == 0 && s / x >= 2)
        list.Add((x, x));
      var sum = 2 * x - 1;
      var r = s % sum;
      if (s >= sum && (r == 0 || r == x))
        list.Add((x, x - 1));
    }

    list.Sort();

    var sb = new StringBuilder();
    sb.AppendLine($"{s}:");
    foreach (var p in list)
      sb.AppendLine($"{p.x},{p.y}");
    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef pair<int, int> pii;
typedef vector<pii> vpii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int s; cin >> s;
  vpii res;

  for (int x = 2; x <= s; x++) {
    if (s % x == 0 && s / x >= 2)
      res.push_back({x, x});
    int sum = 2 * x - 1;
    int r = s % sum;
    if (s >= sum && (r == 0 || r == x))
      res.push_back({x, x - 1});
  }

  sort(res.begin(), res.end());

  cout << s << ":\n";
  for (auto [x, y] : res)
    cout << x << "," << y << "\n";

  return 0;
}
```
