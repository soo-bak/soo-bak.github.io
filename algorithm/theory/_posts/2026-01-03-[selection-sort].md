---
layout: single
title: "선택 정렬(Selection Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 03:00:00 +0900"
description: 배열에서 최솟값을 찾아 맨 앞으로 이동시키는 선택 정렬 알고리듬의 원리, 구현 방법, 특징을 다룹니다
---

## 선택 정렬이란?

**선택 정렬(Selection Sort)**은 배열에서 가장 작은(또는 가장 큰) 원소를 **선택**하여 앞으로 이동시키는 과정을 반복하는 정렬 알고리듬입니다.

정렬되지 않은 부분에서 최솟값을 찾아 맨 앞 원소와 교환하고, 이 과정을 배열 끝까지 반복하면 정렬이 완료됩니다.

<br>

### 단계별 예시

배열 `[64, 25, 12, 22, 11]`을 오름차순으로 정렬하는 과정입니다:

```
초기: [64, 25, 12, 22, 11]

1회차: 최솟값 11 선택 → 64와 교환 → [11, 25, 12, 22, 64]
2회차: 최솟값 12 선택 → 25와 교환 → [11, 12, 25, 22, 64]
3회차: 최솟값 22 선택 → 25와 교환 → [11, 12, 22, 25, 64]
4회차: 최솟값 25 선택 → 이미 제자리 → [11, 12, 22, 25, 64]

결과: [11, 12, 22, 25, 64]
```

---

## 선택 정렬의 원리

선택 정렬은 다음과 같은 과정으로 동작합니다:

1. **최솟값 찾기**: 정렬되지 않은 부분에서 최솟값의 위치를 찾음
2. **교환**: 찾은 최솟값을 정렬되지 않은 부분의 첫 번째 원소와 교환
3. **범위 축소**: 정렬된 부분을 하나 늘리고, 남은 부분에서 같은 과정을 반복
4. **종료**: 모든 원소가 정렬될 때까지 반복

<br>

각 단계마다 정렬된 영역이 하나씩 늘어나며, $$n-1$$번의 반복 후 정렬이 완료됩니다.

---

## 구현

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
  // 출력: 11 12 22 25 64

  return 0;
}
```

<br>

### 내림차순 정렬

최댓값을 선택하여 앞으로 이동시키는 방식입니다:

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

---

## 시간 복잡도

선택 정렬의 시간 복잡도는 모든 경우에 동일합니다.

<br>

### 모든 경우 시간 복잡도: $$O(n^2)$$

이미 정렬된 배열이라도, 정렬되지 않은 부분에서 최솟값을 찾기 위해 모든 원소를 비교해야 합니다.

따라서 최선, 평균, 최악의 경우 모두 $$O(n^2)$$의 시간 복잡도를 가집니다.

<br>

**비교 횟수**: 항상 $$\frac{n(n-1)}{2}$$번

**교환 횟수**: 최대 $$n-1$$번 (매 순회마다 한 번)

<br>

### 공간 복잡도

$$O(1)$$입니다. 추가 메모리가 거의 필요하지 않은 제자리 정렬입니다.

> 참고: [제자리 정렬(In-place Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/in-place-sort/)

---

## 선택 정렬의 특징

### 장점

- **구현이 간단**: 이해하기 쉽고 코드가 짧음
- **제자리 정렬**: 추가 메모리가 필요하지 않음
- **교환 횟수가 적음**: 최대 $$n-1$$번의 교환만 수행

<br>

교환 비용이 큰 경우(예: 디스크의 큰 레코드)에는 이 특성이 유리합니다.

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

> 참고: [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

---

## 선택 정렬의 활용

선택 정렬이 적합한 경우는 다음과 같습니다:

<br>

### 1. 교환 비용이 높은 경우

데이터 이동 비용이 비교 비용보다 훨씬 큰 경우에 효율적입니다.

교환 횟수가 최대 $$n-1$$번으로 제한되기 때문입니다.

<br>

### 2. 메모리 제약이 심한 경우

추가 메모리가 전혀 필요하지 않습니다.

<br>

### 3. 작은 데이터셋

원소 수가 매우 적은 경우 구현의 단순함이 장점이 됩니다.

---

## 양방향 선택 정렬

한 번의 순회에서 최솟값과 최댓값을 동시에 선택하는 최적화 방법입니다.

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

반복 횟수가 절반으로 줄어들지만, 비교 횟수는 동일하므로 시간 복잡도는 여전히 $$O(n^2)$$입니다.

---

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

<br>

단, 이 방식은 이동 횟수가 증가하여 원래 선택 정렬의 장점이 사라집니다.

안정 정렬이 필요하다면 삽입 정렬이나 병합 정렬을 고려하는 것이 좋습니다.

---

## 마무리

선택 정렬은 가장 직관적인 정렬 알고리듬 중 하나입니다.

<br>

정렬되지 않은 부분에서 최솟값을 찾아 앞으로 이동시키는 단순한 방식으로, 교환 횟수가 최대 $$n-1$$번으로 제한된다는 특징이 있습니다.

<br>

모든 경우에 $$O(n^2)$$의 시간 복잡도를 가지므로 실무에서는 거의 사용되지 않지만, 교환 비용이 매우 큰 특수한 상황에서는 고려할 수 있습니다.

더 효율적인 정렬이 필요하다면 빠른 정렬이나 병합 정렬을 사용하면 됩니다.

<br>

**관련 글**:
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [버블 정렬(Bubble Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/bubble-sort/)
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2751] 수 정렬하기 2](https://soo-bak.github.io/algorithm/boj/SortingNumbers-2-75/)
