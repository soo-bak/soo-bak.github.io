---
layout: single
title: "[백준 9622] Cabin Baggage (C#, C++) - soo:bak"
date: "2023-07-01 09:25:00 +0900"
description: 수학, 사칙 연산, 구현, 조건 분기 등을 주제로 하는 백준 9622번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [9622번 - Cabin Baggage](https://www.acmicpc.net/problem/9622)

## 설명
입력으로 주어지는 수하물들의 정보를 바탕으로, 해당 수하물이 항공사의 기준에 부합하는지 판별하는 문제입니다. <br>

항공사의 수하물 기준은 다음과 같습니다. <br>
- 길이가 `56`cm 이하, 너비가 `45`cm 이하, 높이가 `25`cm 이하이거나, 길이와 너비, 높이의 합이 `125cm` 이하<br>
- 무게가 `7`kg 이하 <br>

위 조건에 맞추어 구현을 진행한 후, 기준을 만족하는 수하물에 대해서는 `1` 을, 만족하지 않는 수하물에 대해서는 `0` 을 출력합니다. <br>

마지막으로, 기준을 만족하는 수하물의 개수를 출력합니다. <br>

<br>
문제의 설명에는 나와있지 않지만, 테스트 케이스의 입력 중 데이터 구분자가 `"  "` 공백 두 칸인 경우가 있습니다.<br>

따라서, `C#` 혹은 `JAVA` 로 입력을 받을 때, 구분자로 `' '` 공백 한칸을 사용하게 되면, `Format` 에러가 발생하게 됨에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var t = int.Parse(Console.ReadLine()!);

      int cntAllowance = 0;
      for (int c = 0; c < t; c++) {
        var input = Console.ReadLine()!.Replace("  ", " ").Split(' ');
        var length = double.Parse(input[0]);
        var width = double.Parse(input[1]);
        var depth = double.Parse(input[2]);
        var weight = double.Parse(input[3]);

        var isAllowedSize = ((length <= 56 && width <= 45 && depth <= 25) ||
                             (length + width + depth <= 125));
        var isAllowedWeight = weight <= 7;

        if (isAllowedSize && isAllowedWeight) {
          Console.WriteLine("1");
          cntAllowance++;
        } else Console.WriteLine("0");
      }

      Console.WriteLine(cntAllowance);

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

  int t; cin >> t;

  int cntAllowance = 0;
  for (int c = 0; c < t; c++) {
    double length, width, depth, weight;
    cin >> length >> width >> depth >> weight;

    bool isAllowedSize = ((length <= 56 && width <= 45 && depth <= 25) ||
                          (length + width + depth <= 125));
    bool isAllowedWeight = weight <= 7;

    if (isAllowedSize && isAllowedWeight) {
      cout << "1\n";
      cntAllowance++;
    } else cout << "0\n";
  }

  cout << cntAllowance << "\n";

  return 0;
}
  ```
