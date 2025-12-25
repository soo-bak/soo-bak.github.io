---
layout: single
title: "[백준 18158] What an Easy Problem (C#, C++) - soo:bak"
date: "2025-12-25 23:40:59 +0900"
description: 심리전 발언에 맞춰 항상 지는 손을 반환하는 함수 구현 문제
---

## 문제 링크
[18158번 - What an Easy Problem](https://www.acmicpc.net/problem/18158)

## 설명
교준이의 심리전 발언에 따라 실제로 내는 손이 달라질 때, 매번 지는 손을 선택하는 함수를 구현하는 문제입니다.

<br>

## 접근법
먼저 심리전 발언에 따라 실제로 내는 손이 어떻게 바뀌는지 정리합니다.

다음으로 세 경우를 비교하면, 우리가 져야 하는 손은 항상 발언한 손과 같음을 알 수 있습니다.

이후 각 라운드에서 발언한 손과 같은 손을 내도록 반환하면 됩니다.

마지막으로 함수 구현 문제이므로 추가 입출력 없이 제공된 함수만 작성합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

public static class Program {
  public static void init(int T) {
  }

  public static int janken(int P) {
    return P;
  }
}
```

### C++
```cpp
#include "WAEP.h"

void init(int T) {
}

int janken(int P) {
  return P;
}
```
