---
layout: single
title: "[백준 1107] 리모컨 (C#, C++) - soo:bak"
date: "2025-10-24 23:58:00 +0900"
description: 고장난 숫자 버튼을 고려해 목표 채널까지 최소 버튼 입력 횟수를 찾는 백준 1107번 리모컨 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1107번 - 리모컨](https://www.acmicpc.net/problem/1107)

## 설명

숫자 `0`부터 `9`까지와 `+`, `-` 버튼이 있는 리모컨이 있을 때,<br>

일부 숫자 버튼이 고장난 경우에 대하여 **숫자 버튼과** `+`**,** `-` **버튼을 조합해 목표 채널 `N`까지 이동하는 최소 횟수**를 구하는 문제입니다.<br>

이 때, 현재 채널은 `100`이고, `+`나 `-` 버튼은 **한 번에 채널을** `1`**씩만 이동**시킬 수 있습니다.<br>

<br>

## 접근법

가능한 모든 채널 번호 중 숫자 버튼으로 직접 만들 수 있는 후보를 찾고,<br>

해당 번호에서 `N`까지 `+`, `-`로 보정하는 횟수를 포함해 **최소 버튼 입력 수를 선택**하는 방식으로 풀이할 수 있습니다.<br>

<br>
`N`은 최대 `500,000`이므로, **숫자 버튼으로 만들 수 있는 채널을 완전 탐색**하여도 충분히 빠르게 해결할 수 있습니다.

- 우선 `|N - 100|`을 초기 답으로 설정해, 숫자 버튼을 전혀 쓰지 않는 경우를 기준으로 가정합니다.
- 채널 `0`부터 `1,000,000`까지 순회하며, 고장난 숫자가 없는지 확인해 직접 누를 수 있는 후보만 추립니다.
- 후보 채널에 대하여 `입력 자릿수 + |후보 - N|`을 계산하고, 이 값이 더 작으면 답을 갱신합니다.

<br>
숫자 버튼이 모두 고장난 특수 케이스도 포함되므로, **직접 숫자를 입력하지 않는 경우** 또한 비교해 최솟값을 선택해야 함에 주의합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    var target = tokens[0];
    var brokenCount = int.Parse(Console.ReadLine()!);

    var broken = brokenCount > 0
      ? Console.ReadLine()!.Split().Select(int.Parse).ToHashSet()
      : new HashSet<int>();

    var ans = Math.Abs(target - 100);

    int DigitCount(int value) {
      if (value == 0) return broken.Contains(0) ? 0 : 1;
      var count = 0;
      while (value > 0) {
        if (broken.Contains(value % 10)) return 0;
        value /= 10;
        count++;
      }
      return count;
    }

    foreach (var channel in Enumerable.Range(0, 1_000_001)) {
      var digits = DigitCount(channel);
      if (digits == 0) continue;
      var presses = digits + Math.Abs(channel - target);
      if (presses < ans) ans = presses;
    }

    Console.WriteLine(ans);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<bool> vb;

vb broken(10, false);

int digitCount(int num) {
  if (num == 0) return broken[0] ? 0 : 1;

  int cnt = 0;
  while (num > 0) {
    if (broken[num % 10]) return 0;
    num /= 10;
    ++cnt;
  }

  return cnt;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int target, m; cin >> target >> m;

  while (m--) {
    int digit; cin >> digit;
    broken[digit] = true;
  }

  int ans = abs(target - 100);
  for (int channel = 0; channel <= 1'000'000; ++channel) {
    int digits = digitCount(channel);
    if (!digits) continue;
    int presses = digits + abs(channel - target);
    if (presses < ans) ans = presses;
  }

  cout << ans << "\n";

  return 0;
}
```
