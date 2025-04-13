---
layout: single
title: "[백준 11098] 첼시를 도와줘! (C#, C++) - soo:bak"
date: "2025-04-14 05:12:47 +0900"
description: 각 테스트 케이스마다 가장 높은 금액을 제시한 선수를 찾아 출력하는 백준 11098번 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[11098번 - 첼시를 도와줘!](https://www.acmicpc.net/problem/11098)

## 설명
이 문제는 여러 테스트 케이스에 대해 각 선수들의 제시 금액과 이름을 입력받고,  <br>
**가장 높은 금액을 제시한 선수의 이름을 출력하는 문제**입니다.

---

## 접근법
- 테스트 케이스마다 제시된 선수의 정보 `(금액, 이름)`을 입력받습니다.
- 금액이 가장 큰 선수를 갱신하면서 기록합니다.
- 모든 선수를 확인한 뒤 가장 높은 금액의 선수를 출력합니다.

입력 수가 많지 않기 때문에 단순 비교로도 충분히 해결할 수 있는 문제입니다.

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
        int n = int.Parse(Console.ReadLine()!);
        long max = -1;
        string maxName = "";

        for (int i = 0; i < n; i++) {
          var parts = Console.ReadLine()!.Split();
          long bid = long.Parse(parts[0]);
          string name = parts[1];
          if (bid > max) {
            max = bid;
            maxName = name;
          }
        }

        Console.WriteLine(maxName);
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
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int numC; cin >> numC;

    ll maxVal = -1; string maxStr;
    for (int i = 0; i < numC; i++) {
      ll val; string str; cin >> val >> str;
      if (val > maxVal) {
        maxVal = val;
        maxStr = str;
      }
    }

    cout << maxStr << "\n";
  }

  return 0;
}
```
