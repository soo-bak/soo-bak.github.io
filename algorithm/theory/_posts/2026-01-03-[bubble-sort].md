---
layout: single
title: "거품 정렬(Bubble Sort)의 원리와 구현 - soo:bak"
date: "2026-01-03 02:00:00 +0900"
description: 인접한 두 원소를 비교하며 정렬하는 거품 정렬 알고리듬의 원리, 구현 방법, 최적화 기법을 다룹니다
---

## 거품 정렬이란?

**거품 정렬(Bubble Sort)**은 인접한 두 원소를 비교하여 순서가 잘못되어 있으면 교환하는 과정을 반복하는 정렬 알고리듬입니다.

영어로 "Bubble Sort"라 불리는 이유는 정렬 과정에서 큰 값이 배열의 끝으로 점점 **떠오르는(bubble up)** 모습이 마치 거품이 수면 위로 올라오는 것과 같기 때문입니다.

<br>

예를 들어, 배열 `[5, 3, 8, 1]`을 정렬하는 과정을 살펴보겠습니다:

```
1회차: [5, 3, 8, 1] → [3, 5, 8, 1] → [3, 5, 8, 1] → [3, 5, 1, 8]
2회차: [3, 5, 1, 8] → [3, 5, 1, 8] → [3, 1, 5, 8]
3회차: [3, 1, 5, 8] → [1, 3, 5, 8]
결과:  [1, 3, 5, 8]
```

각 회차가 끝날 때마다 가장 큰 값이 배열의 끝으로 이동합니다.

---

## 거품 정렬의 원리

거품 정렬은 다음과 같은 단계로 동작합니다:

1. **첫 번째 순회**: 배열의 처음부터 끝까지 인접한 두 원소를 비교하고, 앞의 원소가 뒤의 원소보다 크면 교환합니다. 첫 번째 순회가 끝나면 **가장 큰 원소**가 배열의 마지막 위치로 이동합니다.

2. **두 번째 순회**: 마지막 원소를 제외하고 같은 과정을 반복합니다. 두 번째로 큰 원소가 뒤에서 두 번째 위치로 이동합니다.

3. **반복**: 정렬이 완료될 때까지 순회를 반복합니다.

4. **종료**: 더 이상 교환이 발생하지 않거나, `n-1`번의 순회가 완료되면 종료합니다.

---

## 구현

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

바깥 반복문은 순회 횟수를 제어하고, 안쪽 반복문은 인접한 원소를 비교합니다.

`n - 1 - i`로 범위를 제한하는 이유는 매 순회가 끝날 때마다 가장 큰 원소가 제자리를 찾기 때문입니다.

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

<br>

한 번의 순회 동안 교환이 한 번도 발생하지 않았다면, 배열은 이미 정렬된 상태입니다.

이 최적화를 적용하면 이미 정렬된 배열은 $$O(n)$$에 처리할 수 있습니다.

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

이 방식은 배열의 뒷부분이 일찍 정렬되는 경우 효과적입니다.

---

## 시간 복잡도

거품 정렬의 시간 복잡도는 다음과 같습니다:

- **최선**: $$O(n)$$ - 이미 정렬된 경우 (조기 종료 최적화 적용 시)
- **평균**: $$O(n^2)$$ - 일반적인 경우
- **최악**: $$O(n^2)$$ - 역순으로 정렬된 경우

<br>

**공간 복잡도**: $$O(1)$$

추가 메모리가 거의 필요하지 않은 제자리 정렬입니다.

> 참고: [제자리 정렬(In-place Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/in-place-sort/)

---

## 거품 정렬의 특징

거품 정렬은 구현이 매우 간단하고 직관적입니다. 코드가 짧아 이해하기 쉬우며, 추가 메모리가 필요하지 않은 제자리 정렬입니다.

<br>

또한 같은 값을 가진 원소들의 상대적 순서가 유지되는 **안정 정렬(Stable Sort)**입니다.

> 참고: [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

<br>

거의 정렬된 데이터에 대해서는 조기 종료 최적화를 적용하면 효율적으로 동작합니다.

<br>

그러나 평균 및 최악의 경우 시간 복잡도가 $$O(n^2)$$이고, 다른 정렬에 비해 교환 연산이 많아 큰 데이터셋에는 부적합합니다.

따라서 실무에서는 거의 사용되지 않으며, 더 효율적인 정렬이 필요하다면 병합 정렬이나 빠른 정렬을 고려해야 합니다.

---

## 활용 상황

거품 정렬이 적합한 경우는 다음과 같습니다:

<br>

**교육 목적**: 정렬 알고리듬의 기본 개념을 학습할 때 가장 먼저 접하게 되는 알고리듬입니다. 인접 원소 비교와 교환이라는 단순한 동작으로 정렬의 원리를 이해하기 좋습니다.

<br>

**거의 정렬된 데이터**: 조기 종료 최적화를 적용하면 거의 정렬된 데이터에 대해 $$O(n)$$에 가까운 성능을 보입니다.

<br>

**작은 데이터셋**: 원소 수가 매우 적은 경우 구현의 단순함이 오히려 장점이 됩니다.

---

## 실전 예제: 정렬 과정 시각화

거품 정렬의 동작을 확인하기 위한 시각화 코드입니다:

```cpp
#include <bits/stdc++.h>
using namespace std;

void printArray(const vector<int>& arr) {
  for (int x : arr) cout << x << " ";
  cout << "\n";
}

void bubbleSortVisualize(vector<int>& arr) {
  int n = arr.size();
  int round = 1;

  for (int i = 0; i < n - 1; i++) {
    bool swapped = false;
    cout << round++ << "회차: ";

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
1회차: 1 4 2 5 8
2회차: 1 2 4 5 8
3회차: 1 2 4 5 8
정렬 완료!
```

---

## 마무리

거품 정렬은 가장 단순한 정렬 알고리듬 중 하나로, 인접한 두 원소를 비교하여 교환하는 과정을 반복합니다.

<br>

평균 및 최악의 경우 $$O(n^2)$$의 시간 복잡도를 가지며, 실무에서는 거의 사용되지 않습니다.

하지만 정렬 알고리듬의 기초 개념을 이해하는 데 중요한 역할을 하며, 안정 정렬이자 제자리 정렬이라는 특성을 가집니다.

<br>

**관련 글**:
- [끼워넣기 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [선택 정렬(Selection Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/selection-sort/)
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
