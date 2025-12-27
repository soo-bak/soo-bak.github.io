---
layout: single
title: "[백준 2750] 수 정렬하기 (C#, C++) - soo:bak"
date: "2023-05-22 15:51:00 +0900"
description: 수학과 정렬 알고리즘을 주제로 하는 백준 2750번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2750
  - C#
  - C++
  - 알고리즘
keywords: "백준 2750, 백준 2750번, BOJ 2750, SortingNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2750번 - 수 정렬하기](https://www.acmicpc.net/problem/2750)

## 설명
입력으로 주어진 수들을 오름차순으로 정렬하는 문제입니다. <br>

정렬을 위해 사용하는 알고리즘에는 다양한 알고리즘들이 존재합니다. <br>

각각의 정렬 알고리즘들 마다 시간 복잡도도 다르며, 구현의 방법 및 관점도 다릅니다. <br>

<br>
이 문제에서는 정렬 대상의 개수가 최대 `1001` 개로 비교적 작으며, 정렬 대상들이 중복되지 않는 다는 조건 또한 있습니다. <br>

따라서, 문제의 의도 및 학습의 의도를 고려하여 `sort()` 함수를 사용하지 않고,<br>

정렬 알고리즘들 중 가장 기본적이라고 할 수 있는 <b>거품 정렬</b> 알고리즘을 구현하여 풀이하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static void BubbleSort(int[] numbers, int n) {
      for (int i = 0; i < n; i++) {
        for (int j = 0; j < n - i - 1; j++) {
          if (numbers[j] > numbers[j + 1]) {
            var tmp = numbers[j];
            numbers[j] = numbers[j + 1];
            numbers[j + 1] = tmp;
          }
        }
      }
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var numbers = new int[n];
      for (int i = 0; i < n; i++)
        numbers[i] = int.Parse(Console.ReadLine()!);

      BubbleSort(numbers, n);

      foreach (var number in numbers)
        Console.WriteLine(number);

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

void bubbleSort(vector<int>& numbers, int n) {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n - i - 1; j++) {
      if (numbers[j] > numbers[j + 1])
        swap(numbers[j], numbers[j + 1]);
    }
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<int> numbers(n);

  for (int i = 0; i < n; i++)
    cin >> numbers[i];

  bubbleSort(numbers, n);

  for (const auto& number : numbers)
    cout << number << "\n";

  return 0;
}
  ```
