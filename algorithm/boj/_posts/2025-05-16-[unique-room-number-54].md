---
layout: single
title: "[백준 5671] 호텔 방 번호 (C#, C++) - soo:bak"
date: "2025-05-16 20:39:00 +0900"
description: 지정된 구간 내에서 중복된 숫자가 없는 수의 개수를 구하는 백준 5671번 호텔 방 번호 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5671번 - 호텔 방 번호](https://www.acmicpc.net/problem/5671)

## 설명

**숫자에 중복이 없는 방 번호만 허용될 때, 가능한 방 번호의 개수를 구하는 문제입니다.**

두 정수 `N`, `M`이 주어지며, 구간 `[N, M]` 내에서 각 숫자에 **중복된 자릿수가 없는 수**만 세어야 합니다.

<br>
예를 들어 `838`, `1004`는 같은 숫자가 두 번 이상 나타나므로 허용되지 않으며,

`123`, `4879`는 모든 자릿수가 서로 다르므로 허용됩니다.

<br>
이러한 숫자들을 모두 찾아 개수를 출력하는 것이 목표입니다.

<br>

## 접근법

각 숫자를 문자열로 변환하여 **중복된 문자가 있는지 판별**하는 방식으로 처리할 수 있습니다.

- 숫자 `i`에 대해 문자열로 변환한 뒤, 각 자리 숫자를 방문 체크합니다.
- 방문한 적 있는 숫자가 다시 등장하면 유효하지 않은 숫자로 처리합니다.
- 모든 자릿수가 중복 없이 한 번씩만 등장하면 카운트에 포함시킵니다.

전체 범위가 최대 `5000`이므로 단순한 완전 탐색으로도 시간 제한 내에 충분히 해결할 수 있는 문제입니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static bool IsAns(int n) {
    var s = n.ToString();
    var seen = new bool[10];
    foreach (var c in s) {
      int d = c - '0';
      if (seen[d]) return false;
      seen[d] = true;
    }
    return true;
  }

  static void Main() {
    string line;
    while ((line = Console.ReadLine()) != null) {
      var parts = line.Split();
      int s = int.Parse(parts[0]);
      int e = int.Parse(parts[1]);
      int count = 0;
      for (int i = s; i <= e; i++)
        if (IsAns(i)) count++;
      Console.WriteLine(count);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

bool isAns(int n) {
  string s = to_string(n);
  bool seen[10] = {};
  for (char c : s) {
    if (seen[c - '0']) return false;
    else seen[c - '0'] = true;
  }

  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int s, e;
  while (cin >> s >> e) {
    int count = 0;
    for (int i = s; i <= e; ++i)
      if (isAns(i)) ++count;
    cout << count << "\n";
  }

  return 0;
}
```
