---
layout: single
title: "[백준 10807] 개수 세기 (C#, C++) - soo:bak"
date: "2025-04-16 01:57:00 +0900"
description: 배열 내에서 특정 정수의 개수를 세는 단순 카운팅 문제인 백준 10807번 개수 세기 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[10807번 - 개수 세기](https://www.acmicpc.net/problem/10807)

## 설명
**정수 배열에서 특정한 값이 몇 번 등장했는지를 세는 간단한 구현 문제**입니다.<br>
<br>

- 정수의 개수가 주어지고, 그 다음 줄에 정수들이 공백으로 나열됩니다.<br>
- 마지막 줄에는 찾고자 하는 값이 주어집니다.<br>
- 이 값이 배열에 몇 번 등장하는지를 출력하면 됩니다.<br>

### 접근법
- 입력으로 주어진 수들을 배열에 저장하고, 특정 값의 등장 횟수를 셉니다.<br>
- 값의 범위가 `-100`부터 `100`까지로 제한되어 있으므로, <br>
  음수를 포함한 값을 양의 범위로 바꾸어 배열에 저장하는 방식으로 해결할 수 있습니다.<br>

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var nums = Console.ReadLine().Split().Select(int.Parse).ToArray();
    int target = int.Parse(Console.ReadLine());
    Console.WriteLine(nums.Count(x => x == target));
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int sieve[202] = {0, };
  int n; cin >> n;
  for (int i = 0; i < n; i++) {
    int num; cin >> num;
    sieve[num + 100]++;
  }
  int tar; cin >> tar;
  cout << sieve[tar + 100] << "\n";

  return 0;
}
```
