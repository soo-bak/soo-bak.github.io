---
layout: single
title: "[백준 18870] 좌표 압축 (C#, C++) - soo:bak"
date: "2025-11-14 23:27:00 +0900"
description: 서로 다른 좌표의 상대적 순위를 부여해 압축 좌표를 출력하는 백준 18870번 좌표 압축 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 18870
  - C#
  - C++
  - 알고리즘
keywords: "백준 18870, 백준 18870번, BOJ 18870, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18870번 - 좌표 압축](https://www.acmicpc.net/problem/18870)

## 설명

좌표 `X1, X2, ..., XN`에 대해, 각 좌표보다 작은 서로 다른 좌표의 개수를 새로운 값으로 출력하는 문제입니다.<br>

동일한 좌표는 같은 값으로 매핑되어야 하며, 입력 크기는 최대 `1,000,000`입니다.<br>

<br>

## 접근법

좌표 압축은 좌표 값을 상대적 순위로 변환하는 기법입니다.

입력 배열을 복사하여 정렬하고 중복을 제거하면, 서로 다른 좌표들이 오름차순으로 정렬된 배열을 얻을 수 있습니다.

이 배열에서 각 좌표의 인덱스가 해당 좌표보다 작은 서로 다른 좌표의 개수가 됩니다.

원본 배열의 각 좌표를 정렬된 배열에서 찾아 그 위치로 변환합니다.

C#에서는 딕셔너리에 미리 인덱스를 저장해 두어 `O(1)` 조회를 하고, C++에서는 이진 탐색 `lower_bound`를 사용하여 `O(log n)` 조회를 합니다.


입력 순서를 유지한 채 압축된 값들을 공백으로 구분하여 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
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

  int n; cin >> n;
  vi arr(n);
  for (int i = 0; i < n; ++i)
    cin >> arr[i];

  vi sorted = arr;
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

