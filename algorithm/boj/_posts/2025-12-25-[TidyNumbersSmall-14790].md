---
layout: single
title: "[백준 14790] Tidy Numbers (Small) (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 14790번 C#, C++ 풀이 - 마지막 tidy 수를 찾아 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 14790
  - C#
  - C++
  - 알고리즘
keywords: "백준 14790, 백준 14790번, BOJ 14790, TidyNumbersSmall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14790번 - Tidy Numbers (Small)](https://www.acmicpc.net/problem/14790)

## 설명
주어진 수 이하에서 자리수가 왼쪽부터 내려가지 않는 가장 큰 수를 구하는 문제입니다.

<br>

## 접근법
왼쪽에서 오른쪽으로 볼 때 내려가는 지점이 있으면 그 앞자리를 하나 줄이고, 그 뒤는 모두 9로 만드는 것이 가장 큽니다.  
이 과정에서 더 왼쪽에서도 내려감이 생길 수 있으므로, 오른쪽에서 왼쪽으로 확인하며 같은 처리를 반복합니다.  
마지막에 앞의 0을 제거하면 답이 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();

    for (var caseNo = 1; caseNo <= t; caseNo++) {
      var s = Console.ReadLine()!.Trim();
      var arr = s.ToCharArray();
      var n = arr.Length;

      for (var i = n - 1; i > 0; i--) {
        if (arr[i] < arr[i - 1]) {
          arr[i - 1]--;
          for (var j = i; j < n; j++)
            arr[j] = '9';
        }
      }

      var start = 0;
      while (start < n - 1 && arr[start] == '0') start++;
      var result = new string(arr, start, n - start);

      sb.AppendLine($"Case #{caseNo}: {result}");
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
  for (int caseNo = 1; caseNo <= t; caseNo++) {
    string s; cin >> s;
    int n = (int)s.size();

    for (int i = n - 1; i > 0; i--) {
      if (s[i] < s[i - 1]) {
        s[i - 1]--;
        for (int j = i; j < n; j++)
          s[j] = '9';
      }
    }

    int start = 0;
    while (start < n - 1 && s[start] == '0') start++;
    string result = s.substr(start);

    cout << "Case #" << caseNo << ": " << result << "\n";
  }

  return 0;
}
```
