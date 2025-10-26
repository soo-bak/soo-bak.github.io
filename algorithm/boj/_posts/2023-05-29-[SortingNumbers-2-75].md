---
layout: single
title: "[백준 2751] 수 정렬하기 2 (C#, C++) - soo:bak"
date: "2023-05-29 19:56:00 +0900"
description: 정렬, 빠른 정렬, 힙 정렬 등을 주제로 하는 백준 2751번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [2751번 - 수 정렬하기 2](https://www.acmicpc.net/problem/2751)

## 설명
입력으로 주어지는 숫자들을 오름 차순으로 정렬하는 문제입니다. <br>

`n` 의 범위가 `1` <= `n` <= `1'000'000` 으로 크기 때문에, 이를 효율적으로 처리할 수 있는 알고리즘을 사용해야 합니다. <br>

`C++` 과 `C#` 의 `sort()` 표준 함수는 최소 시간 복잡도 `O(N logN)` 을 보장하도록 규정되어 있으므로,<br>

해당 표준 함수를 사용하여도 쉽게 문제를 풀이할 수 있습니다. <br>

<br>
하지만, 문제 풀이와 학습의 의도를 고려하여 시간 복잡도 `O(N logN)` 의 `힙 정렬(Heap Sort)` 알고리즘을 구현하여 풀이하였습니다. <br>

<br>

> 참고 : [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)

> 참고 : [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {

  using System.Text;
  class Program {

    static void Heapify(int[] arr, int n, int i) {
      int largest = i, left = 2 * i + 1, right = 2 * i + 2;

      if (left < n && arr[left] > arr[largest])
        largest = left;

      if (right < n && arr[right] > arr[largest])
        largest = right;

      if (largest != i) {
        (arr[i], arr[largest]) = (arr[largest], arr[i]);
        Heapify(arr, n, largest);
      }
    }

    static void HeapSort(int[] arr) {
      int n = arr.Length;

      for (int i = n / 2 - 1; i >= 0; i--)
        Heapify(arr, n, i);

      for (int i = n - 1; i >= 0; i--) {
        (arr[0], arr[i]) = (arr[i], arr[0]);
        Heapify(arr, i, 0);
      }
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var nums = new int[n];
      for (int i = 0; i < n; i++)
        nums[i] = int.Parse(Console.ReadLine()!);

      HeapSort(nums);

      var sb = new StringBuilder();

      foreach (var num in nums)
        sb.AppendLine(num.ToString());

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

void heapify(vector<int>& arr, const int& n, const int& i) {
  int largest = i, left = 2 * i + 1, right = 2 * i + 2;

  if (left < n && arr[left] > arr[largest])
    largest = left;

  if (right < n && arr[right] > arr[largest])
    largest = right;

  if (largest != i) {
    swap(arr[i], arr[largest]);
    heapify(arr, n, largest);
  }
}

void heapSort(vector<int>& arr) {
  int n = arr.size();

  for (int i = n / 2 - 1; i >= 0; i--)
    heapify(arr, n, i);

  for (int i = n - 1; i >= 0; i--) {
    swap(arr[0], arr[i]);
    heapify(arr, i, 0);
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<int> nums(n);
  for (int i = 0; i < n; i++)
    cin >> nums[i];

  heapSort(nums);

  for (const auto& num : nums)
    cout << num << "\n";

  return 0;
}
  ```
