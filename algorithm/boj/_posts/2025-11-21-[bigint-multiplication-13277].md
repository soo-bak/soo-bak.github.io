---
layout: single
title: "[백준 13277] 큰 수 곱셈 (C#, C++) - soo:bak"
date: "2025-11-21 23:55:00 +0900"
description: 최대 30만 자리 두 정수의 곱을 계산하는 백준 13277번 큰 수 곱셈 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 13277
  - C#
  - C++
  - 알고리즘
keywords: "백준 13277, 백준 13277번, BOJ 13277, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13277번 - 큰 수 곱셈](https://www.acmicpc.net/problem/13277)

## 설명

두 양의 정수 `A`와 `B`가 주어질 때, 두 수의 곱 `A × B`를 출력하는 문제입니다.

각 정수는 최대 300,000자리까지 가능하므로, 일반적인 정수 타입으로는 표현할 수 없습니다. 단순한 자릿수별 곱셈은 시간 복잡도가 O(n²)이므로 300,000자리에서는 시간 초과가 발생합니다.

<br>

## 접근법

C#의 경우 `System.Numerics.BigInteger` 타입을 사용하면 큰 수 곱셈을 직접 처리할 수 있습니다.

입력을 `BigInteger`로 파싱한 후 곱셈 연산자를 사용하여 결과를 계산합니다.

<br>
C++의 경우 FFT(Fast Fourier Transform)를 이용한 다항식 곱셈으로 구현합니다.

예를 들어 123과 456을 곱한다면, 이를 다항식 (1x² + 2x + 3)과 (4x² + 5x + 6)의 곱셈으로 볼 수 있습니다.

여기서 x는 10이며, 각 자릿수가 다항식의 계수가 됩니다.

두 다항식을 곱하면 결과 다항식의 계수들이 곱셈 결과의 각 자릿수(올림 처리 전)가 됩니다.

<br>
일반적인 다항식 곱셈은 모든 항의 조합을 계산하므로 O(n²) 시간이 걸립니다.

하지만 FFT를 사용하면 다항식을 여러 점에서 평가한 값으로 변환하여 곱셈을 수행한 후 다시 계수로 역변환하는 방식으로 O(n log n) 시간에 계산할 수 있습니다.

이는 다항식을 여러 점에서 평가한 값으로 표현하면 곱셈이 단순히 같은 점에서의 값끼리 곱하는 것으로 변환되기 때문입니다.

<br>
구현 단계는 다음과 같습니다.

먼저 두 수를 역순 자릿수 배열로 만듭니다.

예를 들어 123은 `[3, 2, 1]`이 됩니다.

역순으로 저장하는 이유는 낮은 자릿수가 배열의 앞쪽에 위치하여 올림 처리가 편리하기 때문입니다.

<br>
배열 크기를 두 수 길이의 합보다 큰 2의 거듭제곱으로 조정합니다. FFT는 2의 거듭제곱 크기에서 효율적으로 동작하기 때문입니다.

<br>
각 배열에 FFT를 적용하여 여러 점에서의 값으로 변환한 후, 같은 인덱스끼리 곱합니다.

이 단계가 실제 다항식 곱셈이 일어나는 곳입니다.

<br>
곱셈 결과에 역FFT를 적용하면 원래의 계수 형태로 돌아옵니다.

<br>
이 계수들은 아직 10 이상의 값을 가질 수 있으므로, 낮은 자릿수부터 순회하며 10으로 나눈 몫을 다음 자리로 올림 처리합니다.

<br>
마지막으로 앞자리 0을 제거하고 역순으로 문자열을 구성하여 출력합니다.

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

  for (int i = 1, j = 0; i < n; i++) {
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
      for (int j = 0; j < len / 2; j++) {
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
  fa.resize(n), fb.resize(n);

  fft(fa, false);
  fft(fb, false);
  for (int i = 0; i < n; i++) fa[i] *= fb[i];
  fft(fa, true);

  vi res(n);
  ll carry = 0;
  for (int i = 0; i < n; i++) {
    ll t = (ll)round(fa[i].real()) + carry;
    res[i] = t % 10;
    carry = t / 10;
  }

  while (carry)
    res.push_back(carry % 10), carry /= 10;

  while (res.size() > 1 && res.back() == 0) res.pop_back();

  string result;
  for (int i = res.size() - 1; i >= 0; --i) result.push_back(char('0' + res[i]));

  return result;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string a, b; cin >> a >> b;

  cout << multiply(a, b) << "\n";

  return 0;
}
```

