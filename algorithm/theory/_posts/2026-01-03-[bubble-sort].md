---
layout: single
title: "버블 정렬(Bubble Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 02:00:00 +0900"
description: 인접한 두 원소를 비교하며 정렬하는 버블 정렬 알고리듬의 원리, 구현 방법, 최적화 기법을 다룹니다
---

## 버블 정렬이란?

**버블 정렬(Bubble Sort)**은 인접한 두 원소를 비교하여 순서가 잘못되어 있으면 교환하는 과정을 반복하는 정렬 알고리듬입니다.

<br>

이름의 유래는 정렬 과정에서 큰 값이 배열의 끝으로 점점 **떠오르는(bubble up)** 모습에서 비롯되었습니다.

<br>

**동작 예시**

배열 `[5, 3, 8, 1]`을 정렬하는 과정:

```
1회차: [5, 3, 8, 1] → [3, 5, 8, 1] → [3, 5, 8, 1] → [3, 5, 1, 8]
2회차: [3, 5, 1, 8] → [3, 5, 1, 8] → [3, 1, 5, 8]
3회차: [3, 1, 5, 8] → [1, 3, 5, 8]
결과:  [1, 3, 5, 8]
```

각 회차가 끝날 때마다 가장 큰 값이 배열의 끝으로 이동합니다.

<br>

## 버블 정렬의 원리

버블 정렬은 다음과 같은 단계로 동작합니다:

<br>

**1. 첫 번째 패스**

배열의 처음부터 끝까지 인접한 두 원소를 비교합니다.

앞의 원소가 뒤의 원소보다 크면 두 원소를 교환합니다.

첫 번째 패스가 끝나면 **가장 큰 원소**가 배열의 마지막 위치로 이동합니다.

<br>

**2. 두 번째 패스**

마지막 원소를 제외하고 같은 과정을 반복합니다.

두 번째로 큰 원소가 뒤에서 두 번째 위치로 이동합니다.

<br>

**3. 반복**

정렬이 완료될 때까지 패스를 반복합니다.

<br>

**4. 종료**

더 이상 교환이 발생하지 않거나, n-1번의 패스가 완료되면 종료합니다.

<br>

## 버블 정렬의 구현

<br>

### 기본 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

void bubbleSort(vector<int>& arr) {
  int n = arr.size();

  for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - 1 - i; j++) {
      if (arr[j] > arr[j + 1]) {
        swap(arr[j], arr[j + 1]);
      }
    }
  }
}

int main() {
  vector<int> arr = {64, 34, 25, 12, 22, 11, 90};

  bubbleSort(arr);

  for (int x : arr) cout << x << " ";
  cout << "\n";

  return 0;
}
```

**출력**: `11 12 22 25 34 64 90`

<br>

### 최적화: 조기 종료

이미 정렬된 배열의 경우, 불필요한 반복을 줄일 수 있습니다.

```cpp
void bubbleSortOptimized(vector<int>& arr) {
  int n = arr.size();

  for (int i = 0; i < n - 1; i++) {
    bool swapped = false;  // 교환 발생 여부 추적

    for (int j = 0; j < n - 1 - i; j++) {
      if (arr[j] > arr[j + 1]) {
        swap(arr[j], arr[j + 1]);
        swapped = true;
      }
    }

    // 교환이 없으면 이미 정렬된 상태
    if (!swapped) break;
  }
}
```

이 최적화를 통해 이미 정렬된 배열은 $$O(n)$$에 처리할 수 있습니다.

<br>

### 추가 최적화: 마지막 교환 위치 기억

마지막으로 교환이 발생한 위치 이후는 이미 정렬되어 있습니다.

```cpp
void bubbleSortFurther(vector<int>& arr) {
  int n = arr.size();
  int lastSwap = n - 1;

  while (lastSwap > 0) {
    int newLastSwap = 0;

    for (int j = 0; j < lastSwap; j++) {
      if (arr[j] > arr[j + 1]) {
        swap(arr[j], arr[j + 1]);
        newLastSwap = j;
      }
    }

    lastSwap = newLastSwap;
  }
}
```

<br>

## 시간 복잡도

<br>

| 경우 | 시간 복잡도 | 설명 |
|------|------------|------|
| 최선 | $$O(n)$$ | 이미 정렬된 경우 (최적화 적용 시) |
| 평균 | $$O(n^2)$$ | 일반적인 경우 |
| 최악 | $$O(n^2)$$ | 역순으로 정렬된 경우 |

<br>

**공간 복잡도**: $$O(1)$$

추가 메모리가 거의 필요하지 않은 제자리 정렬입니다.

<br>

## 버블 정렬의 특징

<br>

### 장점

- **구현이 매우 간단**: 이해하기 쉽고 코드가 짧음
- **제자리 정렬**: 추가 메모리가 필요하지 않음
- **안정 정렬**: 같은 값의 상대적 순서가 유지됨
- **적응적**: 거의 정렬된 데이터에 효율적 (최적화 적용 시)

<br>

### 단점

- **비효율적**: 평균 및 최악 시간 복잡도가 $$O(n^2)$$
- **교환 횟수가 많음**: 다른 정렬에 비해 교환 연산이 많음
- **실용성 낮음**: 큰 데이터셋에는 부적합

<br>

## 다른 정렬과 비교

<br>

| 특성 | 버블 정렬 | 선택 정렬 | 삽입 정렬 |
|------|----------|----------|----------|
| 평균 시간 복잡도 | $$O(n^2)$$ | $$O(n^2)$$ | $$O(n^2)$$ |
| 최선 시간 복잡도 | $$O(n)$$ | $$O(n^2)$$ | $$O(n)$$ |
| 공간 복잡도 | $$O(1)$$ | $$O(1)$$ | $$O(1)$$ |
| 안정성 | 안정 | 불안정 | 안정 |
| 교환 횟수 | 많음 | 적음 | 중간 |
| 적응성 | 있음 | 없음 | 있음 |

<br>

> 참고: [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

<br>

## 활용 상황

버블 정렬이 적합한 경우:

<br>

**1. 교육 목적**

정렬 알고리듬의 기본 개념을 학습할 때 사용됩니다.

<br>

**2. 거의 정렬된 데이터**

최적화된 버블 정렬은 거의 정렬된 데이터에 효율적입니다.

<br>

**3. 작은 데이터셋**

원소 수가 매우 적은 경우 구현의 단순함이 장점이 됩니다.

<br>

**4. 안정 정렬이 필요한 경우**

같은 값의 상대적 순서를 유지해야 할 때 사용됩니다.

<br>

## 실전 예제: 정렬 과정 시각화

```cpp
#include <bits/stdc++.h>
using namespace std;

void printArray(const vector<int>& arr) {
  for (int x : arr) cout << x << " ";
  cout << "\n";
}

void bubbleSortVisualize(vector<int>& arr) {
  int n = arr.size();
  int pass = 1;

  for (int i = 0; i < n - 1; i++) {
    bool swapped = false;
    cout << "Pass " << pass++ << ": ";

    for (int j = 0; j < n - 1 - i; j++) {
      if (arr[j] > arr[j + 1]) {
        swap(arr[j], arr[j + 1]);
        swapped = true;
      }
    }

    printArray(arr);

    if (!swapped) {
      cout << "정렬 완료!\n";
      break;
    }
  }
}

int main() {
  vector<int> arr = {5, 1, 4, 2, 8};

  cout << "초기: ";
  printArray(arr);

  bubbleSortVisualize(arr);

  return 0;
}
```

**출력**:
```
초기: 5 1 4 2 8
Pass 1: 1 4 2 5 8
Pass 2: 1 2 4 5 8
Pass 3: 1 2 4 5 8
정렬 완료!
```

<br>

## 마무리

버블 정렬은 가장 단순한 정렬 알고리듬 중 하나입니다.

<br>

**핵심 포인트**
- **인접 원소 비교**: 인접한 두 원소를 비교하여 교환
- **버블 업**: 큰 값이 배열의 끝으로 점점 이동
- **시간 복잡도**: 평균 및 최악 $$O(n^2)$$, 최선 $$O(n)$$
- **안정 정렬**: 같은 값의 순서 유지

<br>

실무에서는 거의 사용되지 않지만, 정렬 알고리듬의 기초 개념을 이해하는 데 중요한 역할을 합니다.

더 효율적인 정렬이 필요하다면 [빠른 정렬](https://soo-bak.github.io/algorithm/theory/quick-sort/)이나 [병합 정렬](https://soo-bak.github.io/algorithm/theory/merge-sort/)을 고려하세요.

<br>

### 관련 글
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)

<br>

### 관련 문제
- [[백준 2750] 수 정렬하기](https://www.acmicpc.net/problem/2750)

