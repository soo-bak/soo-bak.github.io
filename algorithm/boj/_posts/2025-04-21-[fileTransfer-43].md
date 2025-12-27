---
layout: single
title: "[백준 11943] 파일 옮기기 (C#, C++) - soo:bak"
date: "2025-04-21 00:42:00 +0900"
description: 바구니 간 교차 선택을 통해 사과와 오렌지를 최소 비용으로 옮기는 백준 11943번 파일 옮기기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11943
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 11943, 백준 11943번, BOJ 11943, fileTransfer, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11943번 - 파일 옮기기](https://www.acmicpc.net/problem/11943)

## 설명
**두 바구니에 사과와 오렌지가 각각 들어 있을 때,**<br>
**서로 다른 바구니에서 하나씩 골라 합이 최소가 되도록 옮기는 문제입니다.**
<br>

- 첫 번째 줄: `첫 번째 바구니`의 `사과 개수`와 `오렌지 개수`가 주어집니다.
- 두 번째 줄: `두 번째 바구니`의 `사과 개수`와 `오렌지 개수`가 주어집니다.
- 바구니에서 사과와 오렌지를 하나씩 옮겨야 하는데, **서로 다른 바구니에서 하나씩 골라야 합니다.**
- 즉, `첫 번째 바구니`의 **사과** + `두 번째 바구니`의 **오렌지** 또는<br>
  `두 번째 바구니`의 **사과** + `첫 번째 바구니`의 **오렌지** 중 **더 작은 합을 선택**해야 합니다.


## 접근법

- 두 바구니로부터 각각 (사과, 오렌지)의 값을 입력받습니다.
- 가능한 조합은 두 가지뿐이므로, 두 경우의 합을 직접 비교하여 **최소값**을 출력하면 됩니다.
- 단순한 조건 비교 문제이며, 시간 복잡도는 `O(1)`입니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var ab = Array.ConvertAll(Console.ReadLine().Split(), int.Parse);
    var cd = Array.ConvertAll(Console.ReadLine().Split(), int.Parse);

    int res = Math.Min(ab[0] + cd[1], cd[0] + ab[1]);
    Console.WriteLine(res);
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

  int cntAppleA, cntOrangeA; cin >> cntAppleA >> cntOrangeA;
  int cntAppleB, cntOrangeB; cin >> cntAppleB >> cntOrangeB;
  int ans = min(cntAppleA + cntOrangeB, cntAppleB + cntOrangeA);
  cout << ans << "\n";

  return 0;
}
```
