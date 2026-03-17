---
layout: single
title: "[백준 2075] N번째 큰 수 (C#, C++) - soo:bak"
date: "2026-03-17 20:03:00 +0900"
description: "백준 2075번 C#, C++ 풀이 - 크기 N의 최소 힙만 유지해 N번째 큰 수를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 2075
  - C#
  - C++
  - 알고리즘
  - 우선순위 큐
  - 힙
keywords: "백준 2075, 백준 2075번, BOJ 2075, N번째 큰 수, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2075번 - N번째 큰 수](https://www.acmicpc.net/problem/2075)

## 설명
`N x N` 표에 있는 모든 수 중에서 `N`번째로 큰 수를 구하는 문제입니다.

표의 각 수는 자기 바로 위에 있는 수보다 크다는 조건이 있지만, 이 문제는 그 조건을 직접 활용하지 않아도 풀 수 있습니다. 핵심은 **전체 숫자를 다 저장하지 않고도 N번째 큰 수를 찾는 것**입니다.

<br>

## 접근법
메모리 제한이 `12MB`이므로 표 전체를 배열에 저장하는 방식은 적절하지 않습니다. 대신 수를 하나씩 읽으면서, 지금까지 나온 값 중 큰 값 `N`개만 남겨 두면 됩니다.

이를 위해 크기가 `N`인 **최소 힙(min-heap)** 을 사용합니다. 최소 힙의 맨 위에는 현재 힙에 들어 있는 값 중 가장 작은 값이 있으므로, 새 숫자를 읽을 때마다 그 값과 비교하면 됩니다.

처음에는 힙 크기가 `N`보다 작으므로 그대로 넣습니다. 힙이 `N`개로 찬 뒤에는 새 숫자가 힙의 최솟값보다 클 때만 최솟값을 빼고 새 숫자를 넣습니다. 반대로 새 숫자가 더 작거나 같다면, 지금 남겨 둔 큰 값 `N`개 안에 들어갈 수 없으므로 버리면 됩니다.

이 과정을 끝까지 반복하면 힙에는 전체 수 중 큰 값 `N`개만 남습니다. 그러면 힙의 최솟값이 그 `N`개 중 가장 작은 값이므로, 결국 전체에서 `N`번째로 큰 수가 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.IO;
using System.Collections.Generic;

class FastScanner {
  private readonly Stream stream = Console.OpenStandardInput();
  private readonly byte[] buffer = new byte[1 << 16];
  private int index;
  private int size;

  private int Read() {
    if (index >= size) {
      size = stream.Read(buffer, 0, buffer.Length);
      index = 0;
      if (size == 0)
        return -1;
    }
    return buffer[index++];
  }

  public int NextInt() {
    int c = Read();
    while (c <= 32) {
      c = Read();
    }

    int sign = 1;
    if (c == '-') {
      sign = -1;
      c = Read();
    }

    int value = 0;
    while (c > 32) {
      value = value * 10 + (c - '0');
      c = Read();
    }
    return value * sign;
  }
}

class Program {
  static void Main() {
    var fs = new FastScanner();
    int n = fs.NextInt();

    var pq = new PriorityQueue<int, int>();

    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        int num = fs.NextInt();

        if (pq.Count < n) {
          pq.Enqueue(num, num);
        } else if (num > pq.Peek()) {
          pq.Dequeue();
          pq.Enqueue(num, num);
        }
      }
    }

    Console.WriteLine(pq.Peek());
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

  priority_queue<int, vector<int>, greater<int>> pq;

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      int num;
      cin >> num;

      if ((int)pq.size() < n) {
        pq.push(num);
      } else if (num > pq.top()) {
        pq.pop();
        pq.push(num);
      }
    }
  }

  cout << pq.top() << "\n";

  return 0;
}
```
