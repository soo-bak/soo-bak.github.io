---
layout: single
title: "[백준 9437] 사라진 페이지 찾기 (C#, C++) - soo:bak"
date: "2025-05-03 02:25:00 +0900"
description: 4의 배수 형태로 구성된 시험지에서 한 페이지만 남았을 때 나머지 사라진 페이지를 추론하는 백준 9437번 사라진 페이지 찾기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9437
  - C#
  - C++
  - 알고리즘
keywords: "백준 9437, 백준 9437번, BOJ 9437, missingpages, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9437번 - 사라진 페이지 찾기](https://www.acmicpc.net/problem/9437)

## 설명
시험지는 총 `N쪽`으로 구성되며, 이 수는 항상 `4의 배수`입니다.

`한 장`의 종이에는 앞면과 뒷면에 각각 `두 쪽`씩, 총 `4쪽`이 인쇄됩니다.

예를 들어 `N = 12`인 경우, `한 장`은 다음과 같은 방식으로 구성됩니다:
-  앞면 `(a, b)`, 뒷면 `(c, d)`
- 실제 페이지 조합: `1, 2, 11, 12` / `3, 4, 9, 10` / `5, 6, 7, 8`

<br>
이때 어떤 이유로 `한 페이지`만 남고 나머지 종이가 사라졌다면,

그 페이지만으로 같은 종이에 인쇄되어 있었던 `나머지 세 페이지`를 찾아 출력하는 문제입니다.

<br> n

## 접근법
- 전체 페이지 수 `N`은 `4의 배수`이므로, `N ÷ 4` 장의 종이가 존재합니다.
- 각 장은 앞면/뒷면 `2쪽`씩, 총 `4쪽`으로 구성됩니다.
- 각 장을 다음과 같이 구성합니다:
  - `i`번 장: [`앞면 왼쪽`, `앞면 오른쪽`, `뒷면 왼쪽`, `뒷면 오른쪽`]
- 전체 페이지 배열을 구성하고, 각 페이지마다 해당 종이의 번호를 부여합니다.
- 이후 입력으로 주어진 페이지가 속한 종이를 찾아,
  - 그 종이에 포함된 나머지 세 페이지를 `오름차순`으로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    while (true) {
      var parts = Console.ReadLine().Split();
      int n = int.Parse(parts[0]);
      if (n == 0) break;

      int p = int.Parse(parts[1]);
      var page = new int[n + 1];

      for (int i = 1; i <= n / 2; i += 2) {
        page[i] = page[i + 1] = (i + 1) / 2;
        if (i + n / 2 <= n)
          page[i + n / 2] = page[i + n / 2 + 1] = n / 4 + 1 - (i + 1) / 2;
      }

      var res = new List<int>();
      for (int i = 1; i <= n; i++) {
        if (i == p) continue;
        if (page[i] == page[p]) res.Add(i);
      }

      res.Sort();
      Console.WriteLine(string.Join(" ", res));
    }
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

  while (true) {
    int n; cin >> n;
    if (!n) break;

    vi page(n + 1);
    for (int i = 1; i <= n / 2; i += 2) {
      page[i] = page[i + 1] = (i + 1) / 2;
      if (i + n / 2 <= n)
        page[i + n / 2] = page[i + n / 2 + 1] = n / 4 + 1 - (i + 1) / 2;
    }

    int p; cin >> p;
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
      if (i == p) continue;
      if (page[i] == page[p]) {
        cout << i << (++cnt == 3 ? "\n" : " ");
        if (cnt == 3) break;
      }
    }
  }

  return 0;
}
```
