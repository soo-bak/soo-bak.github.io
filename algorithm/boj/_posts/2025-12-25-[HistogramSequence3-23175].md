---
layout: single
title: "[백준 23175] Histogram Sequence 3 (C#, C++) - soo:bak"
date: "2025-12-25 23:54:01 +0900"
description: 높이 수열에서 블록 길이를 복원해 원래 수열을 출력하는 문제
---

## 문제 링크
[23175번 - Histogram Sequence 3](https://www.acmicpc.net/problem/23175)

## 설명
주어진 높이 수열로부터 원래의 히스토그램 수열을 복원해 출력하는 문제입니다.

<br>

## 접근법
먼저 높이 수열은 같은 값이 연속된 구간들로 이루어집니다.

다음으로 각 구간의 값은 그 구간의 길이와 같으므로, 현재 위치의 값을 결과에 추가하고 그 값만큼 다음 위치로 이동합니다.

이후 끝에 도달할 때까지 위 과정을 반복하면 하나의 유효한 히스토그램 수열이 만들어집니다.

마지막으로 얻은 수열을 한 줄에 출력합니다.

<br>

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
    var m = int.Parse(parts[idx++]);
    var b = new int[m];
    for (var i = 0; i < m; i++) b[i] = int.Parse(parts[idx++]);

    var sb = new StringBuilder();
    for (var i = 0; i < m;) {
      var v = b[i];
      sb.Append(v).Append(' ');
      i += v;
    }

    if (sb.Length > 0) sb.Length--;
    Console.WriteLine(sb);
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

  int m; cin >> m;
  vector<int> b(m);
  for (int i = 0; i < m; i++) cin >> b[i];

  bool first = true;
  for (int i = 0; i < m;) {
    int v = b[i];
    if (!first) cout << ' ';
    cout << v;
    first = false;
    i += v;
  }
  cout << "\n";

  return 0;
}
```
