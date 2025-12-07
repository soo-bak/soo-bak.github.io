---
layout: single
title: "[백준 2331] 반복수열 (C#, C++) - soo:bak"
date: "2025-12-07 04:15:00 +0900"
description: 각 자릿수의 P제곱 합으로 수열을 만들어 반복 전 원소 개수를 구하는 백준 2331번 반복수열 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[2331번 - 반복수열](https://www.acmicpc.net/problem/2331)

## 설명
첫째 항 A가 주어지고, 다음 항은 이전 항의 각 자릿수를 P제곱하여 더한 값입니다. 이렇게 수열을 만들면 언젠가 이전에 나온 값이 다시 등장하여 반복이 시작됩니다. 반복되는 부분을 제외한 원소의 개수를 구하는 문제입니다.

<br>

## 접근법
각 값이 몇 번 등장했는지 기록하는 배열을 사용합니다. 수열을 따라가다가 이전에 등장한 값이 다시 나오면 반복이 시작됩니다. 예를 들어 57, 74, 65, 61, 37, 58, ..., 16, 37에서 37이 두 번째로 등장하면 반복 구간의 시작입니다.

반복 구간의 원소들은 최소 두 번 등장하고, 반복 이전 원소들은 정확히 한 번만 등장합니다. 따라서 같은 값이 세 번째로 등장하면 반복 구간을 한 바퀴 더 돈 것이므로 탐색을 종료합니다.

탐색이 끝나면 정확히 한 번만 등장한 원소의 개수가 반복되는 부분을 제외한 수열의 길이입니다.

<br>

- - -

## Code

### C#

```csharp
using System;

class Program {
  const int MAX = 300001;
  static int p;
  static int[] cache = new int[MAX];

  static void Solve(int d) {
    cache[d]++;
    if (cache[d] == 3) return;
    var sum = 0;
    while (d > 0) {
      sum += (int)Math.Pow(d % 10, p);
      d /= 10;
    }
    Solve(sum);
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    p = int.Parse(parts[1]);
    Solve(a);

    var ret = 0;
    for (var i = 0; i < MAX; i++)
      if (cache[i] == 1) ret++;
    Console.WriteLine(ret);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAX = 300001;
int p, cache[MAX] = {0, };

void solve(int d) {
  cache[d]++;
  if (cache[d] == 3) return;
  int sum = 0;
  while (d > 0) {
    sum += (int)pow(d % 10, p);
    d /= 10;
  }
  solve(sum);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int a; cin >> a >> p;
  solve(a);

  int ret = 0;
  for (int i = 0; i < MAX; i++)
    if (cache[i] == 1) ret++;
  cout << ret << "\n";

  return 0;
}
```
