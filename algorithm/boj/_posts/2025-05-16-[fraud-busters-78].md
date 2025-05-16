---
layout: single
title: "[백준 9584] Fraud Busters (C#, C++) - soo:bak"
date: "2025-05-16 21:00:00 +0900"
description: 차량 번호판 일부가 가려진 상태에서 가능한 모든 일치 코드를 필터링하는 백준 9584번 Fraud Busters 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[9584번 - Fraud Busters](https://www.acmicpc.net/problem/9584)

## 설명

**일부 문자가 가려진 차량 번호판과 비교 가능한 후보 리스트가 주어질 때, 일치하는 차량 번호를 찾아내는 문제입니다.**

- 차량 번호판은 항상 `9자리 문자열`로 구성되며, `알파벳 대문자` 또는 `숫자`입`니다.
- 인식된 번호판에는 `*` 문자가 포함될 수 있으며, 이 위치는 아무 문자나 허용되는 **와일드카드**로 취급합니다.
- 이 인식된 패턴과 완전히 일치할 수 있는 모든 등록 차량 번호를 찾아내야 합니다.

<br>
예를 들어, 인식된 번호판이 `A**00P19*`라면:
- `1`, `2`, `8`번째 위치는 어떤 문자든 무관하며,
- 나머지 위치는 정확히 일치해야 합니다.

<br>

## 접근법

이 문제는 단순한 문자열 비교 문제이지만, **일부 위치를 무시하는 조건부 비교**가 필요합니다.

전체 흐름은 다음과 같습니다:

1. 인식된 번호판의 각 문자 위치를 순회하며,
2. `*`가 아닌 위치의 문자 인덱스를 따로 저장해둡니다.
3. 이후 후보군 각각에 대해, 인식된 번호판과 일치하는지를 비교합니다.
   - 단, 비교는 `*`가 아닌 위치만 확인하면 됩니다.
   - 모든 유효 위치에서 일치한다면 해당 후보를 결과로 기록합니다.
4. 최종적으로 일치한 후보 수와 함께 정렬 순서 없이 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static void Main() {
    string plate = Console.ReadLine();
    var valid = new List<int>();
    for (int i = 0; i < plate.Length; i++) {
      if (plate[i] != '*') valid.Add(i);
    }

    int n = int.Parse(Console.ReadLine());
    var result = new List<string>();
    for (int i = 0; i < n; i++) {
      string candidate = Console.ReadLine();
      bool match = true;
      foreach (int idx in valid) {
        if (plate[idx] != candidate[idx]) {
          match = false;
          break;
        }
      }
      if (match) result.Add(candidate);
    }

    Console.WriteLine(result.Count);
    foreach (var s in result)
      Console.WriteLine(s);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string plate; cin >> plate;

  vi valid;
  for (size_t i = 0; i < plate.size(); ++i) {
    if (plate[i] != '*')
      valid.push_back((int)i);
  }

  int n; cin >> n;
  vs matches;
  while (n--) {
    string s; cin >> s;

    bool ok = true;
    for (size_t i : valid)
      if (plate[i] != s[i]) {
        ok = false;
        break;
      }

    if (ok) matches.push_back(s);
  }

  cout << matches.size() << "\n";
  for (const auto& s : matches)
    cout << s << "\n";

  return 0;
}
```
