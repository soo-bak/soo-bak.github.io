---
layout: single
title: "[백준 5522] 카드 게임 (C#, C++) - soo:bak"
date: "2025-04-14 21:07:53 +0900"
description: 5번의 점수를 입력받아 총합을 출력하는 단순 합산 문제 백준 5522번 카드 게임의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[5522번 - 카드 게임](https://www.acmicpc.net/problem/5522)

## 설명
이 문제는 **5번의 점수를 입력받아 총합을 출력하는 간단한 문제**입니다.  <br>
<br>
각 점수는 자연수이며, 조건 없이 그대로 더해서 출력하면 됩니다.

---

## 접근법
- 입력은 총 `5`번 주어지며, 각 줄마다 점수 하나를 입력받습니다.
- 모든 점수를 누적하여 총합을 계산합니다.
- 반복이 끝난 후 누적된 값을 그대로 출력하면 됩니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      long sum = 0;
      for (int i = 0; i < 5; i++)
        sum += long.Parse(Console.ReadLine()!);
      Console.WriteLine(sum);
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

  ll sum = 0;
  for (int i = 0; i < 5; i++) {
    ll score; cin >> score;
    sum += score;
  }

  cout << sum << "\n";

  return 0;
}
```
