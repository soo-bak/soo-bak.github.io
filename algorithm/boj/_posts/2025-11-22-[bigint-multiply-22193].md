---
layout: single
title: "[백준 22193] Multiply (C#, C++) - soo:bak"
date: "2025-11-22 03:10:00 +0900"
description: 최대 5만 자리 두 정수의 곱을 arbitrary precision으로 계산하는 백준 22193번 Multiply 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 22193
  - C#
  - C++
  - 알고리즘
keywords: "백준 22193, 백준 22193번, BOJ 22193, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[22193번 - Multiply](https://www.acmicpc.net/problem/22193)

## 설명

두 양의 정수 `A`와 `B`의 곱을 계산하는 문제입니다. 각 수는 최대 50,000자리까지 가능하므로 일반적인 64비트 정수로는 표현할 수 없습니다.

따라서 임의 정밀도(arbitrary precision) 연산이 가능한 방식으로 큰 수의 곱셈을 처리해야 합니다.

<br>

## 접근법

C#은 `BigInteger` 클래스를 사용하여 곱셈을 직접 계산할 수 있습니다.

<br>
C++은 FFT(Fast Fourier Transform) 기반 다항식 곱셈으로 큰 수 곱셈을 구현합니다.

각 자릿수를 다항식의 계수로 보고 `x = 10`일 때의 결과를 구하는 방식입니다.

FFT는 다항식 곱셈을 `O(n log n)` 시간에 처리할 수 있어 최대 5만 자리 곱셈도 효율적으로 수행 가능합니다.

<br>
구체적으로는 숫자 문자열을 역순으로 자릿수 배열로 변환하고, 배열 크기를 2의 거듭제곱으로 조정합니다.

FFT를 적용하여 여러 점에서 평가한 값으로 변환한 후 각 점에서 곱셈을 수행하고, 역 FFT로 원래의 계수 형태로 되돌립니다. 

마지막으로 올림을 처리하고 앞자리 0을 제거하여 최종 결과를 얻습니다.

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
      _ = Console.ReadLine();
      var a = BigInteger.Parse(Console.ReadLine()!);
      var b = BigInteger.Parse(Console.ReadLine()!);

      Console.WriteLine(a * b);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef complex<double> cd;
typedef vector<int> vi;
typedef long long ll;

const double PI = acos(-1);

void fft(vector<cd>& a, bool invert) {
  int n = a.size();
  for (int i = 1, j = 0; i < n; ++i) {
    int bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) swap(a[i], a[j]);
  }

  for (int len = 2; len <= n; len <<= 1) {
    double ang = 2 * PI / len * (invert ? -1 : 1);
    cd wlen(cos(ang), sin(ang));
    for (int i = 0; i < n; i += len) {
      cd w(1);
      for (int j = 0; j < len / 2; ++j) {
        cd u = a[i + j], v = a[i + j + len / 2] * w;
        a[i + j] = u + v;
        a[i + j + len / 2] = u - v;
        w *= wlen;
      }
    }
  }

  if (invert)
    for (cd &x : a) x /= n;
}

string multiply(const string& s1, const string& s2) {
  if (s1 == "0" || s2 == "0") return "0";

  vi a, b;
  for (int i = s1.size() - 1; i >= 0; --i) a.push_back(s1[i] - '0');
  for (int i = s2.size() - 1; i >= 0; --i) b.push_back(s2[i] - '0');

  int n = 1;
  while (n < (int)a.size() + (int)b.size()) n <<= 1;
  vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
  fa.resize(n); fb.resize(n);

  fft(fa, false);
  fft(fb, false);
  for (int i = 0; i < n; ++i) fa[i] *= fb[i];
  fft(fa, true);

  vi res(n);
  ll carry = 0;
  for (int i = 0; i < n; ++i) {
    ll val = llround(fa[i].real()) + carry;
    res[i] = val % 10;
    carry = val / 10;
  }

  while (carry) {
    res.push_back(carry % 10);
    carry /= 10;
  }
  while (res.size() > 1 && res.back() == 0) res.pop_back();

  string out;
  for (int i = res.size() - 1; i >= 0; --i)
    out.push_back('0' + res[i]);

  return out;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  string a, b; cin >> a >> b;

  cout << multiply(a, b) << "\n";

  return 0;
}
```

