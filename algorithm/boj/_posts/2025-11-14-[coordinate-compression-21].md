---
layout: single
title: "[백준 18870] 좌표 압축 (C#, C++) - soo:bak"
date: "2025-11-14 23:27:00 +0900"
description: 서로 다른 좌표의 상대적 순위를 부여해 압축 좌표를 출력하는 백준 18870번 좌표 압축 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[18870번 - 좌표 압축](https://www.acmicpc.net/problem/18870)

## 설명

좌표 `X1, X2, ..., XN`에 대해, 각 좌표보다 작은 서로 다른 좌표의 개수를 새로운 값으로 출력하는 문제입니다.<br>
동일한 좌표는 같은 값으로 묶어야 하며, 입력 크기는 최대 `1,000,000`입니다.<br>

<br>

## 접근법

좌표를 정렬해 중복을 제거한 뒤, 원래의 좌표를 이 정렬된 리스트에서의 인덱스로 치환하면 됩니다.

- 입력 배열을 복사해 정렬하고 `Distinct`/`unique`로 중복을 제거합니다.
- 원본 좌표마다 정렬된 배열에서의 위치(이진 탐색 또는 딕셔너리 Lookup)를 찾습니다.
- 출력은 입력 순서를 유지한 채 공백으로 구분합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var arr = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    var sorted = arr.Distinct().OrderBy(x => x).ToArray();
    var index = new Dictionary<int, int>(sorted.Length);
    for (var i = 0; i < sorted.Length; i++)
      index[sorted[i]] = i;

    var compressed = arr.Select(x => index[x]);
    Console.WriteLine(string.Join(" ", compressed));
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

  int n;
  cin >> n;
  vector<int> arr(n);
  for (int i = 0; i < n; ++i)
    cin >> arr[i];

  vector<int> sorted = arr;
  sort(sorted.begin(), sorted.end());
  sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());

  for (int i = 0; i < n; ++i) {
    int idx = lower_bound(sorted.begin(), sorted.end(), arr[i]) - sorted.begin();
    cout << idx;
    if (i + 1 < n) cout << ' ';
  }
  cout << "\n";

  return 0;
}
```

