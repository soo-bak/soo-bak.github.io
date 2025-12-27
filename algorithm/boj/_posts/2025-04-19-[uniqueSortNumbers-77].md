---
layout: single
title: "[백준 10867] 중복 빼고 정렬하기 (C#, C++) - soo:bak"
date: "2025-04-19 19:03:42 +0900"
description: 입력된 정수에서 중복을 제거하고 정렬하여 출력하는 백준 10867번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10867
  - C#
  - C++
  - 알고리즘
  - 정렬
keywords: "백준 10867, 백준 10867번, BOJ 10867, uniqueSortNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10867번 - 중복 빼고 정렬하기](https://www.acmicpc.net/problem/10867)

## 설명
**입력된 정수들 중 중복을 제거하고, 오름차순으로 정렬하여 출력하는 문제**입니다.<br>
<br>

- 정수의 개수가 주어지고, 이어서 해당 개수만큼의 정수가 입력됩니다.<br>
- 이 중 **중복되는 값은 하나로 간주**하고 제거해야 합니다.<br>
- 이후 중복이 제거된 정수들을 **작은 수부터 큰 수 순으로 정렬**하여 한 줄에 출력합니다.<br>

### 접근법
- 먼저 입력된 모든 정수를 하나씩 받아 저장합니다.<br>
- 저장 과정에서 **중복을 자동으로 제거**할 수 있는 구조를 활용합니다.<br>
- 이후 저장된 정수들을 **작은 값부터 차례대로 출력**하면 됩니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var input = Console.ReadLine().Split().Select(int.Parse);
    var uniqueSorted = new SortedSet<int>(input);
    Console.WriteLine(string.Join(" ", uniqueSorted));
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef set<int> si;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  si uniqueNumbers;
  for (int i = 0; i < n; i++) {
    int num; cin >> num;
    uniqueNumbers.insert(num);
  }

  for (auto it = uniqueNumbers.begin(); it != uniqueNumbers.end(); ++it) {
    cout << *it;
    if (next(it) != uniqueNumbers.end()) cout << " ";
  }
  cout << "\n";

  return 0;
}
```
