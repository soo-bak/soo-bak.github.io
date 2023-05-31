---
layout: single
title: "[백준 1654] 랜선 자르기 (C#, C++) - soo:bak"
date: "2023-05-31 21:16:00 +0900"
---

## 문제 링크
  [1654번 - 랜선 자르기](https://www.acmicpc.net/problem/1654)

## 설명
입력으로 주어지는 `k` 개의 랜선들에 대해서, 각 랜선을 자르며 `n` 개의 랜선을 만들 때, 만들 수 있는 `최대 길이` 를 찾는 문제입니다. <br>

문제의 시간 제한과 입력의 범위를 고려하였을 때, 가장 적합한 풀이 방법 중 하나는 `이분 탐색` 을 활용하는 것입니다. <br>

<br>
`이분 탐색` 알고리즘은 <b>정렬된</b> 데이터 구조에서 특정 값을 찾아내는 데에 효율적인 알고리즘입니다. <br>

이 알고리즘은 먼저 중간 값을 선택하고, 찾는 값이 이보다 큰지 작은지를 확인한 후,<br>

<b>검색의 범위를 절반으로 줄이는 과정을 반복</b>하여 효율적으로 탐색을 진행할 수 있습니다. <br>

`이분 탐색` 알고리즘에 관한 자세한 설명은 [여기](https://soo-bak.github.io/algorithm/theory/) 에서 확인하실 수 있습니다. <br>

<br>
먼저, 이미 가지고 있는 랜선들 중 가장 긴 길이를 찾고, 이 길이를 초기 최대 길이로 설정합니다.<br>

최소 길이는 랜선의 길이가 양의 정수라는 조건을 바탕으로 `1` 로 설정합니다. <br>

그 후, `while` 반복문을 이용하여 `최소 길이` 가 `최대 길이` 보다 작거나 같을 때 까지 이분 탐색을 진행합니다. <br>

이분 탐색을 위해 중간 값을 계산하고, 이 중간 값이 만약 `n` 개의 랜선을 만들 수 있는 길이라면, 최소 길이를 중간 값보다 `1` 큰 값으로 갱신합니다. <br>

만약 중간 값으로 `n` 개의 랜선을 만들 수 없다면, 최대 길이를 중간 값보다 `1` 작은 값으로 갱신합니다. <br>

<br>
이렇게 `최소 길이` 와 `최대 길이` 가 같아질 때까지 이분 탐색을 반복하면, n` 개의 랜선을 만들 수 있는 가장 긴 길이를 찾을 수 있습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var k = int.Parse(input[0]);
      var n = int.Parse(input[1]);

      var lines = new long[k];
      for (int i = 0; i < k; i++)
        lines[i] = long.Parse(Console.ReadLine()!);

      var maxLine = lines.Max();
      long minLine = 1;
      long ans = 0;

      while (minLine <= maxLine) {
        var midLine = (minLine + maxLine) / 2;
        var cnt = lines.Sum(line => line / midLine);

        if (cnt >= n) {
          ans = Math.Max(ans, midLine);
          minLine = midLine + 1;
        } else maxLine = midLine - 1;
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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int k, n; cin >> k >> n;

  vector<ll> lines(k);
  for (int i = 0; i < k; i++)
    cin >> lines[i];

  ll maxLine = *max_element(lines.begin(), lines.end());
  ll minLine = 1;
  ll ans = 0;

  while (minLine <= maxLine) {
    ll midLine = (minLine + maxLine) / 2;
    ll cnt = 0;

    for (int i = 0; i < k; i++)
      cnt += lines[i] / midLine;

    if (cnt >= n) {
      if (ans < midLine) ans = midLine;
      minLine = midLine + 1;
    } else maxLine = midLine - 1;
  }

  cout << ans << "\n";

  return 0;
}
  ```
