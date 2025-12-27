---
layout: single
title: "[백준 12604] Store Credit (Large) (C#, C++) - soo:bak"
date: "2025-12-26 03:55:00 +0900"
description: "백준 12604번 C#, C++ 풀이 - 합이 크레딧이 되는 두 물건의 위치를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 12604
  - C#
  - C++
  - 알고리즘
keywords: "백준 12604, 백준 12604번, BOJ 12604, StoreCreditLarge, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12604번 - Store Credit (Large)](https://www.acmicpc.net/problem/12604)

## 설명
주어진 가격 목록에서 합이 크레딧이 되는 두 물건의 위치를 찾는 문제입니다.

<br>

## 접근법
먼저 가격과 인덱스를 함께 저장해 정렬합니다.

다음으로 양 끝 포인터를 움직이며 합이 크레딧이 되는 쌍을 찾습니다.

마지막으로 원래 인덱스를 작은 값부터 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var caseNum = 1; caseNum <= t; caseNum++) {
      var c = int.Parse(parts[idx++]);
      var n = int.Parse(parts[idx++]);
      var arr = new int[n][];
      for (var i = 0; i < n; i++)
        arr[i] = new int[] { int.Parse(parts[idx++]), i + 1 };

      Array.Sort(arr, (x, y) => x[0].CompareTo(y[0]));

      var l = 0;
      var r = n - 1;
      var a = 0;
      var b = 0;
      while (l < r) {
        var sum = arr[l][0] + arr[r][0];
        if (sum == c) {
          a = arr[l][1];
          b = arr[r][1];
          break;
        }
        if (sum < c) l++;
        else r--;
      }

      if (a > b) {
        var tmp = a;
        a = b;
        b = tmp;
      }
      sb.AppendLine($"Case #{caseNum}: {a} {b}");
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;

  for (int caseNum = 1; caseNum <= t; caseNum++) {
    int c, n; cin >> c >> n;

    vector<pii> arr(n);
    for (int i = 0; i < n; i++) {
      int v;
      cin >> v;
      arr[i] = {v, i + 1};
    }

    sort(arr.begin(), arr.end());

    int l = 0;
    int r = n - 1;
    int a = 0;
    int b = 0;
    while (l < r) {
      int sum = arr[l].first + arr[r].first;
      if (sum == c) {
        a = arr[l].second;
        b = arr[r].second;
        break;
      }
      if (sum < c) l++;
      else r--;
    }

    if (a > b) {
      int tmp = a;
      a = b;
      b = tmp;
    }
    cout << "Case #" << caseNum << ": " << a << " " << b << "\n";
  }

  return 0;
}
```
