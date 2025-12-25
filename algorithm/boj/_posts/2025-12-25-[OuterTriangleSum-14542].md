---
layout: single
title: "[백준 14542] Outer Triangle Sum (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 삼각형 외곽에 있는 수들의 합을 구하는 백준 14542번 Outer Triangle Sum 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[14542번 - Outer Triangle Sum](https://www.acmicpc.net/problem/14542)

## 설명
이등변 직각삼각형 모양으로 채워진 수들에서 외곽에 있는 수들의 합을 구하는 문제입니다.

<br>

## 접근법
삼각형을 2차원 배열에 저장한 뒤, 외곽을 세 부분으로 나눠서 더합니다.

왼쪽 변은 각 행의 첫 번째 원소, 밑변은 마지막 행의 두 번째부터 마지막 원소, 오른쪽 대각선 변은 중간 행들의 마지막 원소입니다.

이렇게 하면 중복 없이 외곽의 모든 수를 더할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var lines = Console.In.ReadToEnd().Split('\n');
    var lineIdx = 0;
    var caseNo = 0;
    var sb = new StringBuilder();

    while (lineIdx < lines.Length) {
      var n = int.Parse(lines[lineIdx++].Trim());
      if (n == 0) break;

      caseNo++;
      var nums = new int[n][];
      for (var j = 0; j < n; j++) {
        var parts = lines[lineIdx++].Trim().Split();
        nums[j] = new int[j + 1];
        for (var k = 0; k <= j; k++)
          nums[j][k] = int.Parse(parts[k]);
      }

      var ans = 0;
      for (var j = 0; j < n; j++)
        ans += nums[j][0];

      for (var j = 1; j < n; j++)
        ans += nums[n - 1][j];

      for (var k = n - 2; k > 0; k--)
        ans += nums[k][k];

      sb.AppendLine($"Case #{caseNo}:{ans}");
    }

    Console.Write(sb);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int i = 0;
  while (true) {
    int n; cin >> n;
    if (!n) break;

    i++;
    vvi nums(n, vi(n, 0));
    int ans = 0;

    cin.ignore();
    for (int j = 0; j < n; j++) {
      string line; getline(cin, line);
      stringstream ss(line);
      int k = 0, tmp;
      while (ss >> tmp && k < n) {
        nums[j][k] = tmp;
        k++;
      }
    }

    for (int j = 0; j < n; j++)
      ans += nums[j][0];

    for (int j = 1; j < n; j++)
      ans += nums[n - 1][j];

    for (int k = n - 2; k > 0; k--)
      ans += nums[k][k];

    cout << "Case #" << i << ":" << ans << "\n";
  }

  return 0;
}
```
