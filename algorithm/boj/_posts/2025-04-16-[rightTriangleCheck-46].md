---
layout: single
title: "[백준 7510] 고급 수학 (C#, C++) - soo:bak"
date: "2025-04-16 02:11:00 +0900"
description: 주어진 세 변을 통해 직각삼각형 여부를 판별하고 시나리오 별로 결과를 출력하는 백준 7510번 고급 수학 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[7510번 - 고급 수학](https://www.acmicpc.net/problem/7510)

## 설명
**세 변의 길이를 통해 직각삼각형인지 판별하고, 각 테스트케이스마다 결과를 출력하는 문제**입니다.<br>
<br>

- 여러 개의 테스트케이스가 주어지고, 각 케이스마다 `3`개의 정수(세 변의 길이)를 입력받습니다.<br>
- 주어진 세 변을 정렬한 후, 피타고라스 정리를 이용해<br>
  $$a^2 + b^2 = c^2$$<br>
  가 성립하는지를 확인하면 됩니다 (`a`, `b`, `c`는 정렬된 순서 기준).<br>
<br>

### 접근법
- 테스트케이스 수를 입력받습니다.<br>
- 각 케이스마다 세 변을 배열에 저장하고 정렬한 뒤, 가장 긴 변의 제곱이 나머지 두 변 제곱의 합과 같은지 비교합니다.<br>
- 조건이 성립하면 `"yes"`, 아니면 `"no"`를 출력합니다.<br>
- 각 케이스는 `"Scenario #x:"` 형식으로 번호를 출력하고, 테스트케이스 사이에는 빈 줄을 출력합니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine());
    for (int i = 1; i <= t; i++) {
      var side = Console.ReadLine().Split().Select(long.Parse).ToArray();
      Array.Sort(side);
      Console.WriteLine($"Scenario #{i}:");
      Console.WriteLine(
        side[0] * side[0] + side[1] * side[1] == side[2] * side[2]
        ? "yes" : "no"
      );
      if (i != t) Console.WriteLine();
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;

  int cnt = 1;
  while (t--) {
    ll side[3];
    for (int i = 0; i < 3; i++)
      cin >> side[i];

    sort(side, side + 3);

    cout << "Scenario #" << cnt << ":\n";

    if (side[0] * side[0] + side[1] * side[1] == side[2] * side[2])
      cout << "yes\n";
    else cout << "no\n";
    cnt++;
    if (t != 0) cout << "\n";
  }

  return 0;
}
```
