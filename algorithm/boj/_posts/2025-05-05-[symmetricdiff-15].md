---
layout: single
title: "[백준 1269] 대칭 차집합 (C#, C++) - soo:bak"
date: "2025-05-05 03:12:00 +0900"
description: 두 집합 A와 B의 대칭 차집합의 원소 개수를 계산하는 백준 1269번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1269
  - C#
  - C++
  - 알고리즘
keywords: "백준 1269, 백준 1269번, BOJ 1269, symmetricdiff, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1269 - 대칭 차집합](https://www.acmicpc.net/problem/1269)

## 설명

공집합이 아닌 두 집합 `A`와 `B`가 주어졌을 때,
**두 집합의 대칭 차집합에 포함되는 원소의 개수**를 구하는 문제입니다.

<br>
대칭 차집합은 다음과 같이 정의됩니다:

$$A \triangle B = (A - B) \cup (B - A)$$

<br>
즉, 한 집합에는 포함되어 있지만 다른 집합에는 포함되지 않는 원소들의 집합이며,

두 집합 중 **한 쪽에만 존재하는 원소들만을 모은 결과**입니다.

<br>

## 접근법

- 먼저 집합 `A`의 모든 원소를 해시 기반 자료구조(Set)에 저장합니다.
  - `B`의 원소와의 중복 여부를 효율적으로 판별하기 위함입니다.
- 집합 `B`의 원소를 하나씩 확인하며 다음을 수행합니다:
  - 해당 원소가 `A`에 존재하면, 이는 교집합 원소이므로 제거합니다.
  - 존재하지 않는다면, 이는 `B - A`에 해당하므로 대칭 차집합의 후보로 개수를 하나 증가시킵니다.
- 위 과정이 끝난 후, `A` 집합에 남아 있는 원소 개수는 `A - B`이며,<br>
  앞서 누적한 개수와 합산하여 최종 답을 구할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int n = int.Parse(input[0]);
    int m = int.Parse(input[1]);

    var setA = new HashSet<int>();
    var tokens = Console.ReadLine().Split();
    foreach (var tok in tokens)
      setA.Add(int.Parse(tok));

    int count = 0;
    tokens = Console.ReadLine().Split();
    foreach (var tok in tokens) {
      int val = int.Parse(tok);
      if (setA.Remove(val)) n--;
      else count++;
    }

    count += n;
    Console.WriteLine(count);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef unordered_set<int> ui;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  ui a;
  for (int i = 0; i < n; i++) {
    int x; cin >> x;
    a.insert(x);
  }

  int ans = 0;
  for (int i = 0; i < m; i++) {
    int x; cin >> x;
    if (a.erase(x)) n--;
    else ans++;
  }

  ans += n;

  cout << ans << "\n";

  return 0;
}
```
