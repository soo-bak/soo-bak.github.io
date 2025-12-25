---
layout: single
title: "[백준 24421] 掛け算 (Multiplication) (C#, C++) - soo:bak"
date: "2025-12-26 02:05:00 +0900"
description: 순서를 유지한 세 수의 곱을 세는 문제
---

## 문제 링크
[24421번 - 掛け算 (Multiplication)](https://www.acmicpc.net/problem/24421)

## 설명
수열에서 왼쪽부터 x, y, z를 골라 x × y = z가 되는 경우의 수를 구하는 문제입니다.

<br>

## 접근법
먼저 세 수를 고르는 순서를 고정해 왼쪽에서 오른쪽으로 고릅니다.

다음으로 모든 i < j < k 조합을 확인하며 곱이 같은지 세어 누적합니다.

마지막으로 누적한 값을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var a = new int[n];
    for (var i = 0; i < n; i++)
      a[i] = int.Parse(parts[idx++]);

    var ans = 0;
    for (var i = 0; i < n; i++) {
      for (var j = i + 1; j < n; j++) {
        for (var k = j + 1; k < n; k++) {
          if (a[i] * a[j] == a[k]) ans++;
        }
      }
    }

    Console.WriteLine(ans);
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

  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int ans = 0;
  for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
      for (int k = j + 1; k < n; k++) {
        if (a[i] * a[j] == a[k]) ans++;
      }
    }
  }

  cout << ans << "\n";
  
  return 0;
}
```
