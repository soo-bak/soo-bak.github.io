---
layout: single
title: "[백준 25542] 약속 장소 (C#, C++) - soo:bak"
date: "2023-05-17 02:55:00 +0900"
description: 문자열과 완전 탐색을 주제로 하는 백준 25542번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [25542번 - 약속 장소](https://www.acmicpc.net/problem/25542)

## 설명
`n` 개의 문자열이 주어졌을 때, `n` 개의 문자열들 각각과 한 문자만 다른 문자가 있는지 판별하는 문제입니다. <br>

입력으로 주어지는 문자열의 길이가 길지 않고, `n` 의 크기 역시 크지 않습니다. <br>

따라서, 단순히 완전탐색을 이용하여 풀이하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var n = int.Parse(input[0]);
      var l = int.Parse(input[1]);

      List<string> candidates = new List<string>();
      for (int i = 0; i < n; i++)
        candidates.Add(Console.ReadLine()!);

      char[] ans = candidates[0].ToCharArray();
      for (int i = 0; i < l; i++) {
        bool isFound = false;
        for (char c = 'A'; c <= 'Z'; c++) {
          ans[i] = c;
          bool isValid = true;
          foreach (var candidate in candidates) {
            int cntDiff = 0;
            for (int j = 0; j < l; j++) {
              if (candidate[j] != ans[j]) cntDiff++;
              if (cntDiff > 1) {
                isValid = false;
                break ;
              }
            }
            if (!isValid) break ;
          }
          if (isValid) {
            isFound = true;
            break ;
          }
        }
        if (!isFound) ans[i] = candidates[0][i];
      }

      int diffMax = 0;
      for (int i = 0; i < n; i++) {
        int diffCur = 0;
        for (int j = 0; j < l; j++)  {
          if (candidates[i][j] != ans[j])
            diffCur++;
        }
        diffMax = Math.Max(diffMax, diffCur);
      }

      if (diffMax > 1) Console.WriteLine("CALL FRIEND");
      else Console.WriteLine(new string(ans));

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

  int n, l; cin >> n >> l;

  vector<string> candidates(n);
  for (int i = 0; i < n; i++)
    cin >> candidates[i];

  string ans = candidates[0];
  for (int i = 0; i < l; i++) {
    bool isFound = false;
    for (char c = 'A'; c <= 'Z'; c++) {
      ans[i] = c;
      bool isValid = true;
      for (const auto &candidate : candidates) {
        int cntDiff = 0;
        for (int j = 0; j < l; j++) {
          if (candidate[j] != ans[j]) cntDiff++;
          if (cntDiff > 1) {
            isValid = false;
            break ;
          }
        }
        if (!isValid) break ;
      }
      if (isValid) {
        isFound = true;
        break ;
      }
    }
    if (!isFound) ans[i] = candidates[0][i];
  }

  int diffMax = 0;
  for (int i = 0; i < n; i++) {
    int diffCur = 0;
    for (int j = 0; j < l; j++) {
      if (candidates[i][j] != ans[j])
        diffCur++;
    }
    diffMax = max(diffMax, diffCur);
  }

  if (diffMax > 1) cout << "CALL FRIEND" << "\n";
  else cout << ans << "\n";

  return 0;
}
  ```
