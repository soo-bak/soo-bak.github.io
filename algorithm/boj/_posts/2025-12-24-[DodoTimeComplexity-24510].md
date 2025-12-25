---
layout: single
title: "[백준 24510] 시간복잡도를 배운 도도 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: 각 줄에서 for와 while의 등장 횟수를 세어 최댓값을 구하는 문제
---

## 문제 링크
[24510번 - 시간복잡도를 배운 도도](https://www.acmicpc.net/problem/24510)

## 설명
각 줄에 등장하는 for와 while을 반복문으로 보고, 같은 줄에서의 개수를 세어 최댓값을 출력하는 문제입니다.

<br>

## 접근법
먼저 각 줄을 문자열로 읽고 for와 while이 나타나는 위치를 모두 확인해 개수를 세어 더합니다.

다음으로 각 줄마다 계산한 개수를 비교해 최댓값을 갱신합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var c = int.Parse(Console.ReadLine()!);
    var best = 0;

    for (var i = 0; i < c; i++) {
      var line = Console.ReadLine()!;
      var cnt = 0;
      for (var j = 0; j + 2 < line.Length; j++) {
        if (line[j] == 'f' && line[j + 1] == 'o' && line[j + 2] == 'r') cnt++;
      }
      for (var j = 0; j + 4 < line.Length; j++) {
        if (line[j] == 'w' && line[j + 1] == 'h' && line[j + 2] == 'i'
            && line[j + 3] == 'l' && line[j + 4] == 'e') cnt++;
      }
      if (cnt > best) best = cnt;
    }

    Console.WriteLine(best);
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

  int c; cin >> c;
  int best = 0;
  for (int i = 0; i < c; i++) {
    string line; cin >> line;
    int cnt = 0;
    for (int j = 0; j + 2 < (int)line.size(); j++) {
      if (line[j] == 'f' && line[j + 1] == 'o' && line[j + 2] == 'r') cnt++;
    }
    for (int j = 0; j + 4 < (int)line.size(); j++) {
      if (line[j] == 'w' && line[j + 1] == 'h' && line[j + 2] == 'i'
          && line[j + 3] == 'l' && line[j + 4] == 'e') cnt++;
    }
    if (cnt > best) best = cnt;
  }

  cout << best << "\n";

  return 0;
}
```
