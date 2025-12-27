---
layout: single
title: "[백준 1271] 엄청난 부자2 (C#, C++) - soo:bak"
date: "2025-11-21 23:50:00 +0900"
description: 거대한 정수 n을 생명체 수 m으로 나눈 몫과 나머지를 출력하는 백준 1271번 엄청난 부자2 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1271
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
  - arbitrary_precision
keywords: "백준 1271, 백준 1271번, BOJ 1271, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1271번 - 엄청난 부자2](https://www.acmicpc.net/problem/1271)

## 설명

두 개의 정수 `n`과 `m`이 주어집니다. `n`과 `m`은 최대 `1000`자리까지의 매우 큰 정수입니다.<br>

`n`을 `m`으로 나눈 몫과 나머지를 각각 출력하는 문제입니다.<br>

<br>

## 접근법

일반적인 정수 자료형으로는 최대 `1000`자리 수를 처리할 수 없으므로 큰 정수를 다룰 수 있는 방법이 필요합니다.<br>

C#에서는 `System.Numerics.BigInteger`를 사용하여 큰 정수의 나눗셈을 간단히 처리할 수 있습니다.

`n / m`으로 몫을, `n % m`으로 나머지를 구합니다.<br>

C++에서는 표준 라이브러리에 큰 정수 자료형이 없으므로 문자열 기반의 나눗셈 알고리즘을 직접 구현합니다.

입력을 문자열로 받아 한 자리씩 나누는 방식으로 몫과 나머지를 계산합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Numerics;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var n = BigInteger.Parse(tokens[0]);
      var m = BigInteger.Parse(tokens[1]);

      Console.WriteLine(n / m);
      Console.WriteLine(n % m);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef pair<string, string> pss;

string trimLeadingZeros(const string& s) {
  size_t pos = s.find_first_not_of('0');
  return (pos == string::npos) ? "0" : s.substr(pos);
}

int compareStrings(const string& a, const string& b) {
  string x = trimLeadingZeros(a), y = trimLeadingZeros(b);

  if (x.size() != y.size()) return x.size() < y.size() ? -1 : 1;
  if (x == y) return 0;

  return x < y ? -1 : 1;
}

string multiplyByDigit(const string& s, int digit) {
  if (digit == 0) return "0";

  int carry = 0;
  string result;

  for (int i = (int)s.size() - 1; i >= 0; --i) {
    int val = (s[i] - '0') * digit + carry;
    result.push_back(char('0' + (val % 10)));
    carry = val / 10;
  }

  if (carry) result.push_back(char('0' + carry));

  reverse(result.begin(), result.end());
  return trimLeadingZeros(result);
}

string subtractStrings(string a, const string& b) {
  int carry = 0;
  string result;
  int i = (int)a.size() - 1, j = (int)b.size() - 1;

  while (i >= 0) {
    int av = a[i] - '0' - carry;
    int bv = (j >= 0) ? b[j] - '0' : 0;

    if (av < bv)
      av += 10, carry = 1;
    else
      carry = 0;

    result.push_back(char('0' + (av - bv)));
    --i; --j;
  }

  while (result.size() > 1 && result.back() == '0') result.pop_back();

  reverse(result.begin(), result.end());
  return trimLeadingZeros(result);
}

pss divideStrings(const string& num, const string& den) {
  string quotient, remainder = "0";

  for (char ch : num) {
    if (remainder == "0") remainder.clear();
    remainder.push_back(ch);
    remainder = trimLeadingZeros(remainder);

    int digit = 0;
    if (compareStrings(remainder, den) >= 0) {
      for (int d = 9; d >= 1; --d) {
        string product = multiplyByDigit(den, d);
        if (compareStrings(remainder, product) >= 0) {
          digit = d;
          remainder = subtractStrings(remainder, product);
          break;
        }
      }
    }

    quotient.push_back(char('0' + digit));
  }

  quotient = trimLeadingZeros(quotient);
  remainder = trimLeadingZeros(remainder);

  return {quotient, remainder};
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string n, m; cin >> n >> m;

  auto [quotient, remainder] = divideStrings(n, m);
  cout << quotient << "\n" << remainder << "\n";

  return 0;
}
```
