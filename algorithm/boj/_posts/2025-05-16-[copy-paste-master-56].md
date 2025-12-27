---
layout: single
title: "[백준 11008] 복붙의 달인 (C#, C++) - soo:bak"
date: "2025-05-16 21:57:00 +0900"
description: 복사한 문자열을 활용해 전체 문자열을 최소 시간으로 입력하는 백준 11008번 복붙의 달인 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11008
  - C#
  - C++
  - 알고리즘
keywords: "백준 11008, 백준 11008번, BOJ 11008, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11008번 - 복붙의 달인](https://www.acmicpc.net/problem/11008)

## 설명

**긴 문자열을 작성할 때, 복사한 문자열을 활용하여 최소 시간으로 타이핑을 완료하는 문제입니다.**

기본적으로 `한 문자`를 입력하는 데는 `1초`가 걸리지만,

미리 복사해둔 문자열 `p`는 **전체 문자열을 한 번 붙여넣을 때 1초만에** 입력이 가능합니다.

따라서, 문자열 `s`를 입력할 때, `p`가 등장하는 위치마다 붙여넣기를 사용하면 해당 부분을 빠르게 입력할 수 있습니다.

<br>
예를 들어 `banana`를 입력할 때, `bana`를 복사해두었다면:<br>
- `"bana"`를 붙여넣는 데 `1초`
- 나머지 `"na"`는 개별 타이핑으로 `1초`씩 → 총 `3초`

<br>

## 접근법

전체 문자열 `s`에서 복사`한 문자`열 `p`가 등`장하`는 구간들을 찾아,

**겹치지 않게** 최대한 많이 붙여넣기를 적용하는 것이 핵심입니다.

<br>
이때 탐색 방식은 다음과 같습니다:

- 왼쪽부터 `s`에서 `p`가 시작되는 위치를 탐색합니다.
- 찾은 위치에서는 문자열 `p`의 길이만큼 이동해 다음 탐색을 이어갑니다.
- 이렇게 하면 `p`가 중복 없이 최대한 많이 적용됩니다.
- 나머지 부분은 하나씩 타이핑해야 하므로, 전체 길이에서 `p`로 이루어진 영역을 제외한 문자의 개수를 계산합니다.

최종 시간은 다음과 같이 계산됩니다:

$$
\text{복붙 횟수} + (\text{s.length} - \text{복붙 횟수} \times \text{p.length})
$$

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split();
      string s = tokens[0], p = tokens[1];

      int pos = 0, count = 0;
      while ((pos = s.IndexOf(p, pos)) != -1) {
        count++;
        pos += p.Length;
      }

      int result = count + (s.Length - count * p.Length);
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

  int t; cin >> t;
  while (t--) {
    string s, p; cin >> s >> p;

    int time = 0;
    size_t pos = 0;
    while ((pos = s.find(p, pos)) != string::npos) {
      pos += p.length();
      ++time;
    }

    time += s.length() - time * p.length();

    cout << time << "\n";
  }

  return 0;
}
```
