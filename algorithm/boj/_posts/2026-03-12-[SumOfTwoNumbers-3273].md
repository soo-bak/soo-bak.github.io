---
layout: single
title: "[백준 3273] 두 수의 합 (C#, C++) - soo:bak"
date: "2026-03-12 20:21:00 +0900"
description: "백준 3273번 C#, C++ 풀이 - 정렬과 투 포인터로 합이 x가 되는 두 수의 쌍 개수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 3273
  - C#
  - C++
  - 알고리즘
  - 정렬
  - 투 포인터
keywords: "백준 3273, 백준 3273번, BOJ 3273, 두 수의 합, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3273번 - 두 수의 합](https://www.acmicpc.net/problem/3273)

## 설명
서로 다른 양의 정수들로 이루어진 수열에서 두 수를 골라 합이 `x`가 되는 쌍의 개수를 구하는 문제입니다.

<br>

## 접근법
수열을 먼저 오름차순으로 정렬합니다. 그 다음 가장 작은 값과 가장 큰 값을 가리키는 두 포인터를 둡니다.

현재 두 수의 합이 `x`보다 작으면 더 큰 값이 필요하므로 왼쪽 포인터를 오른쪽으로 옮깁니다. 반대로 합이 `x`보다 크면 더 작은 값이 필요하므로 오른쪽 포인터를 왼쪽으로 옮깁니다.

합이 정확히 `x`라면 하나의 유효한 쌍을 찾은 것이므로 개수를 증가시키고, 두 포인터를 모두 한 칸씩 이동합니다. 수들이 서로 다르기 때문에 같은 원소를 다시 고려할 필요가 없습니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine()!);
    int[] arr = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    int x = int.Parse(Console.ReadLine()!);

    Array.Sort(arr);

    int left = 0;
    int right = n - 1;
    int count = 0;

    while (left < right) {
      int sum = arr[left] + arr[right];

      if (sum == x) {
        count++;
        left++;
        right--;
      } else if (sum < x) {
        left++;
      } else {
        right--;
      }
    }

    Console.WriteLine(count);
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
  for (int i = 0; i < n; i++)
    cin >> arr[i];

  int x;
  cin >> x;

  sort(arr.begin(), arr.end());

  int left = 0;
  int right = n - 1;
  int count = 0;

  while (left < right) {
    int sum = arr[left] + arr[right];

    if (sum == x) {
      count++;
      left++;
      right--;
    } else if (sum < x) {
      left++;
    } else {
      right--;
    }
  }

  cout << count << "\n";

  return 0;
}
```
