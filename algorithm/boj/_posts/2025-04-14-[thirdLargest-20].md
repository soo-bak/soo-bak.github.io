---
layout: single
title: "[백준 2693] N번째 큰 수 (C#, C++) - soo:bak"
date: "2025-04-14 06:20:02 +0900"
description: 정렬을 통해 배열에서 3번째로 큰 수를 추출하는 백준 2693번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[2693번 - N번째 큰 수](https://www.acmicpc.net/problem/2693)

## 설명
이 문제는 각 테스트 케이스에서 `10`**개의 정수 중** `3`**번째로 큰 수를 출력**하는 문제입니다. <br>

입력은 여러 테스트 케이스로 구성되어 있으며, 각 케이스는 `10`개의 정수로 이루어져 있습니다.

---

## 접근법
- `10`개의 정수를 입력받아 배열에 저장합니다.
- 내림차순 정렬을 수행한 뒤, 인덱스 `2`번째 값을 출력합니다 (즉, 3번째로 큰 수).
- 단순한 정렬 기반 문제입니다.

---

## Code
<b>[ C# ] </b>
<br>

```csharp
using System;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      int t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var arr = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
        Array.Sort(arr);
        Console.WriteLine(arr[7]);
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
    int arr[10];
    for (int i = 0; i < 10; i++)
      cin >> arr[i];

    sort(arr, arr + 10);

    cout << arr[7] << "\n";
  }

  return 0;
}
```
