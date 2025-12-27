---
layout: single
title: "[백준 2903] 중앙 이동 알고리즘 (C++, C#) - soo:bak"
date: "2025-05-18 19:31:00 +0900"
description: 점의 수가 제곱 형태로 증가하는 원리를 수식으로 계산하는 백준 2903번 중앙 이동 알고리즘 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2903
  - C#
  - C++
  - 알고리즘
  - 수학
keywords: "백준 2903, 백준 2903번, BOJ 2903, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2903번 - 중앙 이동 알고리즘](https://www.acmicpc.net/problem/2903)

## 설명

**정사각형 점** `4개`**에서 시작하여, 중앙과 변 중간에 점을 추가하는 방식으로 점의 수를 확장하는 문제입니다.**

<br>
점의 추가 방식은 다음과 같습니다:

- 각 변의 중간에 점을 하나씩 추가하여, 변의 개수를 두 배로 만듭니다.
- 중심에도 점을 하나 추가하므로, 전체적으로 정사각형 안의 격자 수가 커지는 구조입니다.

이 과정을 `N`번 반복했을 때 최종적으로 생기는 점의 총 개수를 구해야 합니다.

<br>

## 접근법

처음 상태에서 한 변에는 점이 `2`개 존재합니다.

이후 매 반복마다 각 변의 점 개수가 다음과 같이 증가합니다:

- 한 번 반복할 때마다, 기존 각 구간의 **중간 지점에 점이 추가되므로** 길이가 두 배가 됩니다.
- 따라서 `i`번째 단계에서 한 변에 있는 점의 수는 다음과 같은 등비 수열을 따릅니다:

$$
\text{한 변의 점 수} = 2 + (2^{1} + 2^{2} + \cdots + 2^{N-1}) = 2 + \sum_{i=1}^{N} 2^{i-1}
$$

<br>
이는 결국 다음과 같이 정리됩니다:

$$
\text{한 변의 점 수} = 2^{N} + 1
$$

<br>
따라서, 최종 점의 개수는 다음과 같이 계산할 수 있습니다:

$$
\text{총 점의 수} = (2^{N} + 1)^2
$$

<br>

이 수식을 직접 구현하면, 반복문의 사용 없이도 효율적으로 정답을 구할 수 있습니다.

---

## Code

### C#
```csharp
namespace Solution {
  class Program {
    static void Main(string[] args) {
      int n = int.Parse(Console.ReadLine());
      var result = (int)Math.Pow(Math.Pow(2, n) + 1, 2);
      Console.WriteLine(result);
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
  cout << (int)pow((pow(2, n) + 1), 2) << "\n";

  return 0;
}
```
