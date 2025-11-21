---
layout: single
title: "[백준 5554] 심부름 가는 길 (C#, C++) - soo:bak"
date: "2025-04-20 03:27:00 +0900"
description: 4개의 구간에 걸쳐 소요된 시간(초)을 입력받아 총 시간을 분과 초로 환산하여 출력하는 백준 5554번 심부름 가는 길 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[5554번 - 심부름 가는 길](https://www.acmicpc.net/problem/5554)

## 설명
**총**`4`**개의 이동 구간에 대해 각각의 소요 시간을 초 단위로 입력받아,**<br>
**총 소요 시간을 분과 초로 나누어 출력하는 문제입니다.**<br>
<br>

- 각 줄에는 `4`개의 각 이동 구간에서 소요된 시간이 초 단위로 주어집니다.
- 이 네 개의 값을 모두 더한 뒤, 총합을 `분`과 `초`로 환산하여 출력합니다.


## 접근법

1. 네 개의 줄에 걸쳐 각 구간의 시간(초)을 입력받습니다.
2. 입력받은 시간들을 모두 더합니다.
3. 총합을 `60`으로 나누어 `몫`은 `분`, `나머지`는 `초`로 출력합니다.

- 시간 단위 변환의 기본 개념을 확인할 수 있는 단순 구현 문제입니다.


## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int total = 0;
    for (int i = 0; i < 4; i++)
      total += int.Parse(Console.ReadLine());

    Console.WriteLine(total / 60);
    Console.WriteLine(total % 60);
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

  int sumSec = 0;
  for (int i = 0; i < 4; i++) {
    int sec; cin >> sec;
    sumSec += sec;
  }
  cout << sumSec / 60 << "\n" << sumSec % 60 << "\n";

  return 0;
}
```
