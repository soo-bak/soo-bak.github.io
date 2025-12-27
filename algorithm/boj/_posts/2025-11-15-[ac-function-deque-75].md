---
layout: single
title: "[백준 5430] AC (C#, C++) - soo:bak"
date: "2025-11-15 00:40:00 +0900"
description: 뒤집기와 삭제 연산을 문자열로 받은 뒤 덱과 방향 플래그로 최종 배열을 계산하는 백준 5430번 AC 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5430
  - C#
  - C++
  - 알고리즘
  - deque
  - 파싱
  - 구현
  - 문자열
  - 자료구조
keywords: "백준 5430, 백준 5430번, BOJ 5430, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5430번 - AC](https://www.acmicpc.net/problem/5430)

## 설명

정수 배열에 두 가지 연산을 수행하는 문제입니다.<br>

`R`(뒤집기)은 배열의 순서를 뒤집고, `D`(버리기)는 배열의 첫 번째 원소를 제거합니다.<br>

연산이 문자열로 주어지며, 배열이 비어 있을 때 `D` 연산을 수행하려고 하면 `error`를 출력합니다. 그렇지 않으면 모든 연산을 수행한 결과를 배열 형태로 출력합니다.<br>

테스트 케이스는 최대 `100`개이고, 연산 문자열의 길이와 배열 크기는 각각 최대 `100,000`입니다.<br>

<br>

## 접근법

덱(deque)과 방향 플래그를 사용하여 효율적으로 해결합니다.

`R` 연산이 나올 때마다 배열을 실제로 뒤집으면 `O(n)` 시간이 소요되어 시간 초과가 발생합니다.

방향 플래그로 현재 배열이 뒤집힌 상태인지만 기록하고, `D` 연산 시 방향에 따라 덱의 앞 또는 뒤에서 제거합니다.

<br>
먼저 입력 문자열에서 정수를 파싱하여 덱에 저장합니다. 대괄호와 쉼표를 건너뛰고 숫자만 추출합니다.

<br>
연산 문자열을 순회하며 각 연산을 처리합니다.

`R`이 나오면 `isReverse` 플래그를 토글합니다.

`D`가 나오면 현재 방향에 따라 덱의 앞 또는 뒤에서 원소를 제거합니다. 정방향이면 `pop_front`, 역방향이면 `pop_back`을 수행합니다.

덱이 비어 있을 때 `D`가 나오면 에러 처리합니다.

<br>
모든 연산을 수행한 후, 방향 플래그에 따라 덱의 원소를 순서대로 또는 역순으로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var outputs = new List<string>(t);

      while (t-- > 0) {
        var cmd = Console.ReadLine()!;
        var n = int.Parse(Console.ReadLine()!);
        var arrayLine = Console.ReadLine()!;
        var deque = ParseDeque(arrayLine, n);

        bool isReverse = false;
        bool error = false;
        foreach (var ch in cmd) {
          if (ch == 'R') isReverse = !isReverse;
          else {
            if (deque.Count == 0) {
              error = true;
              break;
            }
            if (isReverse) deque.RemoveLast();
            else deque.RemoveFirst();
          }
        }

        outputs.Add(error ? "error" : FormatDeque(deque, isReverse));
      }

      Console.WriteLine(string.Join("\n", outputs));
    }

    static LinkedList<int> ParseDeque(string line, int n) {
      var deque = new LinkedList<int>();
      if (n == 0) return deque;
      var num = 0;
      var hasNumber = false;
      foreach (var ch in line) {
        if (char.IsDigit(ch)) {
          num = num * 10 + (ch - '0');
          hasNumber = true;
        } else if (hasNumber) {
          deque.AddLast(num);
          num = 0;
          hasNumber = false;
        }
      }
      if (hasNumber) deque.AddLast(num);
      return deque;
    }

    static string FormatDeque(LinkedList<int> deque, bool isReverse) {
      var items = isReverse ? deque.Reverse() : deque;
      return "[" + string.Join(",", items) + "]";
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

  int t; cin >> t;
  while (t--) {
    string cmd; cin >> cmd;
    int n; cin >> n;
    string arr; cin >> arr;

    deque<int> dq;
    int num = 0;
    bool inNumber = false;
    for (char ch : arr) {
      if (isdigit(ch)) {
        num = num * 10 + (ch - '0');
        inNumber = true;
      } else if (inNumber) {
        dq.push_back(num);
        num = 0;
        inNumber = false;
      }
    }

    bool reversed = false;
    bool error = false;
    for (char op : cmd) {
      if (op == 'R') reversed = !reversed;
      else {
        if (dq.empty()) {
          error = true;
          break;
        }
        if (reversed) dq.pop_back();
        else dq.pop_front();
      }
    }

    if (error) {
      cout << "error\n";
      continue;
    }

    cout << "[";
    if (!dq.empty()) {
      if (!reversed) {
        for (size_t i = 0; i < dq.size(); ++i) {
          if (i) cout << ",";
          cout << dq[i];
        }
      } else {
        for (size_t i = dq.size(); i-- > 0;) {
          cout << dq[i];
          if (i) cout << ",";
        }
      }
    }
    cout << "]\n";
  }

  return 0;
}
```

