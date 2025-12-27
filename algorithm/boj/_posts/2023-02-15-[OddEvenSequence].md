---
layout: single
title: "[백준 25629] 홀짝 수열 (C#, C++) - soo:bak"
date: "2023-02-15 18:16:00 +0900"
description: 수열과 수학을 주제로한 백준 25629번 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 25629
  - C#
  - C++
  - 알고리즘
keywords: "백준 25629, 백준 25629번, BOJ 25629, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [25629번 - 홀짝 수열](https://www.acmicpc.net/problem/25629)

## 설명
  수학과 구현 문제입니다.<br>

  문제의 조건에 맞는 `홀짝 수열` 을 만들기 위해서는 다음과 같은 조건들을 만족해야 합니다. <br>

  1. 홀수 원소들의 개수와 짝수 원소들의 개수가 같거나, 홀수 원소들의 개수가 짝수 원소들의 개수보다 1개 많아야 한다.
  2. 홀수 원소들을 감소하지 않는 순서대로 정렬할 수 있어야 한다.
  3. 짝수 원소들을 감소하지 않는 순서대로 정렬할 수 있어야 한다.

  입력으로 주어진 숫자들을 파싱한 후, 위 조건들의 만족 여부에 따라 정답을 출력합니다.
  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int.TryParse(Console.ReadLine(), out int n);

      string[]? input = Console.ReadLine()?.Split();
      List<int> lstOdd = new List<int>(), lstEven = new List<int>();
      for (int i = 0; i < n; i++) {
        int.TryParse(input?[i], out int num);
        if (num % 2 == 1) lstOdd.Add(num);
        else lstEven.Add(num);
      }

      int ans = 1;
      if (lstOdd.Count - lstEven.Count > 1 || lstOdd.Count - lstEven.Count < 0)
        ans = 0;
      else {
        lstOdd.Sort(); lstEven.Sort();

        for (int i = 1; i < lstEven.Count; i++) {
          if (lstEven[i] < lstEven[i - 1]) {
            ans = 0;
            break ;
          }
        }

        if (ans != 0) {
          for (int i = 1; i < lstOdd.Count; i++) {
            if (lstOdd[i] < lstOdd[i - 1]) {
              ans = 0;
              break ;
            }
          }
        }
      }

      Console.WriteLine(ans);
    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<int> vOdd, vEven;

  for (int i = 0; i < n; i++) {
    int num; cin >> num;
    if (num % 2 == 1) vOdd.push_back(num);
    else vEven.push_back(num);
  }

  int ans = 1;
  if (vOdd.size() - vEven.size() > 1 || vOdd.size() - vEven.size() < 0)
    ans = 0;
  else {
    sort(vOdd.begin(), vOdd.end());
    sort(vEven.begin(), vEven.end());

    for (size_t i = 1; i < vEven.size(); i++) {
      if (vEven[i] < vEven[i]) {
        ans = 0; break ;
      }
    }

    if (ans != 0) {
      for (size_t i = 1; i < vOdd.size(); i++) {
        if (vOdd[i] < vOdd[i]) {
          ans = 0; break ;
        }
      }
    }

  }

  cout << ans << "\n" ;

  return 0;
}
  ```
