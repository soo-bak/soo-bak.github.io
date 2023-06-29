---
layout: single
title: "[백준 2805] 나무 자르기 (C#, C++) - soo:bak"
date: "2023-06-28 14:30:00 +0900"
description: 이분 탐색, 수학 등을 주제로 하는 백준 2805번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [2805번 - 나무 자르기](https://www.acmicpc.net/problem/2805)

## 설명
`n` 개의 나무들의 높이와, 집으로 가져가길 원하는 나무들의 <b>최소</b> 길이 합 `m` 이 주어졌을 때, <br>

나무를 잘라 적어도 합이 `m` 이상이 되게 하여 집으로 가져갈 수 있게 하는, 절단기의 <b>최대</b> 높이 `h` 를 찾는 문제입니다. <br>

<br>
문제의 설명에 따르면, 절단기는 땅으로부터 `h` 의 높이에서 나무들을 절단하므로, <br>

절단기의 최소 높이는 `0` 으로, 최대 높이는 입력받은 나무들의 높이 중 가장 큰 높이로 설정하여 이분 탐색을 진행합니다. <br>

이후, 각 경우의 절단기 높이로 나무를 잘랐을 때, 적어도 `m` 길이 이상의 나무를 얻을 수 있는지 확인합니다. <br>

<br>
절단기의 <b>최대</b> 높이를 찾아야 하므로, `m` 길이 이상의 나무를 얻을 수 있는 경우, 절단기 높이를 더 크게 설정하고 탐색을 계속 진행합니다. <br>

만약, `m` 길이 이상의 나무를 얻을 수 없는 경우, 절단기의 높이를 더 작게 설정하고 탐색을 계속 진행합니다. <br>

이러한 이분 탐색 과정을 통하여 '적어도 `m` 길이 이상의 나무를 얻을 수 있는 절단기의 최대 높이 `h`' 를 찾을 수 있습니다. <br>

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
      var m = int.Parse(input[1]);

      var trees = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

      int start = 0, end = trees.Max();
      while (start <= end) {
        int mid = (start + end) / 2;

        long wood = 0;
        foreach (var tree in trees)
          if (tree > mid)
            wood += tree - mid;

        if (wood >= m) start = mid + 1;
        else end = mid - 1;
      }

      Console.WriteLine(end);

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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vector<int> trees(n);
  for (int i = 0; i < n; i++)
    cin >> trees[i];

  int start = 0, end = *max_element(trees.begin(), trees.end());
  while (start <= end) {
    int mid = (start + end) / 2;

    ll wood = 0;
    for (int tree : trees)
      if (tree > mid)
        wood += tree - mid;

    if (wood >= m) start = mid + 1;
    else end = mid - 1;
  }

  cout << end << "\n";

  return 0;
}
  ```
