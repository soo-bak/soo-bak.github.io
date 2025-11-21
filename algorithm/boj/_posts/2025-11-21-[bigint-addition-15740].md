---
layout: single
title: "[백준 15740] A+B - 9 (C#, C++) - soo:bak"
date: "2025-11-22 01:59:00 +0900"
description: ±10^1,000,000 범위의 큰 정수 A와 B를 더하는 백준 15740번 A+B - 9 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[15740번 - A+B - 9](https://www.acmicpc.net/problem/15740)

## 설명

두 정수 `A`와 `B`가 주어질 때, 두 수의 합 `A + B`를 출력하는 문제입니다.

각 정수는 최대 1,000,000자리의 양의 정수 또는 음의 정수가 가능하므로, 일반적인 정수 타입으로는 표현할 수 없습니다.

따라서 임의 정밀도 산술이 필요합니다.

<br>

## 접근법

C#의 경우 `System.Numerics.BigInteger` 타입을 사용하면 큰 수 덧셈을 직접 처리할 수 있습니다.

입력을 `BigInteger`로 파싱한 후 덧셈 연산자를 사용하여 결과를 계산합니다.

<br>
C++의 경우 큰 수 연산을 문자열 기반으로 직접 구현해야 합니다.

입력을 문자열로 받아 부호와 절댓값을 분리합니다.

두 수의 부호가 같으면 절댓값을 더하고 같은 부호를 붙입니다.

두 수의 부호가 다르면 절댓값 크기를 비교하여 큰 쪽에서 작은 쪽을 빼고, 절댓값이 더 큰 쪽의 부호를 결과에 붙입니다.

<br>
절댓값 덧셈은 낮은 자릿수부터 더하며 올림을 처리합니다.

절댓값 뺄셈은 큰 수에서 작은 수를 빼되 받아내림을 처리합니다.

모든 연산을 마친 후 앞자리 0을 제거하며, 결과가 0이면 부호를 붙이지 않습니다.

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
      var a = BigInteger.Parse(tokens[0]);
      var b = BigInteger.Parse(tokens[1]);

      Console.WriteLine(a + b);
    }
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
  string x = trimZero(a), y = trimZero(b);

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

string subAbs(const string& a, const string& b) {
  string result;
  int borrow = 0, i = a.size() - 1, j = b.size() - 1;

  while (i >= 0) {
    int diff = (a[i] - '0') - borrow;
    if (j >= 0) diff -= (b[j] - '0');

    if (diff < 0)
      diff += 10, borrow = 1;
    else
      borrow = 0;

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
  absA = trimZero(absA), absB = trimZero(absB);

  if (absA == "0") signA = 1;
  if (absB == "0") signB = 1;

  if (signA == signB) {
    string sum = addAbs(absA, absB);
    if (sum == "0") return "0";
    return (signA == -1 ? "-" : "") + sum;
  }

  int cmp = compareAbs(absA, absB);
  if (cmp == 0) return "0";

  bool absAGreater = (cmp > 0);
  string diff = absAGreater ? subAbs(absA, absB) : subAbs(absB, absA);
  int sign = absAGreater ? signA : signB;

  if (diff == "0") return "0";

  return (sign == -1 ? "-" : "") + diff;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string A, B; cin >> A >> B;

  cout << addSigned(A, B) << "\n";

  return 0;
}
```

