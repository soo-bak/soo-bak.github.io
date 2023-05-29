---
layout: single
title: "[백준 11650] 좌표 정렬하기 (C#, C++) - soo:bak"
date: "2023-05-29 21:19:00 +0900"
---

## 문제 링크
  [11650번 - 좌표 정렬하기](https://www.acmicpc.net/problem/11650)

## 설명
입력으로 주어지는 2차원 평면 위의 점들을 정렬하는 문제입니다. <br>

정렬의 규칙은 다음과 같습니다. <br>

- `x` 좌표가 증가하는 순으로 정렬 <br>
- `x` 좌표가 같다면 `y` 좌표가 증가하는 순으로 정렬 <br>

<br>
`C++` 에서 `sort()` 함수는 기본적으로 `pair` 의 `first` 를 우선으로, 그 후에 `second` 를 비교하여 정렬하므로, <br>

별도의 비교 함수를 구현하지 않고 점의 위치를 `pair` 로 저장하여 풀이하였습니다. <br>

<br>
`C#` 에서는 `Tuple` 클래스를 활용하였습니다.<br>

`C#` 의 `Tuple` 클래스는 내부의 모든 요소가 `IComparable` 인터페이스를 구현하는 경우,<br>

자체적으로 모든 요소에 대하여 `IComparable` 를 구현하기 때문에, `Tuple` 클래스 내부의 모든 요소에 대하여 순차적인 비교가 가능합니다.<br>

<br>
또한, `C#` 에서는 `StringBuilder` 을 사용하지 않으면 `시간 초과` 가 됨에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  using System.Text;
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var points = new Tuple<int, int>[n];
      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        points[i] = Tuple.Create(int.Parse(input[0]), int.Parse(input[1]));
      }

      Array.Sort(points);

      var sb = new StringBuilder();

      foreach (var point in points)
        sb.AppendLine($"{point.Item1} {point.Item2}");
      Console.Write(sb.ToString());

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

typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<pii> points(n);
  for (int i = 0; i < n; i++)
    cin >> points[i].first >> points[i].second;

  sort(points.begin(), points.end());

  for (const auto& point : points)
    cout << point.first << " " << point.second << "\n";

  return 0;
}
  ```
