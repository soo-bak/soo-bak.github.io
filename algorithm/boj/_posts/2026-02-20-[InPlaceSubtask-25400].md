---
layout: single
title: "[백준 25400] 제자리 서브태스크 (C#, C++) - soo:bak"
date: "2026-02-20 22:13:00 +0900"
description: "백준 25400번 C#, C++ 풀이 - 최소 카드 제거로 남은 수열을 1,2,3,... 형태로 만드는 문제"
tags:
  - 백준
  - BOJ
  - 25400
  - C#
  - C++
  - 알고리즘
  - 구현
  - 그리디
keywords: "백준 25400, 백준 25400번, BOJ 25400, 제자리 서브태스크, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25400번 - 제자리 서브태스크](https://www.acmicpc.net/problem/25400)

## 설명
카드를 일부 제거한 뒤 남은 카드들이 왼쪽부터 `1, 2, 3, ...` 순서가 되도록 만들 때, 제거해야 하는 카드 수의 최솟값을 구하는 문제입니다.

<br>

## 접근법
남길 수 있는 카드의 최대 개수를 `k`라고 하면, 정답은 `N-k`입니다. 남은 수열은 반드시 `1,2,3,...,k` 형태여야 하므로, 왼쪽부터 보면서 현재 필요한 값 `need`를 두고 `A[i] == need`일 때만 채택하면 됩니다. 이렇게 얻는 `k`가 최댓값이므로 한 번 순회로 답을 구할 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var fs = new FastScanner();
    int n = fs.NextInt();

    int need = 1;
    for (int i = 0; i < n; i++) {
      int x = fs.NextInt();
      if (x == need)
        need++;
    }

    int kept = need - 1;
    Console.WriteLine(n - kept);
  }

  private sealed class FastScanner {
    private readonly byte[] buffer = new byte[1 << 16];
    private int ptr;
    private int len;

    private int Read() {
      if (ptr >= len) {
        len = Console.OpenStandardInput().Read(buffer, 0, buffer.Length);
        ptr = 0;
        if (len == 0)
          return -1;
      }
      return buffer[ptr++];
    }

    public int NextInt() {
      int c = Read();
      while (c <= 32)
        c = Read();
      int v = 0;
      while (c > 32) {
        v = v * 10 + (c - '0');
        c = Read();
      }
      return v;
    }
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

  int n; cin >> n;

  int need = 1;
  for (int i = 0; i < n; i++) {
    int x; cin >> x;
    if (x == need)
      need++;
  }

  int kept = need - 1;
  cout << (n - kept) << "\n";

  return 0;
}
```
