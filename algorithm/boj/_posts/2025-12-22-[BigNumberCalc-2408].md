---
layout: single
title: "[백준 2408] 큰 수 계산 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 2408번 C#, C++ 풀이 - 큰 수에 대해 덧셈/뺄셈/곱셈/나눗셈을 순서대로 적용하는 문제"
tags:
  - 백준
  - BOJ
  - 2408
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
  - arbitrary_precision
keywords: "백준 2408, 백준 2408번, BOJ 2408, BigNumberCalc, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2408번 - 큰 수 계산](https://www.acmicpc.net/problem/2408)

## 설명
큰 수 수식을 왼쪽부터 순서대로 계산하고 결과를 출력하는 문제입니다.

<br>

## 접근법
입력된 수와 연산자를 하나의 수식으로 합친 뒤, 일반 사칙연산 우선순위에 따라 계산합니다.

먼저 곱셈과 나눗셈을 처리하고, 이후 덧셈과 뺄셈을 처리합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Numerics;

class Program {
  static BigInteger FloorDiv(BigInteger a, BigInteger b) {
    var q = a / b;
    var r = a % b;
    if (r != 0 && ((r > 0 && b < 0) || (r < 0 && b > 0)))
      q -= 1;
    return q;
  }

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var nums = new List<BigInteger>();
    var ops = new List<char>();

    nums.Add(BigInteger.Parse(Console.ReadLine()!));
    for (var i = 0; i < n - 1; i++) {
      ops.Add(Console.ReadLine()![0]);
      nums.Add(BigInteger.Parse(Console.ReadLine()!));
    }

    for (var i = 0; i < ops.Count; ) {
      if (ops[i] == '*' || ops[i] == '/') {
        if (ops[i] == '*') nums[i] *= nums[i + 1];
        else nums[i] = FloorDiv(nums[i], nums[i + 1]);
        nums.RemoveAt(i + 1);
        ops.RemoveAt(i);
      } else i++;
    }

    var res = nums[0];
    for (var i = 0; i < ops.Count; i++) {
      if (ops[i] == '+') res += nums[i + 1];
      else res -= nums[i + 1];
    }

    Console.WriteLine(res);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

struct BigInt {
  string d;
  bool neg = false;

  BigInt() : d("0") {}
  BigInt(string s) {
    if (!s.empty() && s[0] == '-') { neg = true; s = s.substr(1); }
    while (s.size() > 1 && s[0] == '0') s.erase(s.begin());
    d = s.empty() ? "0" : s;
  }

  static bool less(const string& a, const string& b) {
    if (a.size() != b.size()) return a.size() < b.size();
    return a < b;
  }

  static string addAbs(const string& a, const string& b) {
    string r;
    int c = 0, i = a.size() - 1, j = b.size() - 1;
    while (i >= 0 || j >= 0 || c) {
      int x = (i >= 0 ? a[i--] - '0' : 0) + (j >= 0 ? b[j--] - '0' : 0) + c;
      r.push_back('0' + x % 10); c = x / 10;
    }
    reverse(r.begin(), r.end());
    return r;
  }

  static string subAbs(const string& a, const string& b) {
    string r;
    int c = 0, i = a.size() - 1, j = b.size() - 1;
    while (i >= 0) {
      int x = a[i--] - '0' - (j >= 0 ? b[j--] - '0' : 0) - c;
      if (x < 0) { x += 10; c = 1; } else c = 0;
      r.push_back('0' + x);
    }
    while (r.size() > 1 && r.back() == '0') r.pop_back();
    reverse(r.begin(), r.end());
    return r;
  }

  static string mulAbs(const string& a, const string& b) {
    vector<int> r(a.size() + b.size(), 0);
    for (int i = a.size() - 1; i >= 0; i--) {
      for (int j = b.size() - 1; j >= 0; j--) {
        int m = (a[i] - '0') * (b[j] - '0');
        int p = i + j + 1;
        r[p] += m; r[p - 1] += r[p] / 10; r[p] %= 10;
      }
    }
    string s;
    for (int x : r)
      if (!(s.empty() && x == 0)) s.push_back('0' + x);
    return s.empty() ? "0" : s;
  }

  static pair<string, string> divAbs(const string& a, const string& b) {
    if (less(a, b)) return {"0", a};
    string q, cur;
    for (char ch : a) {
      cur.push_back(ch);
      while (cur.size() > 1 && cur[0] == '0') cur.erase(cur.begin());
      int cnt = 0;
      while (!less(cur, b)) { cur = subAbs(cur, b); cnt++; }
      q.push_back('0' + cnt);
    }
    while (q.size() > 1 && q[0] == '0') q.erase(q.begin());
    if (cur.empty()) cur = "0";
    return {q, cur};
  }

  BigInt operator+(const BigInt& o) const {
    BigInt r;
    if (neg == o.neg) { r.d = addAbs(d, o.d); r.neg = neg; }
    else if (less(d, o.d)) { r.d = subAbs(o.d, d); r.neg = o.neg; }
    else { r.d = subAbs(d, o.d); r.neg = neg; }
    if (r.d == "0") r.neg = false;
    return r;
  }

  BigInt operator-(const BigInt& o) const {
    BigInt t = o; t.neg = !t.neg;
    return *this + t;
  }

  BigInt operator*(const BigInt& o) const {
    BigInt r; r.d = mulAbs(d, o.d);
    r.neg = (neg != o.neg) && r.d != "0";
    return r;
  }

  BigInt floorDiv(const BigInt& o) const {
    auto pr = divAbs(d, o.d);
    BigInt r; r.d = pr.first;
    r.neg = (neg != o.neg) && r.d != "0";
    if (pr.second != "0" && neg != o.neg)
      r = r - BigInt("1");
    return r;
  }

  friend ostream& operator<<(ostream& os, const BigInt& x) {
    if (x.neg) os << '-';
    return os << x.d;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<BigInt> nums;
  vector<char> ops;

  string s; cin >> s;
  nums.push_back(BigInt(s));
  for (int i = 0; i < n - 1; i++) {
    char op; string v;
    cin >> op >> v;
    ops.push_back(op);
    nums.push_back(BigInt(v));
  }

  for (int i = 0; i < (int)ops.size(); ) {
    if (ops[i] == '*' || ops[i] == '/') {
      if (ops[i] == '*') nums[i] = nums[i] * nums[i + 1];
      else nums[i] = nums[i].floorDiv(nums[i + 1]);
      nums.erase(nums.begin() + i + 1);
      ops.erase(ops.begin() + i);
    } else i++;
  }

  BigInt res = nums[0];
  for (int i = 0; i < (int)ops.size(); i++) {
    if (ops[i] == '+') res = res + nums[i + 1];
    else res = res - nums[i + 1];
  }

  cout << res << "\n";

  return 0;
}
```
