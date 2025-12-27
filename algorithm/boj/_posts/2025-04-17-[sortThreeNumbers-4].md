---
layout: single
title: "[백준 2752] 세수정렬 (C#, C++) - soo:bak"
date: "2025-04-17 00:01:00 +0900"
description: 주어진 세 수를 오름차순으로 정렬하여 출력하는 백준 2752번 세수정렬 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2752
  - C#
  - C++
  - 알고리즘
keywords: "백준 2752, 백준 2752번, BOJ 2752, sortThreeNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2752번 - 세수정렬](https://www.acmicpc.net/problem/2752)

## 설명
**주어진 세 개의 정수를 오름차순으로 정렬하여 출력하는 문제**입니다.<br>
<br>

- 입력으로 공백으로 구분된 세 개의 정수가 주어집니다.<br>
- 이를 오름차순으로 정렬한 후 공백으로 구분하여 출력합니다.<br>
- 가장 기본적인 정렬 문제로, 정렬 알고리즘 또는 내장 함수를 이용하면 쉽게 해결할 수 있습니다.<br>

### 접근법
- 입력된 세 수를 배열이나 리스트에 저장합니다.<br>
- 정렬 함수를 이용해 오름차순으로 정렬합니다.<br>
- 정렬된 세 수를 순서대로 출력합니다.<br>

> 참고 : [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var nums = Console.ReadLine().Split().Select(int.Parse).ToList();
    nums.Sort();
    Console.WriteLine(string.Join(" ", nums));
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi arr(3);
  for (int i = 0; i < 3; i++)
    cin >> arr[i];

  sort(arr.begin(), arr.end());

  for (int i = 0; i < 3; i++)
    cout << arr[i] << " ";
  cout << "\n";

  return 0;
}
```
