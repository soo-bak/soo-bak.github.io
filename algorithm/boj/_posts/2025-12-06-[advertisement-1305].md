---
layout: single
title: "[백준 1305] 광고 (C#, C++) - soo:bak"
date: "2025-12-06 12:51:00 +0900"
description: KMP의 접두사 배열로 반복 주기를 구해 가능한 광고 길이의 최솟값을 찾는 백준 1305번 광고 문제의 C#/C++ 풀이와 해설
---

## 문제 링크
[1305번 - 광고](https://www.acmicpc.net/problem/1305)

## 설명

전광판에 보이는 길이 L의 문자열이 어떤 광고 문자열을 무한 반복한 일부입니다. 가능한 광고 문자열의 최소 길이를 구하는 문제입니다.

<br>

## 접근법

광고의 최소 길이는 문자열의 최소 반복 주기와 같습니다. KMP 알고리즘의 실패 함수를 이용하면 이 주기를 효율적으로 구할 수 있습니다.

실패 함수는 각 위치에서 접두사와 접미사가 일치하는 최대 길이를 저장합니다. 전체 문자열의 마지막 위치에서 이 값이 크다면, 문자열의 앞부분과 뒷부분이 많이 겹친다는 뜻입니다.

전체 길이에서 마지막 위치의 실패 함수 값을 빼면 최소 반복 주기가 됩니다. 예를 들어 길이 6인 문자열에서 앞 4글자와 뒤 4글자가 같다면, 2글자가 반복 단위입니다.

<br>

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static int[] Prefix(string s) {
      var n = s.Length;
      var pi = new int[n];
      for (int i = 1, j = 0; i < n; i++) {
        while (j > 0 && s[i] != s[j])
          j = pi[j - 1];
        if (s[i] == s[j])
          pi[i] = ++j;
      }
      return pi;
    }

    static void Main(string[] args) {
      var L = int.Parse(Console.ReadLine()!);
      var s = Console.ReadLine()!;
      var pi = Prefix(s);
      Console.WriteLine(L - pi[L - 1]);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int L; cin >> L;
  string s; cin >> s;
  vi pi(L, 0);
  for (int i = 1, j = 0; i < L; i++) {
    while (j > 0 && s[i] != s[j])
      j = pi[j - 1];
    if (s[i] == s[j])
      pi[i] = ++j;
  }

  cout << L - pi[L - 1] << "\n";

  return 0;
}
```
