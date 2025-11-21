---
layout: single
title: "[백준 15740] A+B - 9 (C#, C++) - soo:bak"
date: "2025-11-21 23:59:00 +0900"
description: ±10^1,000,000 범위의 큰 정수 A와 B를 더하는 백준 15740번 A+B - 9 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[15740번 - A+B - 9](https://www.acmicpc.net/problem/15740)

## 설명

`A`와 `B`는 ±10¹⁰⁰⁰⁰⁰⁰까지 가능한 큰 정수입니다.  
따라서 문자열 기반 큰 정수 덧셈을 직접 구현해야 합니다.

<br>

## 접근법

- C#은 `BigInteger`로 바로 처리합니다.
- C++은 문자열로 입력받아 부호와 절댓값을 분리하고, 절댓값 덧셈/뺄셈을 직접 구현해 결과를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Numerics;

class Program {
  static void Main() {
    var tokens = Console.ReadLine()!.Split();
    BigInteger a = BigInteger.Parse(tokens[0]);
    BigInteger b = BigInteger.Parse(tokens[1]);
    Console.WriteLine(a + b);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string trimZero(const string& s) {
  size_t pos = s.find_first_not_of('0');
  return (pos == string::npos) ? "0" : s.substr(pos);
}

int compareAbs(const string& a, const string& b) {
  string x = trimZero(a);
  string y = trimZero(b);
  if (x.size() != y.size()) return x.size() < y.size() ? -1 : 1;
  if (x == y) return 0;
  return x < y ? -1 : 1;
}

string addAbs(const string& a, const string& b) {
  string result;
  int carry = 0, i = a.size() - 1, j = b.size() - 1;
  while (i >= 0 || j >= 0 || carry) {
    int sum = carry;
    if (i >= 0) sum += a[i--] - '0';
    if (j >= 0) sum += b[j--] - '0';
    result.push_back(char('0' + (sum % 10)));
    carry = sum / 10;
  }
  reverse(result.begin(), result.end());
  return trimZero(result);
}

string subAbs(const string& a, const string& b) { // assume |a| >= |b|
  string result;
  int borrow = 0, i = a.size() - 1, j = b.size() - 1;
  while (i >= 0) {
    int diff = (a[i] - '0') - borrow;
    if (j >= 0) diff -= (b[j] - '0');
    if (diff < 0) {
      diff += 10;
      borrow = 1;
    } else borrow = 0;
    result.push_back(char('0' + diff));
    --i; --j;
  }
  while (result.size() > 1 && result.back() == '0') result.pop_back();
  reverse(result.begin(), result.end());
  return trimZero(result);
}

string addSigned(const string& a, const string& b) {
  int signA = (a[0] == '-') ? -1 : 1;
  int signB = (b[0] == '-') ? -1 : 1;
  string absA = (signA == -1) ? a.substr(1) : a;
  string absB = (signB == -1) ? b.substr(1) : b;
  absA = trimZero(absA);
  absB = trimZero(absB);

  if (absA == "0") signA = 1;
  if (absB == "0") signB = 1;

  if (signA == signB) {
    string sum = addAbs(absA, absB);
    if (sum == "0") return "0";
    return (signA == -1 ? "-" : "") + sum;
  } else {
    int cmp = compareAbs(absA, absB);
    if (cmp == 0) return "0";
    bool absAGreater = (cmp > 0);
    string diff = absAGreater ? subAbs(absA, absB) : subAbs(absB, absA);
    int sign = absAGreater ? signA : signB;
    if (diff == "0") return "0";
    return (sign == -1 ? "-" : "") + diff;
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string A, B;
  cin >> A >> B;
  cout << addSigned(A, B) << "\n";
  return 0;
}
```

