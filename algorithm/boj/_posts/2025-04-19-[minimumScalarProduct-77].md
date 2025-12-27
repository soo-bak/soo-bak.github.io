---
layout: single
title: "[백준 1026] 보물 (C#, C++) - soo:bak"
date: "2025-04-19 19:00:42 +0900"
description: 정렬을 통해 최소 곱의 합을 만드는 백준 1026번 보물 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1026
  - C#
  - C++
  - 알고리즘
keywords: "백준 1026, 백준 1026번, BOJ 1026, minimumScalarProduct, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1026번 - 보물](https://www.acmicpc.net/problem/1026)

## 설명
**두 개의 정수 수열에서 각 원소를 곱한 합이 최소가 되도록 만드는 문제**입니다.<br>
<br>

- 두 수열의 길이는 동일하며, 각각 정수로 구성되어 있습니다.<br>
- 각 위치에서의 곱을 더한 값, 즉<br>
  $$\sum_{i=0}^{n-1} A_i \times B_i$$<br>
  의 결과가 **최소**가 되도록 수열을 재배열해야 합니다.<br>
- 수열 $A$는 순서를 바꿀 수 없고, 수열 $B$만 재배열이 가능합니다.<br>

### 접근법
- 곱의 총합을 최소로 만들기 위해서는, 수열 $A$의 **작은 수**에 수열 $B$의 **큰 수**를 곱해야 합니다.<br>
- 따라서 수열 $A$는 오름차순으로 정렬하고, 수열 $B$는 내림차순으로 정렬합니다.<br>
- 두 수열을 앞에서부터 순서대로 곱한 뒤, 그 결과를 누적하여 합산합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int len = int.Parse(Console.ReadLine());
    var arrA = Console.ReadLine().Split().Select(int.Parse).ToArray();
    var arrB = Console.ReadLine().Split().Select(int.Parse).ToArray();

    Array.Sort(arrA);
    Array.Sort(arrB);
    Array.Reverse(arrB);

    int sum = 0;
    for (int i = 0; i < len; i++)
      sum += arrA[i] * arrB[i];

    Console.WriteLine(sum);
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

  int len; cin >> len;

  vi arrA(len), arrB(len);
  for (int i = 0; i < len; i++)
    cin >> arrA[i];
  for (int i = 0; i < len; i++)
    cin >> arrB[i];

  sort(arrA.begin(), arrA.end());
  sort(arrB.rbegin(), arrB.rend());

  int sum = 0;
  for (int i = 0; i < len; i++)
    sum += arrA[i] * arrB[i];
  cout << sum << "\n";

  return 0;
}
```
