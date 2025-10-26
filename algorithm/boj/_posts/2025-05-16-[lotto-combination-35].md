---
layout: single
title: "[백준 6603] 로또 (C#, C++) - soo:bak"
date: "2025-05-16 21:53:00 +0900"
description: 오름차순 집합에서 6개의 수를 선택하는 모든 조합을 구하는 백준 6603번 로또 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[6603번 - 로또](https://www.acmicpc.net/problem/6603)

## 설명

**주어진 수열에서** `6개`**의 수를 선택하는 모든 조합을 사전순으로 출력**하는 조합 생성 문제입니다.

입력은 여러 개의 테스트케이스로 이루어져 있으며,

각 줄마다 첫 번째 숫자는 집합의 크기 `k`입니다.

이후 `k`개의 오름차순 정수가 주어지며, 이에 대해 다음과 같은 작업을 수행해야 합니다:

- 조건: `6 < k < 13`
- 출력: 이 집합에서 `6개`**를 선택하는 모든 조합을 사전순으로 출력**

각 테스트케이스 사이에는 **빈 줄 한 줄**을 출력해야 하며,

입력이 `0`인 경우 과정을 종료합니다.

<br>

## 접근법

이 문제는 전형적인 **백트래킹 기반의 조합 생성** 문제로 다음 방식으로 해결할 수 있습니다.

<br>
입력으로 주어진 수열은 오름차순으로 정렬되어 있으므로,

앞에서부터 차례대로 수를 선택해 나가면서 `6개`의 수를 고르면 하나의 조합이 완성됩니다.

<br>
이때, 이미 선택한 수보다 앞에 있는 숫자는 다시 고를 필요가 없기 때문에,

현재 위치 이후의 수만을 대상으로 다음 수를 선택하는 방식으로 탐색을 이어갑니다.

<br>
이런 방식으로 깊이를 하나씩 늘려가며 선택한 수가 정확히 `6개`가 되었을 때, 그때의 조합을 출력하면 됩니다.

<br>
결국 이 과정은 조합을 사전순으로 생성하는 백트래킹 과정이며,

불필요한 중복 없이 모든 가능한 조합을 생성할 수 있는 구조입니다.

<br>

> 참고 : [백트래킹(Backtracking)의 개념과 구조적 사고 - soo:bak](https://soo-bak.github.io/algorithm/theory/backTracking/)

> 참고 : [조합(Combination)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/combination/)

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Backtrack(List<int> nums, List<int> comb, int pos) {
    if (comb.Count == 6) {
      Console.WriteLine(string.Join(" ", comb));
      return;
    }
    for (int i = pos; i < nums.Count; i++) {
      comb.Add(nums[i]);
      Backtrack(nums, comb, i + 1);
      comb.RemoveAt(comb.Count - 1);
    }
  }

  static void Main() {
    string line;
    while ((line = Console.ReadLine()) != "0") {
      var parts = Array.ConvertAll(line.Split(), int.Parse);
      var nums = new List<int>(parts[1..]);
      Backtrack(nums, new List<int>(), 0);
      Console.WriteLine();
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

void backtrack(vi& nums, vi& comb, int pos) {
  if (comb.size() == 6) {
    for (int i = 0; i < 6; ++i)
      cout << comb[i] << (i < 5 ? " " : "\n");
    return;
  }

  for (int i = pos; i < nums.size(); ++i) {
    comb.push_back(nums[i]);
    backtrack(nums, comb, i + 1);
    comb.pop_back();
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    int k; cin >> k;
    if (!k) break;

    vi nums(k);
    for (int& x : nums)
      cin >> x;

    vi comb;
    backtrack(nums, comb, 0);

    cout << "\n";
    cin.ignore();
  }

  return 0;
}
```
