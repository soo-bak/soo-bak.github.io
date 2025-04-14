---
layout: single
title: "[백준 10178] 할로윈의 사탕 (C#, C++) - soo:bak"
date: "2025-04-14 21:07:53 +0900"
description: 사탕을 친구들과 나눈 뒤 남은 개수를 계산하는 백준 10178번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[10178번 - 할로윈의 사탕](https://www.acmicpc.net/problem/10178)

## 설명
**전체 사탕 개수와 친구 수**가 주어졌을 때,  <br>
<br>
사탕을 친구들에게 균등하게 나눈 후 **한 사람당 가져가는 사탕 수**와 <br>
<br>
**남은 사탕 개수**를 구하는 단순한 몫과 나머지 계산 문제입니다.

---

## 접근법
- 테스트할 횟수를 먼저 입력받습니다.
- 각 테스트 케이스마다:
  - 사탕의 전체 개수와 나눌 친구 수를 입력받고,
  - 한 명당 받는 사탕 수는 `전체 수 / 친구 수`,
  - 남는 사탕은 `전체 수 % 친구 수`로 계산합니다.
- 결과는 지정된 출력 형식에 맞춰 출력합니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var input = Console.ReadLine()!.Split();
        int c = int.Parse(input[0]);
        int v = int.Parse(input[1]);
        Console.WriteLine($"You get {c / v} piece(s) and your dad gets {c % v} piece(s).");
      }
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int cntC, cntS; cin >> cntC >> cntS;
    cout << "You get " << cntC / cntS << " piece(s) and your dad gets ";
    cout << cntC % cntS << " piece(s).\n";
  }

  return 0;
}
```
