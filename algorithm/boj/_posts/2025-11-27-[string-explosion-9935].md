---
layout: single
title: "[백준 9935] 문자열 폭발 (C#, C++) - soo:bak"
date: "2025-11-27 00:50:00 +0900"
description: 스택을 사용하여 문자를 추가하며 폭발 문자열을 즉시 제거하는 방식으로 O(N) 시간에 처리하는 백준 9935번 문자열 폭발 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 9935
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 문자열
  - 스택
keywords: "백준 9935, 백준 9935번, BOJ 9935, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9935번 - 문자열 폭발](https://www.acmicpc.net/problem/9935)

## 설명

문자열에서 폭발 문자열을 발견하면 제거하고, 제거 후 다시 폭발 문자열이 생기면 더 이상 없을 때까지 반복해서 제거하는 상황에서 원본 문자열과 폭발 문자열이 주어질 때, 모든 폭발이 끝난 후 남은 문자열을 구하는 문제입니다.

원본 문자열의 길이는 최대 1,000,000이고, 폭발 문자열의 길이는 최대 36입니다.

남은 문자열이 없으면 `FRULA`를 출력합니다.

<br>

## 접근법

문자열을 처음부터 끝까지 반복하며 제거하면 매번 O(N²) 시간이 걸리므로, 스택을 사용하여 한 번의 순회로 모든 폭발을 처리합니다.

원본 문자열의 각 문자를 왼쪽부터 순서대로 스택에 추가하고, 스택에 쌓인 문자의 개수가 폭발 문자열 길이 이상이면 스택의 끝부분과 폭발 문자열을 비교합니다.

일치하면 폭발 문자열 길이만큼 스택에서 제거하고, 일치하지 않으면 다음 문자를 계속 추가합니다.

<br>
이 방식으로 제거 후 앞뒤 문자가 자동으로 연결되어 새로운 폭발 문자열이 생기더라도 다음 순회에서 확인되므로, O(N) 시간에 모든 폭발을 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var s = Console.ReadLine()!;
      var bomb = Console.ReadLine()!;
      var blen = bomb.Length;

      var stack = new StringBuilder();

      foreach (var ch in s) {
        stack.Append(ch);

        if (stack.Length >= blen) {
          var match = true;

          for (var i = 0; i < blen; i++)
            if (stack[stack.Length - blen + i] != bomb[i]) {
              match = false;
              break;
            }

          if (match) stack.Length -= blen;
        }
      }

      if (stack.Length == 0) Console.WriteLine("FRULA");
      else Console.WriteLine(stack.ToString());
    }
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

  string s, bomb; cin >> s >> bomb;
  int blen = bomb.size();

  string st;
  st.reserve(s.size());

  for (char ch : s) {
    st.push_back(ch);

    if ((int)st.size() >= blen) {
      bool match = true;

      for (int i = 0; i < blen; i++)
        if (st[st.size() - blen + i] != bomb[i]) {
          match = false;
          break;
        }

      if (match) st.erase(st.end() - blen, st.end());
    }
  }

  if (st.empty()) cout << "FRULA\n";
  else cout << st << "\n";

  return 0;
}
```

