---
layout: single
title: "[백준 3040] 백설 공주와 일곱 난쟁이 (C#, C++) - soo:bak"
date: "2025-04-17 00:25:43 +0900"
description: 아홉 난쟁이 중에서 합이 100이 되는 일곱 명을 찾아 출력하는 백준 3040번 백설 공주와 일곱 난쟁이 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3040
  - C#
  - C++
  - 알고리즘
keywords: "백준 3040, 백준 3040번, BOJ 3040, snowWhiteSeven, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3040번 - 백설 공주와 일곱 난쟁이](https://www.acmicpc.net/problem/3040)

## 설명
**아홉 난쟁이의 키 중에서 합이 정확히 100이 되는 일곱 명을 찾아 출력하는 문제**입니다.<br>
<br>

- 아홉 개의 자연수가 주어지며, 이 중 두 개는 가짜 난쟁이의 키입니다.<br>
- 나머지 일곱 개의 수의 합이 정확히 `100`이 되도록 하는 조합을 찾아야 합니다.<br>
- 조건에 맞는 일곱 난쟁이의 키를 **입력 순서를 유지한 채 출력**해야 합니다.<br>

### 접근법
- 전체 키의 총합을 구한 뒤, 그 합에서 `100`을 뺀 값을 저장해둡니다.<br>
- 아홉 명 중 두 명을 골라, 그 두 키의 합이 위에서 계산한 값과 같다면 해당 두 명이 가짜 난쟁이입니다.<br>
- 조건을 만족하는 두 명을 제외한 나머지 일곱 명을 입력 순서대로 출력하면 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var dwarfs = new List<int>();
    int total = 0;

    for (int i = 0; i < 9; i++) {
      int h = int.Parse(Console.ReadLine());
      dwarfs.Add(h);
      total += h;
    }

    int excess = total - 100;
    int skip1 = -1, skip2 = -1;
    for (int i = 0; i < 8; i++) {
      for (int j = i + 1; j < 9; j++) {
        if (dwarfs[i] + dwarfs[j] == excess) {
          skip1 = i;
          skip2 = j;
          break;
        }
      }
      if (skip1 != -1) break;
    }

    for (int i = 0; i < 9; i++) {
      if (i != skip1 && i != skip2)
        Console.WriteLine(dwarfs[i]);
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
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi dwarfs(9);
  int total = 0;

  for (int i = 0; i < 9; i++) {
    cin >> dwarfs[i];
    total += dwarfs[i];
  }

  int excess = total - 100;
  int fake1 = -1, fake2 = -1;
  bool found = false;
  for (int i = 0; i < 8; i++) {
    for (int j = i + 1; j < 9; j++) {
      if (dwarfs[i] + dwarfs[j] == excess) {
        fake1 = i;
        fake2 = j;
        found = true;
        break;
      }
    }
    if (found) break;
  }

  for (int i = 0; i < 9; i++) {
    if (i != fake1 && i != fake2)
      cout << dwarfs[i] << "\n";
  }

  return 0;
}
```
