---
layout: single
title: "선택 정렬(Selection Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 03:00:00 +0900"
description: 배열에서 최솟값을 찾아 맨 앞으로 이동시키는 선택 정렬 알고리듬의 원리, 구현 방법, 특징을 다룹니다
---

## 선택 정렬이란?

**선택 정렬(Selection Sort)**은 배열에서 가장 작은(또는 가장 큰) 원소를 **선택**하여 앞으로 이동시키는 과정을 반복하는 정렬 알고리듬입니다.

<br>

**동작 예시**

배열 `[64, 25, 12, 22, 11]`을 오름차순으로 정렬하는 과정:

```
1회차: [64, 25, 12, 22, 11] → 최솟값 11 선택 → [11, 25, 12, 22, 64]
2회차: [11, 25, 12, 22, 64] → 최솟값 12 선택 → [11, 12, 25, 22, 64]
3회차: [11, 12, 25, 22, 64] → 최솟값 22 선택 → [11, 12, 22, 25, 64]
4회차: [11, 12, 22, 25, 64] → 최솟값 25 선택 → [11, 12, 22, 25, 64]
결과:  [11, 12, 22, 25, 64]
```

<br>

## 선택 정렬의 원리

선택 정렬은 다음과 같은 단계로 동작합니다:

<br>

**1. 최솟값 찾기**

정렬되지 않은 부분에서 최솟값을 찾습니다.

<br>

**2. 교환**

찾은 최솟값을 정렬되지 않은 부분의 첫 번째 원소와 교환합니다.

<br>

**3. 범위 축소**

정렬된 부분을 하나 늘리고, 정렬되지 않은 부분에서 같은 과정을 반복합니다.

<br>

**4. 종료**

모든 원소가 정렬될 때까지 반복합니다.

<br>

## 선택 정렬의 구현

<br>

### 기본 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

void selectionSort(vector<int>& arr) {
  int n = arr.size();

  for (int i = 0; i < n - 1; i++) {
    // 정렬되지 않은 부분에서 최솟값의 인덱스 찾기
    int minIdx = i;
    for (int j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }

    // 최솟값을 현재 위치로 이동
    if (minIdx != i) {
      swap(arr[i], arr[minIdx]);
    }
  }
}

int main() {
  vector<int> arr = {64, 25, 12, 22, 11};

  selectionSort(arr);

  for (int x : arr) cout << x << " ";
  cout << "\n";

  return 0;
}
```

**출력**: `11 12 22 25 64`

<br>

### 내림차순 정렬

최댓값을 선택하여 뒤로 이동시키는 방식:

```cpp
void selectionSortDesc(vector<int>& arr) {
  int n = arr.size();

  for (int i = 0; i < n - 1; i++) {
    int maxIdx = i;
    for (int j = i + 1; j < n; j++) {
      if (arr[j] > arr[maxIdx]) {
        maxIdx = j;
      }
    }

    if (maxIdx != i) {
      swap(arr[i], arr[maxIdx]);
    }
  }
}
```

<br>

### 양방향 선택 정렬

한 번의 패스에서 최솟값과 최댓값을 동시에 선택하는 최적화:

```cpp
void cocktailSelectionSort(vector<int>& arr) {
  int n = arr.size();
  int left = 0, right = n - 1;

  while (left < right) {
    int minIdx = left, maxIdx = right;

    for (int i = left; i <= right; i++) {
      if (arr[i] < arr[minIdx]) minIdx = i;
      if (arr[i] > arr[maxIdx]) maxIdx = i;
    }

    swap(arr[left], arr[minIdx]);

    // maxIdx가 left 위치에 있었다면, minIdx로 이동됨
    if (maxIdx == left) maxIdx = minIdx;

    swap(arr[right], arr[maxIdx]);

    left++;
    right--;
  }
}
```

<br>

## 시간 복잡도

<br>

| 경우 | 시간 복잡도 | 설명 |
|------|------------|------|
| 최선 | $$O(n^2)$$ | 이미 정렬되어도 모든 비교 수행 |
| 평균 | $$O(n^2)$$ | 일반적인 경우 |
| 최악 | $$O(n^2)$$ | 역순으로 정렬된 경우 |

<br>

**비교 횟수**: 항상 $$\frac{n(n-1)}{2}$$

**교환 횟수**: 최대 $$n-1$$번 (각 패스마다 한 번)

<br>

**공간 복잡도**: $$O(1)$$

추가 메모리가 거의 필요하지 않은 [제자리 정렬](https://soo-bak.github.io/algorithm/theory/in-place-sort/)입니다.

<br>

## 선택 정렬의 특징

<br>

### 장점

- **구현이 간단**: 이해하기 쉽고 코드가 짧음
- **제자리 정렬**: 추가 메모리가 필요하지 않음
- **교환 횟수가 적음**: 최대 $$n-1$$번의 교환만 수행
- **데이터 이동 최소화**: 교환 비용이 큰 경우 유리

<br>

### 단점

- **항상 $$O(n^2)$$**: 이미 정렬되어 있어도 모든 비교 수행
- **불안정 정렬**: 같은 값의 상대적 순서가 바뀔 수 있음
- **적응성 없음**: 입력 데이터의 상태에 관계없이 동일한 시간 소요

<br>

### 불안정 정렬 예시

```
입력: [(A, 3), (B, 3), (C, 1)]  (값으로 정렬)

1회차: C(1)이 최솟값 → A(3)과 교환 → [(C, 1), (B, 3), (A, 3)]

결과: B(3)과 A(3)의 순서가 바뀜 → 불안정
```

<br>

## 다른 정렬과 비교

<br>

| 특성 | 선택 정렬 | 버블 정렬 | 삽입 정렬 |
|------|----------|----------|----------|
| 평균 시간 복잡도 | $$O(n^2)$$ | $$O(n^2)$$ | $$O(n^2)$$ |
| 최선 시간 복잡도 | $$O(n^2)$$ | $$O(n)$$ | $$O(n)$$ |
| 공간 복잡도 | $$O(1)$$ | $$O(1)$$ | $$O(1)$$ |
| 안정성 | 불안정 | 안정 | 안정 |
| 교환 횟수 | $$O(n)$$ | $$O(n^2)$$ | $$O(n^2)$$ |
| 적응성 | 없음 | 있음 | 있음 |

<br>

**선택 정렬의 강점**: 교환 횟수가 적음

데이터 교환 비용이 큰 경우(예: 디스크의 큰 레코드)에는 선택 정렬이 유리할 수 있습니다.

<br>

## 활용 상황

선택 정렬이 적합한 경우:

<br>

**1. 교환 비용이 높은 경우**

데이터 이동 비용이 비교 비용보다 훨씬 큰 경우에 효율적입니다.

<br>

**2. 메모리 제약이 심한 경우**

추가 메모리가 전혀 필요하지 않습니다.

<br>

**3. 작은 데이터셋**

원소 수가 매우 적은 경우 구현의 단순함이 장점이 됩니다.

<br>

**4. 교육 목적**

정렬 알고리듬의 기본 개념을 학습할 때 사용됩니다.

<br>

## 실전 예제: 정렬 과정 시각화

```cpp
#include <bits/stdc++.h>
using namespace std;

void printArray(const vector<int>& arr, int sortedUntil) {
  for (int i = 0; i < arr.size(); i++) {
    if (i < sortedUntil) cout << "[" << arr[i] << "] ";
    else cout << arr[i] << " ";
  }
  cout << "\n";
}

void selectionSortVisualize(vector<int>& arr) {
  int n = arr.size();

  cout << "초기: ";
  printArray(arr, 0);

  for (int i = 0; i < n - 1; i++) {
    int minIdx = i;
    for (int j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }

    if (minIdx != i) {
      cout << "  → " << arr[i] << "와 " << arr[minIdx] << " 교환\n";
      swap(arr[i], arr[minIdx]);
    }

    cout << "Pass " << (i + 1) << ": ";
    printArray(arr, i + 1);
  }
}

int main() {
  vector<int> arr = {64, 25, 12, 22, 11};

  selectionSortVisualize(arr);

  return 0;
}
```

**출력**:
```
초기: 64 25 12 22 11
  → 64와 11 교환
Pass 1: [11] 25 12 22 64
  → 25와 12 교환
Pass 2: [11] [12] 25 22 64
  → 25와 22 교환
Pass 3: [11] [12] [22] 25 64
Pass 4: [11] [12] [22] [25] 64
```

<br>

## 안정적인 선택 정렬

불안정 정렬 문제를 해결하려면 교환 대신 삽입 방식을 사용합니다:

```cpp
void stableSelectionSort(vector<int>& arr) {
  int n = arr.size();

  for (int i = 0; i < n - 1; i++) {
    int minIdx = i;
    for (int j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }

    // 교환 대신 최솟값을 앞으로 밀어 넣기
    int minVal = arr[minIdx];
    while (minIdx > i) {
      arr[minIdx] = arr[minIdx - 1];
      minIdx--;
    }
    arr[i] = minVal;
  }
}
```

단, 이 방식은 교환 횟수가 증가하여 원래 선택 정렬의 장점이 사라집니다.

<br>

## 마무리

선택 정렬은 가장 직관적인 정렬 알고리듬 중 하나입니다.

<br>

**핵심 포인트**
- **최솟값 선택**: 정렬되지 않은 부분에서 최솟값을 선택
- **교환 횟수 최소**: 최대 $$n-1$$번의 교환만 수행
- **시간 복잡도**: 항상 $$O(n^2)$$ (입력에 관계없음)
- **불안정 정렬**: 같은 값의 순서가 바뀔 수 있음

<br>

실무에서는 거의 사용되지 않지만, 교환 비용이 매우 큰 특수한 상황에서는 고려할 수 있습니다.

더 효율적인 정렬이 필요하다면 [빠른 정렬](https://soo-bak.github.io/algorithm/theory/quick-sort/)이나 [병합 정렬](https://soo-bak.github.io/algorithm/theory/merge-sort/)을 사용하세요.

<br>

### 관련 글
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)

<br>

### 관련 문제
- [[백준 2750] 수 정렬하기](https://www.acmicpc.net/problem/2750)

