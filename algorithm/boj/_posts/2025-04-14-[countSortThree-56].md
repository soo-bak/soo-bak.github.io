---
layout: single
title: "[백준 10989] 수 정렬하기 3 (C#, C++) - soo:bak"
date: "2025-04-14 01:55:19 +0900"
description: 입력 범위를 활용한 계수 정렬 기법으로 대량의 수를 빠르게 정렬하는 백준 10989번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10989
  - C#
  - C++
  - 알고리즘
  - 정렬
keywords: "백준 10989, 백준 10989번, BOJ 10989, countSortThree, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10989번 - 수 정렬하기 3](https://www.acmicpc.net/problem/10989)

## 설명
이 문제는 **입력으로 주어진 수의 개수가 많고**, 각 수의 **범위가 제한적(1 ~ 10,000)**일 때 효율적으로 정렬하는 방법을 묻는 문제입니다.
일반적인 정렬 알고리듬이 아닌, **계수 정렬**(Counting Sort) 기법을 이용하여 정렬 성능을 효율화할 수 있습니다.

### 접근법
- `1`부터 `10,000`까지의 수를 카운팅할 배열을 선언합니다.
- 입력을 받으며 해당 수의 등장 횟수를 카운트합니다.
- 다시 `1` 부터 순차적으로 카운트된 만큼 출력하면 정렬된 결과를 얻을 수 있습니다.

입력의 양이 많기 때문에 **입출력 속도 최적화**도 반드시 고려해야 합니다.

출력 형식은 각 수를 **하나씩 개행하여 출력**합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.IO;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      using (StreamReader sr = new(Console.OpenStandardInput()))
      using (StreamWriter sw = new(Console.OpenStandardOutput())) {
        int n = int.Parse(sr.ReadLine());
        int[] count = new int[10_001];

        for (int i = 0; i < n; i++) {
          int num = int.Parse(sr.ReadLine());
          count[num]++;
        }

        for (int i = 1; i <= 10_000; i++)
          for (int j = 0; j < count[i]; j++)
            sw.WriteLine(i);
      }
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

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n; cin >> n;

  int count[10`001] = {0, };
  for (int i = 0; i < n; i++) {
    int num; cin >> num;
    count[num]++;
  }

  for (int i = 1; i <= 10`000; i++) {
    for (int j = 0; j < count[i]; j++)
      cout << i << "\n";
  }

  return 0;
}
```
