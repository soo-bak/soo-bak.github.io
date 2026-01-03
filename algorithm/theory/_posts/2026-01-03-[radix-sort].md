---
layout: single
title: "기수 정렬(Radix Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 10:00:00 +0900"
description: 자릿수별로 정렬을 반복하여 전체를 정렬하는 기수 정렬 알고리듬의 원리, LSD/MSD 방식, 구현 방법을 다룹니다
tags:
  - 정렬
  - 기수정렬
---

## 기수 정렬이란?

**기수 정렬(Radix Sort)**은 숫자의 **자릿수(radix)**를 기준으로 정렬을 반복하여 전체를 정렬하는 알고리듬입니다.

비교 연산을 사용하지 않고, 각 자릿수 정렬에 계수 정렬을 활용하여 **$$O(d \cdot (n + k))$$** 시간에 정렬합니다.

여기서 $$d$$는 최대 자릿수, $$k$$는 기수(보통 10)입니다.

> 참고: [계수 정렬(Counting Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/counting-sort/)

---

## 기수 정렬의 원리

기수 정렬은 각 자릿수에 대해 안정 정렬을 반복 수행하여 전체를 정렬합니다.

LSD(Least Significant Digit) 방식은 가장 낮은 자릿수부터, MSD(Most Significant Digit) 방식은 가장 높은 자릿수부터 정렬합니다.

<br>

### LSD 방식 예시

배열 `[170, 45, 75, 90, 802, 24, 2, 66]`을 정렬하는 과정:

**1단계: 1의 자리로 정렬**
```
[170, 90, 802, 2, 24, 45, 75, 66]
```

**2단계: 10의 자리로 정렬**
```
[802, 2, 24, 45, 66, 170, 75, 90]
```

**3단계: 100의 자리로 정렬**
```
[2, 24, 45, 66, 75, 90, 170, 802]
```

<br>

각 단계에서 안정 정렬을 사용하기 때문에, 이전 단계의 정렬 결과가 유지됩니다.

---

## LSD vs MSD

<br>

### LSD (Least Significant Digit)

**가장 낮은 자릿수**부터 정렬합니다.

- 구현이 간단하고, 안정 정렬을 유지함
- 모든 자릿수를 반드시 처리해야 함

<br>

### MSD (Most Significant Digit)

**가장 높은 자릿수**부터 정렬합니다.

- 조기 종료가 가능하여 특정 경우 더 빠름
- 재귀적 구현이 필요하여 복잡함

<br>

일반적으로 **LSD 방식**이 더 많이 사용됩니다.

> 참고: [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

---

## 구현

### LSD 기수 정렬

```cpp
#include <bits/stdc++.h>
using namespace std;

void countingSortByDigit(vector<int>& arr, int exp) {
  int n = arr.size();
  vector<int> output(n);
  vector<int> count(10, 0);

  // 해당 자릿수의 개수 세기
  for (int i = 0; i < n; i++) {
    int digit = (arr[i] / exp) % 10;
    count[digit]++;
  }

  // 누적 합 계산
  for (int i = 1; i < 10; i++) {
    count[i] += count[i - 1];
  }

  // 출력 배열 생성 (안정성을 위해 역순)
  for (int i = n - 1; i >= 0; i--) {
    int digit = (arr[i] / exp) % 10;
    output[count[digit] - 1] = arr[i];
    count[digit]--;
  }

  arr = output;
}

void radixSort(vector<int>& arr) {
  if (arr.empty()) return;

  int maxVal = *max_element(arr.begin(), arr.end());

  // 각 자릿수에 대해 계수 정렬 수행
  for (int exp = 1; maxVal / exp > 0; exp *= 10) {
    countingSortByDigit(arr, exp);
  }
}

int main() {
  vector<int> arr = {170, 45, 75, 90, 802, 24, 2, 66};

  radixSort(arr);

  for (int x : arr) cout << x << " ";
  cout << "\n";

  return 0;
}
```

**출력**: `2 24 45 66 75 90 170 802`

<br>

### 음수 포함 기수 정렬

음수가 포함된 경우, 양수와 음수를 분리하여 처리합니다.

```cpp
void radixSortWithNegative(vector<int>& arr) {
  vector<int> negative, positive;

  for (int x : arr) {
    if (x < 0) negative.push_back(-x);
    else positive.push_back(x);
  }

  if (!negative.empty()) radixSort(negative);
  if (!positive.empty()) radixSort(positive);

  // 음수는 역순으로, 부호 복원
  arr.clear();
  for (int i = negative.size() - 1; i >= 0; i--) {
    arr.push_back(-negative[i]);
  }
  for (int x : positive) {
    arr.push_back(x);
  }
}
```

---

## 시간 복잡도

<br>

### 시간 복잡도: $$O(d \cdot (n + k))$$

- $$d$$: 최대 자릿수
- $$n$$: 원소 개수
- $$k$$: 기수 (보통 10)

$$k = 10$$이고 $$d$$가 상수라면, 시간 복잡도는 **$$O(n)$$**입니다.

<br>

### 공간 복잡도: $$O(n + k)$$

출력 배열과 계수 배열을 위한 추가 공간이 필요합니다.

---

## 기수 정렬의 특징

<br>

### 장점

- **선형 시간**: 자릿수가 적으면 $$O(n \log n)$$ 정렬보다 빠름
- **안정 정렬**: LSD 방식은 안정 정렬
- **비비교 정렬**: 비교 연산 없이 정렬

<br>

### 단점

- **정수 전용**: 실수에는 직접 적용 불가
- **추가 메모리**: $$O(n + k)$$의 추가 공간 필요
- **자릿수 의존**: 큰 수는 자릿수가 많아 효율이 떨어짐

<br>

기수 정렬은 자릿수 $$d$$가 $$\log n$$보다 작을 때 빠른 정렬이나 병합 정렬보다 효율적입니다.

---

## 활용

<br>

### 1. 대용량 정수 정렬

수백만 개의 정수를 정렬할 때, 값의 범위가 제한적이라면 기수 정렬이 효과적입니다.

<br>

### 2. 문자열 정렬

고정 길이 문자열을 각 문자 위치별로 정렬할 수 있습니다.

```cpp
void radixSortStrings(vector<string>& arr, int maxLen) {
  for (int pos = maxLen - 1; pos >= 0; pos--) {
    // pos 위치의 문자로 안정 정렬
    stable_sort(arr.begin(), arr.end(),
      [pos](const string& a, const string& b) {
        char ca = pos < a.size() ? a[pos] : 0;
        char cb = pos < b.size() ? b[pos] : 0;
        return ca < cb;
      });
  }
}
```

<br>

### 3. 날짜 정렬

YYYYMMDD 형식의 날짜를 정수로 변환하면, 8자리 숫자로 빠르게 정렬할 수 있습니다.

---

## 마무리

기수 정렬은 자릿수별로 안정 정렬을 반복하여 전체를 정렬하는 비비교 정렬 알고리듬입니다.

<br>

각 자릿수 정렬에 계수 정렬을 사용하며, 자릿수가 적고 원소 개수가 많은 경우에 $$O(n \log n)$$ 정렬보다 효율적입니다.

정수 데이터에만 적용 가능하다는 제약이 있지만, 적절한 조건에서는 매우 빠른 성능을 보여줍니다.

<br>

**관련 글**:
- [계수 정렬(Counting Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/counting-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

<br>

**관련 문제**:
- [[백준 10989] 수 정렬하기 3](https://soo-bak.github.io/algorithm/boj/sortingNumbers3/)
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2751] 수 정렬하기 2](https://soo-bak.github.io/algorithm/boj/SortingNumbers-2-75/)
