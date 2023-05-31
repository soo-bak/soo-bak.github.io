---
layout: single
title: "[백준 5086] 배수와 약수 (C#, C++) - soo:bak"
date: "2023-05-22 17:07:00 +0900"
description: 수학과 배수 약수를 주제로 하는 백준 5086번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [5086번 - 배수와 약수](https://www.acmicpc.net/problem/5086)

## 설명
두 수의 배수와 약수 관계를 판별하는 문제입니다. <br>

입력으로 두 수가 주어지며,<br>

첫 번째 숫자가 두 번째 숫자의 약수이면 `factor`, 배수이면 `multiple`, 둘 다 아니면 `neither` 을 출력합니다. <br>

<br>
배수와 약수의 관계를 판별하는 방법은 다음과 같습니다. <br>

- 첫 번째 숫자를 두 번째 숫자로 나누었을 때, 나머지가 `0` 이면 첫 번째 숫자는 두 번째 숫자의 배수입니다. <br>
- 두 번째 숫자를 첫 번째 숫자로 나누었을 때, 나머지가 `0` 이면 첫 번재 숫자는 두 번째 숫자의 약수입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var input = Console.ReadLine()!.Split(' ');
        var num1 = int.Parse(input[0]);
        var num2 = int.Parse(input[1]);

        if (num1 == 0 && num2 == 0) break ;

        if (num1 % num2 == 0) Console.WriteLine("multiple");
        else if (num2 % num1 == 0) Console.WriteLine("factor") ;
        else Console.WriteLine("neither");
      }

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

  while (true) {
    int num1, num2; cin >> num1 >> num2;
    if (num1 == 0 && num2 == 0) break ;

    if (num1 % num2 == 0) cout << "multiple\n";
    else if (num2 % num1 == 0) cout << "factor\n";
    else cout << "neither\n";
  }

  return 0;
}
  ```
