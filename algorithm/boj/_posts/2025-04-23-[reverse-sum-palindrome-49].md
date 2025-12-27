---
layout: single
title: "[백준 3062] 수 뒤집기 (C#, C++) - soo:bak"
date: "2025-04-23 06:49:00 +0900"
description: 주어진 수를 뒤집어 더한 결과가 회문인지 확인하는 백준 3062번 수 뒤집기 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3062
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 문자열
  - arithmetic
keywords: "백준 3062, 백준 3062번, BOJ 3062, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3062번 - 수 뒤집기](https://www.acmicpc.net/problem/3062)

## 설명
하나의 정수를 입력받아, 그 수를 뒤집은 값과 더한 결과가 **회문(Palindrome)**인지 확인하는 문제입니다.<br><br>

회문이란 앞에서 읽으나 뒤에서 읽으나 같은 수를 의미합니다. 예를 들어 `121`, `7337` 같은 수가 회문입니다.<br><br>

이 문제에서는 여러 개의 테스트케이스가 주어지며, 각 숫자마다 다음과 같은 순서로 처리합니다:

1. 수를 문자열로 변환해 뒤집은 값을 구합니다.
2. 원래 수와 뒤집은 수를 더합니다.
3. 그 결과가 회문인지 확인하여 `"YES"` 또는 `"NO"`를 출력합니다.

## 접근법
- 정수를 문자열로 바꿔 뒤집은 값을 얻습니다.
- 문자열을 다시 정수로 바꿔 원래 수와 더합니다.
- 합계 결과를 다시 문자열로 만들어, 앞뒤가 같은지 확인합니다.


## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());

    while (t-- > 0) {
      int num = int.Parse(Console.ReadLine());
      string s = num.ToString();
      char[] revArr = s.ToCharArray();
      Array.Reverse(revArr);
      int reversed = int.Parse(new string(revArr));

      string sum = (num + reversed).ToString();
      bool isPalindrome = true;

      for (int i = 0; i < sum.Length / 2; i++) {
        if (sum[i] != sum[sum.Length - 1 - i]) {
          isPalindrome = false;
          break;
        }
      }

      Console.WriteLine(isPalindrome ? "YES" : "NO");
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
    int num; cin >> num;

    string s = to_string(num);
    string rev = s;

    reverse(rev.begin(), rev.end());

    string sum = to_string(num + stoi(rev));
    bool isPalindrome = true;
    for (size_t i = 0; i < sum.size() / 2; i++) {
      if (sum[i] != sum[sum.size() - 1 - i]) {
        isPalindrome = false;
        break;
      }
    }

    cout << (isPalindrome ? "YES\n" : "NO\n");
  }

  return 0;
}
```
