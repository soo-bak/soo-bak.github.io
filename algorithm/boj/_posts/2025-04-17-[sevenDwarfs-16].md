---
layout: single
title: "[백준 2309] 일곱 난쟁이 (C#, C++) - soo:bak"
date: "2025-04-17 00:16:47 +0900"
description: 아홉 난쟁이 중 합이 100이 되는 일곱 명을 찾아 출력하는 백준 2309번 일곱 난쟁이 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2309
  - C#
  - C++
  - 알고리즘
keywords: "백준 2309, 백준 2309번, BOJ 2309, sevenDwarfs, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2309번 - 일곱 난쟁이](https://www.acmicpc.net/problem/2309)

## 설명
**아홉 명의 난쟁이 중에서 합이 정확히 100이 되는 일곱 명을 찾는 문제**입니다.<br>
<br>

- 아홉 명의 키가 주어지고, 이 중 일곱 명의 키 합이 `100`이 되는 조합을 찾아야 합니다.<br>
- 단 한 가지 조합만 존재한다고 보장됩니다.<br>
- 정답으로 출력할 때는 **일곱 명의 키를 오름차순으로 출력**해야 합니다.<br>

### 접근법
- 총합을 구한 뒤, 아홉 명 중 **두 명을 제외한 키의 합이 100**이 되도록 두 명의 조합을 찾아냅니다.<br>
- 즉, 전체 합에서 100을 뺀 값을 `target`이라 할 때,<br>
  두 명의 키 합이 `target`이 되는 쌍을 찾아 제외합니다.<br>
- 남은 일곱 명의 키를 정렬하여 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var heights = new List<int>();
    int total = 0;

    for (int i = 0; i < 9; i++) {
      int h = int.Parse(Console.ReadLine());
      heights.Add(h);
      total += h;
    }

    int target = total - 100;
    int skip1 = -1, skip2 = -1;

    for (int i = 0; i < 8; i++) {
      for (int j = i + 1; j < 9; j++) {
        if (heights[i] + heights[j] == target) {
          skip1 = i;
          skip2 = j;
          break;
        }
      }
      if (skip1 != -1) break;
    }

    var result = new List<int>();
    for (int i = 0; i < 9; i++) {
      if (i != skip1 && i != skip2)
        result.Add(heights[i]);
    }

    result.Sort();
    foreach (var h in result)
      Console.WriteLine(h);
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

  vi heights(9);

  int total = 0;
  for (int i = 0; i < 9; i++) {
    cin >> heights[i];
    total += heights[i];
  }

  int target = total - 100;

  bool found = false;
  int exclude1, exclude2;
  for (int i = 0; i < 8 && !found; i++) {
    for (int j = i + 1; j < 9 && !found; j++) {
      if (heights[i] + heights[j] == target) {
        exclude1 = i;
        exclude2 = j;
        found = true;
      }
    }
  }

  vi res;
  for (int i = 0; i < 9; i++) {
    if (i != exclude1 && i != exclude2)
      res.push_back(heights[i]);
  }

  sort(res.begin(), res.end());

  for (int height : res)
    cout << height << "\n";

  return 0;
}
```
