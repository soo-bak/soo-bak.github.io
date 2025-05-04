---
layout: single
title: "[백준 11948] 과목선택 (C#, C++) - soo:bak"
date: "2025-05-04 17:19:00 +0900"
description: 주어진 6과목 점수 중 과학 계열 4과목에서 3과목, 인문 계열 2과목에서 1과목을 선택해 최대 점수 합을 계산하는 백준 11948번 과목선택 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[11948번 - 과목선택](https://www.acmicpc.net/problem/11948)

## 설명
총 `6과목`의 시험 점수가 주어질 때,

**과학 계열 4과목 중 3과목**과 **인문 계열 2과목 중 1과목**을 선택하여,

**점수의 합이 가장 높도록 선택한 후 그 합을 출력하는 문제**입니다.

<br>

## 접근법

- 먼저 총 `6과목`의 점수를 차례대로 입력받습니다.
  - 앞의 4줄은 물리, 화학, 생물, 지구과학의 점수로 과학 계열입니다.
  - 뒤의 2줄은 역사와 지리의 점수로 인문 계열입니다.
- 과학 계열 4과목 중에서는 점수가 **가장 낮은 한 과목을 제외한 3과목의 합**을 구합니다.
- 인문 계열 2과목 중에서는 **점수가 더 높은 과목 1개만 선택**합니다.
- 이 둘을 더한 값이 선택할 수 있는 최고 점수이며, 해당 값을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var science = new int[4];
    for (int i = 0; i < 4; i++)
      science[i] = int.Parse(Console.ReadLine());

    var social = new int[2];
    for (int i = 0; i < 2; i++)
      social[i] = int.Parse(Console.ReadLine());

    int sumScience = science.Sum() - science.Min();
    int maxSocial = social.Max();

    Console.WriteLine(sumScience + maxSocial);
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

  int a[4], b[2], ans = 0;
  for (int i = 0; i < 4; i++) cin >> a[i], ans += a[i];
  ans -= *min_element(a, a + 4);
  for (int i = 0; i < 2; i++) cin >> b[i], ans += b[i];
  ans -= *min_element(b, b + 2);

  cout << ans << "\n";

  return 0;
}
```
