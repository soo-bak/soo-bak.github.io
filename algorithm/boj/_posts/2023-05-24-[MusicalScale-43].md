---
layout: single
title: "[백준 2920] 음계 (C#, C++) - soo:bak"
date: "2023-05-24 20:23:00 +0900"
---

## 문제 링크
  [2920번 - 음계](https://www.acmicpc.net/problem/2920)

## 설명
입력으로 주어지는 음의 연주 순서를 분석하여,<br>

그 순서가 오름차순인지, 내림차순인지 혹은 둘 다 아닌지를 판별하는 문제입니다. <br>

<br>
반복문으로 모든 음에 각각에 대해서 이전 음과의 비교를 통해 풀이할 수도 있지만, <br>

음의 총 개수가 `8` 개 뿐이므로 미리 배열을 만들어서 비교하는 방법으로 풀이하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var ascending = Enumerable.Range(1, 8).ToArray();
      var descending = Enumerable.Range(1, 8).Reverse().ToArray();

      var input = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

      if (input.SequenceEqual(ascending))
        Console.WriteLine("ascending");
      else if (input.SequenceEqual(descending))
        Console.WriteLine("descending");
      else Console.WriteLine("mixed");

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

  vector<int> ascending = {1, 2, 3, 4, 5, 6, 7, 8};
  vector<int> descending = {8, 7, 6, 5, 4, 3, 2, 1};

  vector<int> input(8);
  for (int i = 0; i < 8; i++)
    cin >> input[i];

  if (input == ascending) cout << "ascending\n";
  else if (input == descending) cout << "descending\n";
  else cout << "mixed\n";

  return 0;
}
  ```
