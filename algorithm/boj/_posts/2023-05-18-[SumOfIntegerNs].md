---
layout: single
title: "[백준 15596] 정수 N개의 합 (C++) - soo:bak"
date: "2023-05-18 13:13:00 +0900"
description: 시뮬레이션과 함수 구현을 주제로 하는 백준 15596번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 15596
  - C++
  - 알고리즘
keywords: "백준 15596, 백준 15596번, BOJ 15596, C++ 풀이, 알고리즘"
---

## 문제 링크
  [15596번 - 정수 N개의 합](https://www.acmicpc.net/problem/15596)

## 설명
해당 문제는 각 언어에 따라서 주어진 함수를 구현하는 문제입니다. <br>

`제출` 에서 언어를 선택하면, 작성해야 하는 함수가 해당하는 언어에 따라 <b>완전히 구현되지 않은 형태</b>로 나타납니다. <br>

해당 함수를 문제의 조건에 맞게 구현하는 것이 문제의 목표입니다. <br>

<br>
`C++` 의 경우, 다음과 같은 함수 원형이 주어집니다. <br>
  ```c++
#include <vector>
long long sum(std::vector<int> &a) {
  long long ans = 0;
  return ans;
}
  ```

해당 함수 원형을 바탕으로 문제의 조건에 맞게 구현을 진행한 후 제출하면 됩니다. <br>

- - -

## Code
<b>[ C++ ] </b>
<br>

  ```c++
#include <vector>
long long sum(std::vector<int> &a) {
  long long ans = 0;

  for(const auto& ele : a)
    ans += ele;

  return ans;
}
  ```
