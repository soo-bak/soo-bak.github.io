---
layout: single
title: "[백준 17298] 오큰수 (C#, C++) - soo:bak"
date: "2025-04-14 05:04:45 +0900"
description: 스택을 활용하여 각 원소의 오큰수를 효율적으로 구하는 백준 17298번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17298
  - C#
  - C++
  - 알고리즘
keywords: "백준 17298, 백준 17298번, BOJ 17298, nextGreaterStack, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17298번 - 오큰수](https://www.acmicpc.net/problem/17298)

## 설명
이 문제는 **자신보다 오른쪽에 있으면서 더 큰 수 중 가장 왼쪽에 있는 수**를 구하는 문제입니다.  
모든 원소에 대해 **오큰수(NGE: Next Greater Element)**를 찾아야 하며,  
조건에 맞는 수가 없다면 `-1`을 출력합니다.

---

## 접근법
- 스택을 활용하여 오큰수를 효율적으로 찾는 **모노톤 스택 알고리듬**을 사용합니다.
- 왼쪽에서 오른쪽으로 배열을 순회하며, 현재 값이 스택 상단 인덱스의 값보다 크다면 그 값을 오큰수로 설정합니다.
- 조건을 만족한 인덱스는 스택에서 제거하고, 현재 인덱스를 스택에 추가합니다.
- 마지막까지 오큰수가 없는 경우 기본값 `-1`을 그대로 유지합니다.

시간 복잡도는 **O(N)**으로, 배열을 한 번만 순회합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int size = int.Parse(Console.ReadLine()!);
      var input = Console.ReadLine()!.Split();
      var arr = Array.ConvertAll(input, int.Parse);
      var ans = new int[size];
      Array.Fill(ans, -1);

      var stack = new Stack<int>();
      for (int i = 0; i < size; i++) {
        while (stack.Count > 0 && arr[stack.Peek()] < arr[i]) {
          ans[stack.Pop()] = arr[i];
        }
        stack.Push(i);
      }

      Console.WriteLine(string.Join(" ", ans));
    }
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
typedef stack<int> si;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int size; cin >> size;
  vi arr(size);
  for (int i = 0; i < size; i++)
    cin >> arr[i];

  si undefinedIdx;
  vi ans(size, -1);
  for (int i = 0; i < size; i++) {
    while (!undefinedIdx.empty() && arr[undefinedIdx.top()] < arr[i]) {
      ans[undefinedIdx.top()] = arr[i];
      undefinedIdx.pop();
    }
    undefinedIdx.push(i);
  }

  for (int i = 0; i < size; i++)
    cout << ans[i] << " ";
  cout << "\n";

  return 0;
}
```
