---
layout: single
title: "제자리 정렬(In-place Sort)의 개념과 특성 - soo:bak"
date: "2025-10-26 06:00:00 +0900"
description: 추가 메모리를 최소화하는 제자리 정렬의 정의, 공간 복잡도 분석, 그리고 다양한 정렬 알고리듬의 제자리 여부를 다룹니다
---

## 제자리 정렬이란?

**제자리 정렬(In-place Sort)**은 원본 배열 내에서 정렬을 수행하여 **입력 크기에 비례하지 않는 추가 메모리만 사용**하는 정렬 방식입니다.

**비제자리 정렬(Not In-place Sort)**은 정렬 과정에서 입력 크기에 비례하는 추가 메모리가 필요합니다.

<br>

배열 `[5, 3, 8, 4, 9, 1]`을 정렬하는 두 가지 방식의 차이는 다음과 같습니다:

**제자리 정렬 (빠른 정렬)**:
```
초기: [5, 3, 8, 4, 9, 1]
 ↓ 배열 내부에서 교환
결과: [1, 3, 4, 5, 8, 9]
공간: O(1)
```

**비제자리 정렬 (병합 정렬)**:
```
초기: [5, 3, 8, 4, 9, 1]
 ↓ 크기 n의 임시 배열 필요
임시: [_, _, _, _, _, _]
결과: [1, 3, 4, 5, 8, 9]
공간: O(n)
```

---

## 제자리 정렬의 필요성

메모리 제약이 있는 환경에서는 제자리 정렬이 필수적입니다.

<br>

### 대용량 데이터 처리

시스템 메모리 `4GB`, 정렬 대상 배열 크기 `2GB`인 경우:

| 정렬 방식 | 원본 | 추가 메모리 | 총 메모리 | 상태 |
|---------|------|-----------|---------|------|
| 비제자리 | 2GB | 2GB | 4GB | 위험 |
| 제자리 | 2GB | ~0 | ~2GB | 안정 |

<br>

### 임베디드 시스템

메모리가 제한적인 IoT 기기나 임베디드 시스템에서의 메모리 사용:

```
센서 데이터 10,000개 (int 배열)
비제자리 정렬: 10,000 × 4 bytes × 2 = 80KB
제자리 정렬:   10,000 × 4 bytes × 1 = 40KB
```

메모리 제약이 심한 환경에서는 이 차이가 실행 가능 여부를 결정합니다.

<br>

### 멀티스레드 환경

여러 스레드가 동시에 정렬을 수행하는 경우:

```
10개 스레드, 각 100MB 배열 정렬
비제자리: 10 × 100MB × 2 = 2GB
제자리:   10 × 100MB × 1 = 1GB
```

동시성이 높은 환경에서 메모리 효율이 중요합니다.

---

## 정렬 알고리듬의 제자리 여부

주요 정렬 알고리듬을 공간 복잡도 기준으로 분류합니다.

<br>

### 제자리 정렬 알고리듬

| 알고리듬 | 추가 공간 복잡도 | 메모리 사용 |
|---------|---------------|-----------|
| 힙 정렬 | $$O(1)$$ | 상수 변수만 사용 |
| 삽입 정렬 | $$O(1)$$ | 상수 변수만 사용 |
| 선택 정렬 | $$O(1)$$ | 상수 변수만 사용 |
| 버블 정렬 | $$O(1)$$ | 상수 변수만 사용 |
| 빠른 정렬 | $$O(\log n)$$ | 재귀 호출 스택 |

<br>

### 비제자리 정렬 알고리듬

| 알고리듬 | 추가 공간 복잡도 | 메모리 사용 |
|---------|---------------|-----------|
| 병합 정렬 | $$O(n)$$ | 임시 배열 필요 |
| 계수 정렬 | $$O(k)$$ | 값 범위 크기 배열 |
| 기수 정렬 | $$O(n+k)$$ | 버킷과 임시 배열 |

<br>

> 참고: [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)

> 참고: [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)

> 참고: [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)

> 참고: [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)

---

## 공간 복잡도 분석

제자리 정렬은 입력 크기 $$n$$과 무관한 추가 메모리만 사용합니다.

<br>

### $$O(1)$$ 공간 복잡도

상수 개의 변수만 사용하는 경우입니다.

```cpp
void selectionSort(vector<int>& arr) {
  int n = arr.size();
  
  for (int i = 0; i < n - 1; i++) {
    int minIdx = i;
    
    for (int j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }
    
    swap(arr[i], arr[minIdx]);
  }
}
```

추가 메모리: `minIdx`, `i`, `j` 등 상수 개 → $$O(1)$$

<br>

### $$O(\log n)$$ 공간 복잡도

재귀 호출 스택을 사용하는 경우입니다.

```cpp
void quickSort(vector<int>& arr, int low, int high) {
  if (low < high) {
    int pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
}
```

| 메모리 유형 | 크기 |
|----------|------|
| 상수 변수 | $$O(1)$$ |
| 재귀 스택 (평균) | $$O(\log n)$$ |
| 재귀 스택 (최악) | $$O(n)$$ |

빠른 정렬은 평균 재귀 깊이가 $$O(\log n)$$이므로 제자리 정렬로 분류됩니다.

<br>

### $$O(n)$$ 공간 복잡도

입력 크기에 비례하는 추가 배열이 필요한 경우입니다.

```cpp
void merge(vector<int>& arr, int left, int mid, int right) {
  vector<int> temp(right - left + 1);
  
  // 병합 과정
  
  for (int i = 0; i < temp.size(); i++) {
    arr[left + i] = temp[i];
  }
}
```

추가 메모리: 크기 $$n$$의 임시 배열 → $$O(n)$$ (비제자리 정렬)

---

## 제자리 정렬 vs 비제자리 정렬

<br>

### 특성 비교

| 특성 | 제자리 정렬 | 비제자리 정렬 |
|------|----------|-------------|
| 메모리 사용 | $$O(1)$$ 또는 $$O(\log n)$$ | $$O(n)$$ |
| 대용량 데이터 | 유리 | 불리 |
| 안정 정렬 구현 | 어려움 | 용이 |
| 병렬화 | 상황 의존적 | 용이 |
| 원본 보존 | 불가 | 가능 |
| 캐시 효율 | 높음 | 변동 |

<br>

### 선택 기준

**제자리 정렬 사용**:
- 메모리 제약이 있는 환경
- 대용량 데이터 처리
- 원본 수정이 허용되는 경우
- 안정성이 불필요한 경우

**비제자리 정렬 사용**:
- 안정 정렬이 필수인 경우
- 원본 데이터 보존이 필요한 경우
- 메모리가 충분한 환경
- 병렬 처리가 중요한 경우

---

## 구현 예시

<br>

### 제자리 정렬: 버블 정렬

```cpp
void bubbleSort(vector<int>& arr) {
  int n = arr.size();
  
  for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        swap(arr[j], arr[j + 1]);
      }
    }
  }
}
```

추가 메모리: 상수 개의 변수 → $$O(1)$$

<br>

### 제자리 정렬: 힙 정렬

```cpp
void heapify(vector<int>& arr, int n, int i) {
  int largest = i;
  int left = 2 * i + 1;
  int right = 2 * i + 2;
  
  if (left < n && arr[left] > arr[largest]) {
    largest = left;
  }
  
  if (right < n && arr[right] > arr[largest]) {
    largest = right;
  }
  
  if (largest != i) {
    swap(arr[i], arr[largest]);
    heapify(arr, n, largest);
  }
}

void heapSort(vector<int>& arr) {
  int n = arr.size();
  
  for (int i = n / 2 - 1; i >= 0; i--) {
    heapify(arr, n, i);
  }
  
  for (int i = n - 1; i > 0; i--) {
    swap(arr[0], arr[i]);
    heapify(arr, i, 0);
  }
}
```

추가 메모리: 재귀 스택 → $$O(\log n)$$

<br>

### 비제자리 정렬: 병합 정렬

```cpp
void merge(vector<int>& arr, int left, int mid, int right) {
  vector<int> temp(right - left + 1);
  
  int i = left, j = mid + 1, k = 0;
  
  while (i <= mid && j <= right) {
    if (arr[i] <= arr[j]) {
      temp[k++] = arr[i++];
    } else {
      temp[k++] = arr[j++];
    }
  }
  
  while (i <= mid) temp[k++] = arr[i++];
  while (j <= right) temp[k++] = arr[j++];
  
  for (int idx = 0; idx < temp.size(); idx++) {
    arr[left + idx] = temp[idx];
  }
}
```

추가 메모리: 크기 $$n$$의 임시 배열 → $$O(n)$$

---

## 제자리 병합 정렬

병합 정렬을 제자리로 구현하는 것은 이론적으로 가능하지만 비효율적입니다.

<br>

### 회전 기반 병합

```cpp
void inPlaceMerge(vector<int>& arr, int left, int mid, int right) {
  int start2 = mid + 1;
  
  if (arr[mid] <= arr[start2]) {
    return;
  }
  
  while (left <= mid && start2 <= right) {
    if (arr[left] <= arr[start2]) {
      left++;
    } else {
      int value = arr[start2];
      int index = start2;
      
      while (index != left) {
        arr[index] = arr[index - 1];
        index--;
      }
      arr[left] = value;
      
      left++;
      mid++;
      start2++;
    }
  }
}
```

| 특성 | 값 |
|------|------|
| 시간 복잡도 | $$O(n^2)$$ |
| 공간 복잡도 | $$O(1)$$ |
| 실용성 | 낮음 |

일반적으로 병합 정렬은 $$O(n)$$ 추가 메모리를 사용하는 비제자리 구현을 사용합니다.

---

## 활용 사례

<br>

### 메모리 제약 환경

임베디드 시스템이나 메모리가 제한된 환경에서 사용됩니다.

```cpp
void sortSensorData(int* data, int size) {
  heapSort(data, size);  // O(1) 추가 메모리
}
```

<br>

### 외부 정렬의 블록 처리

대용량 파일을 정렬할 때 각 블록은 제자리 정렬로 처리합니다.

```cpp
void sortBlock(vector<int>& block) {
  quickSort(block, 0, block.size() - 1);  // O(log n) 추가 메모리
}
```

<br>

### 실시간 시스템

메모리 할당/해제 오버헤드를 피하기 위해 제자리 정렬을 사용합니다.

```cpp
void sortPriorities(Task* tasks, int count) {
  for (int i = 1; i < count; i++) {
    Task key = tasks[i];
    int j = i - 1;
    
    while (j >= 0 && tasks[j].priority > key.priority) {
      tasks[j + 1] = tasks[j];
      j--;
    }
    tasks[j + 1] = key;
  }
}
```

---

## 재귀 스택 최적화

빠른 정렬의 재귀 스택을 최소화하는 기법입니다.

<br>

### 꼬리 재귀 최적화

작은 부분은 재귀로, 큰 부분은 반복문으로 처리하여 스택 깊이를 줄입니다.

```cpp
void quickSortOptimized(vector<int>& arr, int low, int high) {
  while (low < high) {
    int pi = partition(arr, low, high);
    
    if (pi - low < high - pi) {
      quickSortOptimized(arr, low, pi - 1);
      low = pi + 1;
    } else {
      quickSortOptimized(arr, pi + 1, high);
      high = pi - 1;
    }
  }
}
```

최악의 경우에도 재귀 깊이를 $$O(\log n)$$으로 보장합니다.

---

## 마무리

제자리 정렬은 원본 배열 내에서 정렬을 수행하여 입력 크기에 비례하지 않는 추가 메모리만 사용하는 정렬 방식입니다.

<br>

공간 복잡도가 $$O(1)$$ 또는 $$O(\log n)$$인 정렬을 제자리 정렬로 분류하며,

힙 정렬, 빠른 정렬, 삽입 정렬 등이 대표적입니다.

병합 정렬은 $$O(n)$$의 추가 메모리가 필요하여 비제자리 정렬입니다.

<br>

메모리 제약 환경, 대용량 데이터 처리, 실시간 시스템에서 제자리 정렬이 필수적이며,

안정 정렬이나 원본 보존이 필요한 경우 비제자리 정렬을 고려해야 합니다.

<br>

**관련 글**:
- [안정 정렬(Stable Sort)의 개념과 특성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)
- [병합 정렬(Merge Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/merge-sort/)
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2751] 수 정렬하기 2](https://soo-bak.github.io/algorithm/boj/SortingNumbers-2-75/)
- [[백준 11931] 수 정렬하기 4](https://soo-bak.github.io/algorithm/boj/sortdesc-44/)

