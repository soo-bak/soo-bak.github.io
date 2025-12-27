---
layout: single
title: "[백준 1037] 약수 (C#, C++) - soo:bak"
date: "2025-04-14 02:58:39 +0900"
description: 진약수의 개념과 활용을 통해 원래의 수를 계산하는 백준 1037번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1037
  - C#
  - C++
  - 알고리즘
  - 수학
  - 정수론
keywords: "백준 1037, 백준 1037번, BOJ 1037, divisorProduct, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1037번 - 약수](https://www.acmicpc.net/problem/1037)

## 설명
이 문제는 어떤 수 `N`의 **진약수 목록**이 주어졌을 때, 원래의 수 `N`을 구하는 문제입니다.

### 진약수란?
진약수는 어떤 자연수의 **자기 자신을 제외한 약수**를 의미합니다. 즉, 1부터 `N-1`까지의 수 중에서 `N`을 나누어 떨어지게 만드는 수들이 진약수입니다.
예를 들어, `12`의 약수는 `1, 2, 3, 4, 6, 12`이며, 이 중 `1`과 `12`를 제외한 `2, 3, 4, 6`이 진약수입니다.

---

## 접근법
- 입력으로 주어지는 수들은 모두 진약수입니다.
- 진약수는 짝을 이룹니다. 가장 작은 값과 가장 큰 값을 곱하면 원래의 수 `N`이 됩니다.
- 예를 들어 진약수가 `2, 4, 8`이면, `2 * 8 = 16`이 원래 수가 됩니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
namespace Solution {
  class Program {
    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      var arr = Console.ReadLine()!.Split().Select(long.Parse).ToArray();

      Array.Sort(arr);
      Console.WriteLine(arr[0] * arr[^1]);
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

typedef long long ll;
typedef vector<ll> vll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  vll v;
  for (int i = 0; i < t; i++) {
    ll num; cin >> num;
    v.push_back(num);
  }

  sort(v.begin(), v.end());

  cout << v.front() * v.back() << "\n";

  return 0;
}
```
