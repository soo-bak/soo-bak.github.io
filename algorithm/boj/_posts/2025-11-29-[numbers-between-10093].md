---
layout: single
title: "[백준 10093] 숫자 (C#, C++) - soo:bak"
date: "2025-11-29 12:45:00 +0900"
description: 두 수의 대소를 비교한 후 사이에 있는 정수의 개수와 오름차순 목록을 구하는 백준 10093번 숫자 문제의 C# 및 C++ 풀이
---

## 문제 링크
[10093번 - 숫자](https://www.acmicpc.net/problem/10093)

## 설명

두 정수가 주어지는 상황에서, A와 B (1 ≤ A, B ≤ 10^15)가 주어질 때, 그 사이에 있는 정수의 개수와 오름차순 목록을 구하는 문제입니다.

두 수의 차이는 최대 100,000이며, 두 수가 같을 경우 사이에 있는 정수는 없습니다.

<br>

## 접근법

두 수가 어떤 순서로 주어지든, 먼저 작은 수와 큰 수를 구분해야 합니다.

사이에 있는 정수의 개수는 큰 수와 작은 수의 차이에서 1을 뺀 값입니다.

<br>
예를 들어, 3과 10이 주어진다면:
- 사이에 있는 수: 4, 5, 6, 7, 8, 9
- 개수: 10 - 3 - 1 = 6개

다른 예로, 100과 105가 주어진다면:
- 사이에 있는 수: 101, 102, 103, 104
- 개수: 105 - 100 - 1 = 4개

<br>
두 수가 같거나 연속된 경우 사이에 있는 수가 없습니다:
- 5와 5 사이: 없음 (0개)
- 10과 11 사이: 없음 (0개)

<br>
사이에 있는 정수가 없다면 개수만 출력하고, 있다면 개수를 출력한 후 작은 수 다음부터 큰 수 직전까지 순서대로 나열합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split();
      long a = long.Parse(input[0]);
      long b = long.Parse(input[1]);
      if (a > b) (a, b) = (b, a);

      long cnt = Math.Max(0, b - a - 1);
      var sb = new StringBuilder();
      sb.Append(cnt).Append('\n');
      if (cnt > 0) {
        for (long num = a + 1; num < b; num++) {
          sb.Append(num);
          if (num + 1 < b) sb.Append(' ');
        }
        sb.Append('\n');
      }
      Console.Write(sb);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b; cin >> a >> b;
  if (a > b) swap(a, b);

  ll cnt = max(0LL, b - a - 1);
  cout << cnt << '\n';
  if (cnt == 0) return 0;
  for (ll num = a + 1; num < b; num++) {
    cout << num << (num + 1 < b ? ' ' : '\n');
  }
  return 0;
}
```
