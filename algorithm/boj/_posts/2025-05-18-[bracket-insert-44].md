---
layout: single
title: "[백준 11899] 괄호 끼워넣기 (C#, C++) - soo:bak"
date: "2025-05-18 02:31:00 +0900"
description: 최소한의 괄호를 추가하여 올바른 괄호열을 만드는 백준 11899번 괄호 끼워넣기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11899
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 문자열
  - 스택
keywords: "백준 11899, 백준 11899번, BOJ 11899, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11899번 - 괄호 끼워넣기](https://www.acmicpc.net/problem/11899)

## 설명

**주어진 괄호열을 올바른 괄호열로 만들기 위해 앞이나 뒤에 추가해야 할 괄호의 최소 개수를 구하는 문제입니다.**

괄호열은 여는 괄호 `(`와 닫는 괄호 `)`로만 이루어져 있으며,

올바른 괄호열은 다음 조건을 만족하는 구조입니다:

- 어느 위치에서든 여는 괄호의 개수가 닫는 괄호의 개수보다 작아지지 않아야 하고,
- 전체적으로 여는 괄호와 닫는 괄호의 개수가 같아야 합니다.

<br>

## 접근법

문자열을 왼쪽에서 오른쪽으로 순차적으로 확인하면서,

**현재까지 닫히지 않은 여는 괄호의 개수**를 추적하며 균형을 맞춥니다.

- 여는 괄호를 만나면 현재 열린 상태로 저장해둘 수 있으므로 개수를 하나 증가시킵니다.
- 닫는 괄호를 만났을 때:
  - 남아 있는 여는 괄호가 있다면 짝을 이룰 수 있으므로 여는 괄호 개수를 하나 줄입니다.
  - 여는 괄호가 없으면, 앞쪽에 여는 괄호가 부족하다는 의미이므로<br>
    추가해야 할 여는 괄호 개수를 하나 증가시킵니다.

문자열을 모두 처리한 이후 남아 있는 여는 괄호는 짝을 이루지 못한 것이므로,

**그만큼 닫는 괄호를 뒤에 붙여야 완전한 괄호열**이 됩니다.

최종적으로, 앞에서 추가해야 했던 여는 괄호 수와 남아 있는 여는 괄호 수를 더한 값이 정답이 됩니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string s = Console.ReadLine();
    int ans = 0, open = 0;

    foreach (char c in s) {
      if (c == '(') open++;
      else if (open == 0) ans++;
      else open--;
    }

    ans += open;
    Console.WriteLine(ans);
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

  string s; cin >> s;
  int ans = 0, open = 0;
  for (char c : s) {
    if (c == '(') ++open;
    else if (open == 0) ++ans;
    else --open;
  }

  ans += open;

  cout << ans << "\n";

  return 0;
}
```
