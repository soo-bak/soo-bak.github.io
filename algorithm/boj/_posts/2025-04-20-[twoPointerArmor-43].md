---
layout: single
title: "[백준 1940] 주몽 (C#, C++) - soo:bak"
date: "2025-04-20 22:44:00 +0900"
description: 투 포인터 알고리즘을 이용해 재료쌍의 합이 주어진 수가 되도록 하는 경우의 수를 계산하는 백준 1940번 주몽 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1940
  - C#
  - C++
  - 알고리즘
  - 정렬
  - 투포인터
keywords: "백준 1940, 백준 1940번, BOJ 1940, twoPointerArmor, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1940번 - 주몽](https://www.acmicpc.net/problem/1940)

## 설명
**재료 번호 목록이 주어졌을 때, 두 개를 골라 더한 값이 특정 값이 되도록 하는 쌍의 개수를 세는 문제입니다.**
<br>

- 첫 줄에는 재료의 수, 두 번째 줄에는 만들고자 하는 갑옷 번호(목표 합)가 주어집니다.
- 다음 줄에 재료들의 고유 번호가 주어지며, 이 중에서 두 개를 골라 그 합이 목표 수가 되면 유효한 조합으로 간주합니다.
- 조건을 만족하는 서로 다른 쌍의 수를 구해야 하며, 같은 조합은 한 번만 셉니다.


## 접근법

- 입력받은 재료 번호들을 먼저 오름차순으로 정렬합니다.
- 투 포인터 기법을 활용하여 양 끝에서 시작합니다:
  - 두 수의 합이 목표보다 작으면 시작 포인터를 증가
  - 크면 끝 포인터를 감소
  - 같으면 조합 수 증가 후 양쪽 포인터 이동
- 모든 쌍을 체크할 때까지 이 과정을 반복합니다.
- 정렬과 투 포인터 기반의 접근으로 시간 복잡도는 `O(n log n)(정렬) + O(n)(탐색)` 입니다.

> 참고 : [투 포인터 알고리듬(Two Pointer Algorithm)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/two-pointer-explained/)

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    int m = int.Parse(Console.ReadLine());
    var arr = Console.ReadLine().Split().Select(int.Parse).ToArray();
    Array.Sort(arr);

    int count = 0, left = 0, right = arr.Length - 1;
    while (left < right) {
      int sum = arr[left] + arr[right];
      if (sum == m) {
        count++;
        left++; right--;
      } else if (sum < m) left++;
      else right--;
    }
    Console.WriteLine(count);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntMat, combNum; cin >> cntMat >> combNum;
  vi matNum(cntMat);
  for (int i = 0; i < cntMat; i++)
    cin >> matNum[i];

  sort(matNum.begin(), matNum.end());

  int cntComb = 0;
  int idxS = 0, idxE = matNum.size() - 1;
  while (idxS < idxE) {
    int sumMat = matNum[idxS] + matNum[idxE];
    if (sumMat == combNum) {
      cntComb++;
      idxS++;
      idxE--;
    }
    else if (sumMat < combNum) idxS++;
    else if (sumMat > combNum) idxE--;
  }

  cout << cntComb << "\n";

  return 0;
}
```
