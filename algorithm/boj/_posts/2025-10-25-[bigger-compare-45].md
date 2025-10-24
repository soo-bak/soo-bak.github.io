---
layout: single
title: "[백준 4101] 크냐? (C#, C++) - soo:bak"
date: "2025-10-25 00:05:00 +0900"
description: 두 양의 정수를 비교해 더 큰 수가 첫 번째인지 판별하는 백준 4101번 크냐? 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[4101번 - 크냐?](https://www.acmicpc.net/problem/4101)

## 설명

두 양의 정수가 주어졌을 때, **첫 번째 정수가 두 번째 정수보다 큰지**를 판별해 `Yes` 또는 `No`로 출력하는 문제입니다.<br>

입력은 여러 테스트 케이스로 구성되며, 마지막 줄에 `0 0`이 들어오면 입력이 종료됩니다.<br>

각 정수는 `1,000,000` 이하이기 때문에, 단순 비교만으로 충분히 빠르게 해결할 수 있습니다.<br>

<br>

## 접근법

입력을 한 줄씩 확인하면서, 종료 조건이 나올 때까지 비교 결과를 출력합니다.

- `0 0`이 입력되면 반복을 종료합니다.
- 첫 번째 수가 더 큰 경우 `Yes`, 두 번째 수가 더 큰 경우 `No`를 출력합니다.

<br>
입력 크기가 작고 조건도 단순하므로, **정확한 종료 조건 처리**만 주의하면 됩니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    while (true) {
      var numbers = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var first = numbers[0];
      var second = numbers[1];
      if (first == 0 && second == 0) break;
      Console.WriteLine(first > second ? "Yes" : "No");
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

  while (true) {
    int a, b; cin >> a >> b;
    if (!a && !b) break;
    cout << (a > b ? "Yes" : "No") << "\n";
  }

  return 0;
}
```

