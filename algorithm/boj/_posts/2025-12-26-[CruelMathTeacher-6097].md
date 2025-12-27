---
layout: single
title: "[백준 6097] Cruel Math Teacher (C#, C++) - soo:bak"
date: "2025-12-26 03:24:00 +0900"
description: "백준 6097번 C#, C++ 풀이 - 큰 정수 거듭제곱을 계산해 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 6097
  - C#
  - C++
  - 알고리즘
keywords: "백준 6097, 백준 6097번, BOJ 6097, CruelMathTeacher, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6097번 - Cruel Math Teacher](https://www.acmicpc.net/problem/6097)

## 설명
정수 N의 P제곱을 계산하고 70자리씩 출력하는 문제입니다.

<br>

## 접근법
먼저 큰 수를 자리 배열로 관리해 곱셈을 직접 구현합니다.

다음으로 거듭제곱은 제곱 분할로 계산해 곱셈 횟수를 줄입니다.

마지막으로 완성된 수를 문자열로 만들고 70자리씩 끊어 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Text;

class Program {
  const int BaseVal = 10000;

  static List<int> Mul(List<int> a, List<int> b) {
    var res = new int[a.Count + b.Count + 1];
    for (var i = 0; i < a.Count; i++) {
      long carry = 0;
      for (var j = 0; j < b.Count; j++) {
        long cur = res[i + j] + (long)a[i] * b[j] + carry;
        res[i + j] = (int)(cur % BaseVal);
        carry = cur / BaseVal;
      }
      var idx = i + b.Count;
      while (carry > 0) {
        long cur = res[idx] + carry;
        res[idx] = (int)(cur % BaseVal);
        carry = cur / BaseVal;
        idx++;
      }
    }

    var len = res.Length;
    while (len > 1 && res[len - 1] == 0)
      len--;

    var list = new List<int>(len);
    for (var i = 0; i < len; i++)
      list.Add(res[i]);

    return list;
  }

  static List<int> Pow(int n, int p) {
    var baseNum = new List<int>();
    while (n > 0) {
      baseNum.Add(n % BaseVal);
      n /= BaseVal;
    }
    if (baseNum.Count == 0) baseNum.Add(0);

    var result = new List<int> { 1 };
    var exp = p;
    while (exp > 0) {
      if ((exp & 1) == 1) result = Mul(result, baseNum);
      baseNum = Mul(baseNum, baseNum);
      exp >>= 1;
    }
    return result;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var p = int.Parse(parts[1]);

    var num = Pow(n, p);
    var sb = new StringBuilder();
    sb.Append(num[num.Count - 1].ToString());
    for (var i = num.Count - 2; i >= 0; i--)
      sb.Append(num[i].ToString("D4"));

    var s = sb.ToString();
    var outSb = new StringBuilder();
    for (var i = 0; i < s.Length; i += 70) {
      var len = Math.Min(70, s.Length - i);
      outSb.AppendLine(s.Substring(i, len));
    }

    Console.Write(outSb.ToString());
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef vector<int> vi;

const int BASE = 10000;

vi mul(const vi &a, const vi &b) {
  vi res(a.size() + b.size() + 1, 0);
  for (int i = 0; i < (int)a.size(); i++) {
    ll carry = 0;
    for (int j = 0; j < (int)b.size(); j++) {
      ll cur = res[i + j] + 1LL * a[i] * b[j] + carry;
      res[i + j] = (int)(cur % BASE);
      carry = cur / BASE;
    }
    int idx = i + (int)b.size();
    while (carry > 0) {
      ll cur = res[idx] + carry;
      res[idx] = (int)(cur % BASE);
      carry = cur / BASE;
      idx++;
    }
  }

  while (res.size() > 1 && res.back() == 0)
    res.pop_back();

  return res;
}

vi powNum(int n, int p) {
  vi baseNum;
  while (n > 0) {
    baseNum.push_back(n % BASE);
    n /= BASE;
  }
  if (baseNum.empty()) baseNum.push_back(0);

  vi result(1, 1);
  int exp = p;
  while (exp > 0) {
    if (exp & 1) result = mul(result, baseNum);
    baseNum = mul(baseNum, baseNum);
    exp >>= 1;
  }
  return result;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, p; cin >> n >> p;

  vi num = powNum(n, p);
  string s = to_string(num.back());
  for (int i = (int)num.size() - 2; i >= 0; i--) {
    string part = to_string(num[i]);
    s += string(4 - (int)part.size(), '0') + part;
  }

  for (int i = 0; i < (int)s.size(); i += 70) {
    int len = min(70, (int)s.size() - i);
    cout << s.substr(i, len) << "\n";
  }

  return 0;
}
```
