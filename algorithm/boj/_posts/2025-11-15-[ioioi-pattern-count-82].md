---
layout: single
title: "[백준 5525] IOIOI (C#, C++) - soo:bak"
date: "2025-11-15 02:20:00 +0900"
description: 문자열을 한 번 스캔하며 반복된 IOI 패턴을 센 뒤 PN 등장 횟수를 계산하는 백준 5525번 IOIOI 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5525
  - C#
  - C++
  - 알고리즘
  - 문자열
keywords: "백준 5525, 백준 5525번, BOJ 5525, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5525번 - IOIOI](https://www.acmicpc.net/problem/5525)

## 설명

`P_N`은 `I`로 시작하여 `OI`가 `N`번 반복되는 패턴입니다.<br>

예를 들어 `P_1 = IOI`, `P_2 = IOIOI`, `P_3 = IOIOIOI`입니다.<br>

문자열 `S`가 주어질 때, `P_N`이 `S`에 몇 번 등장하는지 구하는 문제입니다. 겹쳐서 등장하는 경우도 모두 세어야 합니다.<br>

<br>

## 접근법

문자열을 한 번만 순회하며 연속된 `IOI` 패턴의 개수를 세어 해결합니다.

문자열의 각 위치에서 `IOI` 패턴을 확인합니다.

`IOI`를 찾으면 카운트를 증가시키고 인덱스를 `2`만큼 증가시킵니다. 이렇게 하면 겹치는 부분을 효율적으로 탐색할 수 있습니다.

<br>
카운트가 `N` 이상이 되면 답을 증가시킵니다.

예를 들어 `IOIOIOI`에서는 연속된 `IOI`가 3개이므로 `P_1`이 3번, `P_2`가 2번 나타납니다.

<br>
`IOI` 패턴을 찾지 못하면 카운트를 `0`으로 초기화하고 인덱스를 `1`만큼 증가시켜 다음 위치를 탐색합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var m = int.Parse(Console.ReadLine()!);
      var s = Console.ReadLine()!;

      var answer = 0;
      var count = 0;

      for (var i = 1; i < m - 1; ) {
        if (s[i - 1] == 'I' && s[i] == 'O' && s[i + 1] == 'I') {
          count++;
          if (count >= n)
            answer++;
          i += 2;
        } else {
          count = 0;
          i++;
        }
      }

      Console.WriteLine(answer);
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

  int n, m; cin >> n >> m;
  string s; cin >> s;

  int answer = 0, count = 0;

  for (int i = 1; i < m - 1; ) {
    if (s[i - 1] == 'I' && s[i] == 'O' && s[i + 1] == 'I') {
      ++count;
      if (count >= n)
        ++answer;
      i += 2;
    } else {
      count = 0;
      ++i;
    }
  }

  cout << answer << "\n";

  return 0;
}
```

