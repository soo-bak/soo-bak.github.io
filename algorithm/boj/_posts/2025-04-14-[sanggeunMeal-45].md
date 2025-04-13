---
layout: single
title: "[백준 5543] 상근날드 (C#, C++) - soo:bak"
date: "2025-04-14 03:42:50 +0900"
description: 가장 저렴한 세트 메뉴 가격을 계산하는 백준 5543번 상근날드 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[5543번 - 상근날드](https://www.acmicpc.net/problem/5543)

## 설명
이 문제는 햄버거 3종류, 음료 2종류의 가격이 주어졌을 때,
**햄버거 1개와 음료 1개를 선택했을 때 가장 저렴한 세트 가격을 계산**하는 문제입니다.
단, 세트 주문 시 **50원이 할인**됩니다.

---

## 접근법
- 햄버거 `3`개 중 가장 싼 가격을 찾습니다.
- 음료 `2`개 중 가장 싼 가격을 찾습니다.
- 이 둘을 더한 후, `50`원을 할인해 출력합니다.

단순한 **최솟값 계산 문제**입니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var bgr = int.MaxValue;
      for (int i = 0; i < 3; i++) {
        var n = int.Parse(Console.ReadLine()!);
        if (n < bgr) bgr = n;
      }

      var bvg = int.MaxValue;
      for (int i = 0; i < 2; i++) {
        var n = int.Parse(Console.ReadLine()!);
        if (n < bvg) bvg = n;
      }

      Console.WriteLine(bgr + bvg - 50);
    }
  }
}
```

<br><br>
<b>[ C++ ] </b>
<br>

```cpp
#include <iostream>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int bgr, bvg = 2'000;
  for (int i = 0; i < 3; i++) {
    int input; cin >> input;
    if (input < bgr) bgr = input;
  }
  for (int i = 0; i < 2; i++) {
    int input; cin >> input;
    if (input < bvg) bvg = input;
  }
  cout << bgr + bvg - 50 << "\n";
  return 0;
}
```
