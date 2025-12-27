---
layout: single
title: "[백준 11586] 지영 공주님의 마법 거울 (C#, C++) - soo:bak"
date: "2025-04-21 00:59:00 +0900"
description: 거울에 비친 이미지를 조건에 따라 회전 또는 반전하여 출력하는 백준 11586번 지영 공주님의 마법 거울의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11586
  - C#
  - C++
  - 알고리즘
  - 문자열
  - 구현
keywords: "백준 11586, 백준 11586번, BOJ 11586, mirrorReflection, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11586번 - 지영 공주님의 마법 거울](https://www.acmicpc.net/problem/11586)

## 설명
**입력된 여러 줄의 문자열을 거울에 비친 방식에 따라 출력 형식을 조정하는 문제입니다.**
<br>

- 전체 문자열은 여러 줄로 이루어져 있으며, 각 줄은 고정된 길이를 갖습니다.
- 마지막 입력으로 주어지는 숫자에 따라 출력 방향이 결정됩니다.
  - `1`: 변형 없이 그대로 출력합니다.
  - `2`: 좌/우 반전하여 출력합니다.
  - `3`: 상/하 반전하여 출력합니다.

## 접근법

- 먼저 출력할 줄 수를 입력받고, 해당 줄 수만큼 문자열을 순서대로 저장합니다.
- 이후 입력된 출력 방식에 따라 다음과 같이 처리합니다:

  - `1`이 입력된 경우, 저장한 줄들을 입력받은 순서대로 그대로 출력합니다.
  - `2`인 경우, 각 줄의 문자를 오른쪽에서 왼쪽 순으로 바꿔 출력합니다.
  - `3`인 경우, 전체 줄의 순서를 마지막 줄부터 처음 줄까지 거꾸로 출력합니다.

- 각 처리 방식은 입력받은 줄 수 또는 한 줄의 길이에 비례하는 횟수만큼 반복되므로,<br>
전체 시간 복잡도는 `O(n × m)` 수준입니다.(`n`: 줄 수, `m`: 각 줄의 길이)


## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var lines = new List<string>();
    for (int i = 0; i < n; i++) lines.Add(Console.ReadLine());
    int mode = int.Parse(Console.ReadLine());

    if (mode == 1) {
      foreach (var line in lines) Console.WriteLine(line);
    } else if (mode == 2) {
      foreach (var line in lines)
        Console.WriteLine(new string(line.Reverse().ToArray()));
    } else {
      for (int i = lines.Count - 1; i >= 0; i--)
        Console.WriteLine(lines[i]);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vs mirror(n);
  for (auto &s : mirror) cin >> s;

  int k; cin >> k;
  if (k == 1) {
    for (auto &s : mirror) cout << s << '\n';
  } else if (k == 2) {
    for (auto &s : mirror)
      cout << string(s.rbegin(), s.rend()) << '\n';
  } else {
    for (int i = n - 1; i >= 0; i--) cout << mirror[i] << '\n';
  }

  return 0;
}
```
