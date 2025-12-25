---
layout: single
title: "[백준 20953] 고고학자 예린 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 삼중 반복문의 카운트 결과를 수식으로 계산하는 문제
---

## 문제 링크
[20953번 - 고고학자 예린](https://www.acmicpc.net/problem/20953)

## 설명
주어진 함수 dolmen(a, b)가 반환하는 값을 계산하는 문제입니다.

<br>

## 접근법
내부 루프는 j에 대해 0부터 j-1까지 반복되므로 횟수는 j입니다.  
이를 정리하면 전체 합은 n × n × (n - 1) / 2가 되며, n은 a + b입니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = int.Parse(parts[idx++]);

    var sb = new StringBuilder();
    for (var i = 0; i < t; i++) {
      var a = int.Parse(parts[idx++]);
      var b = int.Parse(parts[idx++]);
      var n = a + b;
      var ans = n * n * (n - 1) / 2;
      sb.AppendLine(ans.ToString());
    }

    Console.Write(sb);
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

  int t; cin >> t;
  while (t--) {
    int a, b; cin >> a >> b;
    int n = a + b;
    int ans = n * n * (n - 1) / 2;
    cout << ans << "\n";
  }

  return 0;
}
```
