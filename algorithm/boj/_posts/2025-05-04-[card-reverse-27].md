---
layout: single
title: "[백준 10804] 카드 역배치 (C#, C++) - soo:bak"
date: "2025-05-04 19:08:21 +0900"
description: 주어진 구간의 카드를 반복적으로 뒤집는 시뮬레이션 문제, 백준 10804번 카드 역배치 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10804번 - 카드 역배치](https://www.acmicpc.net/problem/10804)

## 설명
`1`부터 `20`까지 순서대로 놓인 카드들에 대해 **총 10번에 걸쳐 특정 구간 [a, b]를 선택하여 해당 부분을 뒤집는 작업을 반복한 뒤**,

최종 카드 상태를 출력하는 시뮬레이션 문제입니다.

<br>
각 구간의 시작과 끝은 항상 `1 ≤ a ≤ b ≤ 20`을 만족하며,

각 작업은 입력 순서대로 적용됩니다.

<br>

## 접근법

- 먼저 카드 배열을 `1`부터 `20`까지 초기화합니다.
- `10`번 반복하여 시작 위치와 끝 위치를 입력받습니다.
- 각 구간이 주어질 때마다, 해당 범위 내의 카드 순서를 현재 순서의 반대가 되도록 뒤집습니다.
- 반복이 모두 끝나면, 카드 배열을 공백 구분자로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var cards = Enumerable.Range(1, 20).ToList();

    for (int i = 0; i < 10; i++) {
      var input = Console.ReadLine().Split().Select(int.Parse).ToArray();
      int a = input[0] - 1, b = input[1] - 1;
      cards.Reverse(a, b - a + 1);
    }

    Console.WriteLine(string.Join(" ", cards));
  }
}
```

<br>

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int card[20];
  for (int i = 0; i < 20; i++)
    card[i] = i + 1;

  for (int i = 0; i < 10; i++) {
    int idxB, idxE; cin >> idxB >> idxE;
    reverse(&card[idxB - 1], &card[idxE]);
  }

  for (int i = 0; i < 20; i++) {
    cout << card[i];
    if (i != 19) cout << " ";
    else cout << "\n";
  }

  return 0;
}
```
