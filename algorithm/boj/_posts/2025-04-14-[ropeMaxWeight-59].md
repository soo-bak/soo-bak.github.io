---
layout: single
title: "[백준 2217] 로프 (C#, C++) - soo:bak"
date: "2025-04-14 03:01:39 +0900"
description: 여러 개의 로프를 선택하여 들어올릴 수 있는 최대 중량을 계산하는 백준 2217번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2217
  - C#
  - C++
  - 알고리즘
  - 수학
  - 그리디
  - 정렬
keywords: "백준 2217, 백준 2217번, BOJ 2217, ropeMaxWeight, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2217번 - 로프](https://www.acmicpc.net/problem/2217)

## 설명
이 문제는 여러 개의 로프를 이용해 **들어올릴 수 있는 최대 중량**을 계산하는 문제입니다.
로프는 각각 버틸 수 있는 최대 중량이 다르며, 여러 개의 로프를 병렬로 사용하면 **각 로프에는 동일한 중량이 걸립니다**.

### 조건 정리
- 총 `N`개의 로프가 주어집니다.
- 로프를 몇 개 선택하여 물체를 들어올릴 수 있습니다.
- 이때 선택한 로프들 중 **가장 약한 로프의 중량**에 **사용한 로프 수**를 곱한 값이 총 들어올릴 수 있는 중량입니다.
- 가능한 조합 중에서 가장 큰 값을 출력합니다.

---

## 접근법
- 로프의 중량을 저장한 뒤, **오름차순으로 정렬**합니다.
- 가장 약한 로프부터 하나씩 포함시키면서 최대 중량을 계산합니다:
  - 예를 들어, 정렬된 배열에서 `i`번째 로프를 사용할 경우 남은 로프 수는 `N - i`
  - 최대 중량은 `rope[i] * (N - i)`
- 이 값을 매 반복마다 갱신하여 **최댓값을 추적**합니다.

<br>
> 참고 : [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)

<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var ropes = new int[n];
      for (int i = 0; i < n; i++) {
        ropes[i] = int.Parse(Console.ReadLine()!);
      }

      Array.Sort(ropes);
      var max = 0;
      for (int i = 0; i < n; i++) {
        var w = ropes[i] * (n - i);
        if (w > max) max = w;
      }

      Console.WriteLine(max);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>
#define MAX 10'001

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntR[MAX]; fill_n(cntR, MAX, 0);
  int n; cin >> n;
  for (int i = 0; i < n; i++) {
    int r; cin >> r;
    cntR[r]++;
  }

  int maxW = 0, cnt = 0;
  for (int i = MAX - 1; i >= 1; i--) {
    cnt += cntR[i];
    int w = i * cnt;
    if (maxW < w) maxW = w;
  }

  cout << maxW << "\n";

  return 0;
}
```
