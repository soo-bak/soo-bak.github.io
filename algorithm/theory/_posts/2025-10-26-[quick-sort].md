---
layout: single
title: "빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak"
date: "2025-10-26 01:00:00 +0900"
description: 분할 정복을 이용한 빠른 정렬의 원리, 구현 방법, 시간 복잡도, 최적화 기법을 다룹니다
---

## 빠른 정렬이란?

정렬되지 않은 배열 `[5, 3, 8, 4, 9, 1, 6, 2, 7]`이 있을 때, 이를 정렬하는 방법은 여러 가지가 있습니다.

하나씩 비교하며 정렬할 수도 있고, 병합 정렬처럼 분할한 후 합칠 수도 있습니다.

<br>

**빠른 정렬(Quick Sort)**은 **분할 정복**을 활용하는 정렬 알고리듬으로, 실전에서 가장 빠른 성능을 보이는 정렬 방법 중 하나입니다.

배열에서 **피벗(Pivot)**을 선택한 후, 피벗보다 작은 원소는 왼쪽, 큰 원소는 오른쪽으로 분할하고, 각 부분을 재귀적으로 정렬하는 방식으로 동작합니다.

---

## 빠른 정렬의 원리

빠른 정렬은 다음과 같은 과정으로 동작합니다:

1. **피벗 선택**: 배열에서 기준이 될 피벗을 선택
2. **분할**: 피벗보다 작은 원소는 왼쪽, 큰 원소는 오른쪽으로 분할
3. **재귀 정렬**: 분할된 각 부분 배열에 대해 1~2번 과정 반복
4. **종료**: 부분 배열의 크기가 1 이하가 되면 정렬 완료

<br>

### 단계별 예시

배열 `[5, 3, 8, 4, 9, 1, 6, 2, 7]`을 정렬하는 과정 (피벗: 맨 오른쪽 원소):

**1단계**: 피벗 `7`을 기준으로 분할
- `7`보다 작은 원소: `[5, 3, 4, 1, 6, 2]`
- 피벗: `[7]`
- `7`보다 큰 원소: `[8, 9]`

**2단계**: 왼쪽 부분 `[5, 3, 4, 1, 6, 2]`를 피벗 `2`로 분할
- `2`보다 작은 원소: `[1]`
- 피벗: `[2]`
- `2`보다 큰 원소: `[5, 3, 4, 6]`

**3단계**: 이 과정을 재귀적으로 반복
- 최종 결과: `[1, 2, 3, 4, 5, 6, 7, 8, 9]`

각 단계에서 피벗의 위치가 확정되며, 재귀 호출을 통해 정렬이 완료됩니다.

---

## 분할(Partition) 과정

빠른 정렬의 핵심은 피벗을 기준으로 배열을 두 부분으로 나누는 **분할** 과정입니다.

분할 방법에는 여러 가지가 있으며, 대표적으로 **로무토 분할(Lomuto Partition)**과 **호어 분할(Hoare Partition)**이 있습니다.

<br>

### 로무토 분할 (Lomuto Partition)

로무토 분할은 구현이 간단하고 직관적인 방법입니다.

```cpp
int partition(vector<int>& arr, int low, int high) {
  int pivot = arr[high];  // 맨 오른쪽을 피벗으로 선택
  int i = low - 1;  // 작은 원소들의 마지막 인덱스
  
  for (int j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++;
      swap(arr[i], arr[j]);  // 작은 원소를 왼쪽으로 이동
    }
  }
  
  swap(arr[i + 1], arr[high]);  // 피벗을 중간 위치로 이동
  return i + 1;  // 피벗의 최종 위치
}
```

<br>

### 호어 분할 (Hoare Partition)

호어 분할은 빠른 정렬이 처음 고안될 때 사용된 방법으로, 로무토 분할보다 평균적으로 교환 횟수가 적어 효율적입니다.

```cpp
int hoarePartition(vector<int>& arr, int low, int high) {
  int pivot = arr[low];  // 맨 왼쪽을 피벗으로 선택
  int i = low - 1;
  int j = high + 1;
  
  while (true) {
    do { i++; } while (arr[i] < pivot);
    do { j--; } while (arr[j] > pivot);
    
    if (i >= j) return j;
    swap(arr[i], arr[j]);
  }
}
```

---

## 구현

### 기본 구현 (로무토 분할)

```cpp
#include <bits/stdc++.h>
using namespace std;

int partition(vector<int>& arr, int low, int high) {
  int pivot = arr[high];
  int i = low - 1;
  
  for (int j = low; j < high; j++) {
    if (arr[j] < pivot) {
      i++;
      swap(arr[i], arr[j]);
    }
  }
  
  swap(arr[i + 1], arr[high]);
  return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
  if (low < high) {
    int pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
}

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  
  quickSort(arr, 0, arr.size() - 1);
  
  for (int x : arr) cout << x << " ";
  cout << "\n";
  
  return 0;
}
```

<br>

### 호어 분할 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

int hoarePartition(vector<int>& arr, int low, int high) {
  int pivot = arr[low];
  int i = low - 1;
  int j = high + 1;
  
  while (true) {
    do { i++; } while (arr[i] < pivot);
    do { j--; } while (arr[j] > pivot);
    
    if (i >= j) return j;
    swap(arr[i], arr[j]);
  }
}

void quickSort(vector<int>& arr, int low, int high) {
  if (low < high) {
    int pi = hoarePartition(arr, low, high);
    quickSort(arr, low, pi);
    quickSort(arr, pi + 1, high);
  }
}

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  quickSort(arr, 0, arr.size() - 1);
  
  for (int x : arr) cout << x << " ";
  cout << "\n";
  
  return 0;
}
```

---

## 시간 복잡도

빠른 정렬의 시간 복잡도는 피벗 선택에 따라 달라집니다.

<br>

### 평균 시간 복잡도: $$O(n \log n)$$

피벗이 배열을 균등하게 분할하는 경우, 각 레벨에서 $$O(n)$$의 비교 연산이 수행되고, 재귀 깊이는 $$O(\log n)$$이 됩니다.

$$
T(n) = 2T(n/2) + O(n) = O(n \log n)
$$

<br>

### 최선 시간 복잡도: $$O(n \log n)$$

피벗이 항상 배열을 정확히 절반으로 나누는 경우로, 평균 경우와 동일합니다.

<br>

### 최악 시간 복잡도: $$O(n^2)$$

피벗이 항상 최소값 또는 최대값으로 선택되는 경우입니다.

예를 들어, 이미 정렬된 배열에서 항상 맨 오른쪽을 피벗으로 선택하면 재귀 깊이가 $$O(n)$$이 되어 전체 시간 복잡도가 $$O(n^2)$$가 됩니다.

<br>

### 공간 복잡도

- **재귀 호출 스택**: $$O(\log n)$$ (평균), $$O(n)$$ (최악)
- **추가 공간**: $$O(1)$$ (제자리 정렬이므로 추가 배열 불필요)

---

## 최적화 기법

빠른 정렬의 성능을 개선하기 위한 다양한 최적화 기법이 있습니다.

<br>

### 1) 랜덤 피벗 선택

피벗을 무작위로 선택하여 최악의 경우를 확률적으로 회피하는 방법입니다.

이미 정렬된 배열에서 항상 맨 오른쪽을 피벗으로 선택하면 매번 최악의 분할이 발생하지만, 랜덤하게 선택하면 지속적으로 나쁜 피벗이 선택될 확률이 극히 낮아집니다.

$$n$$개의 원소 중 최선의 분할을 하는 피벗(중간 50% 범위)이 선택될 확률은 약 50%이며, 이는 평균적으로 $$O(n \log n)$$의 성능을 기대할 수 있게 합니다.

특히 악의적으로 설계된 입력 데이터에 대해서도 효과적으로 대응할 수 있다는 장점이 있습니다.

```cpp
int randomPartition(vector<int>& arr, int low, int high) {
  int randomIndex = low + rand() % (high - low + 1);
  swap(arr[randomIndex], arr[high]);
  return partition(arr, low, high);
}
```

<br>

### 2) 중간값 피벗 선택 (Median-of-Three)

배열의 첫 번째, 중간, 마지막 원소 중 중간값을 피벗으로 선택하는 방법입니다.

단순히 한 위치의 값을 선택하는 것보다 균등한 분할 가능성이 높습니다.

```cpp
int medianOfThree(vector<int>& arr, int low, int high) {
  int mid = low + (high - low) / 2;
  
  if (arr[low] > arr[mid]) swap(arr[low], arr[mid]);
  if (arr[low] > arr[high]) swap(arr[low], arr[high]);
  if (arr[mid] > arr[high]) swap(arr[mid], arr[high]);
  
  swap(arr[mid], arr[high]);
  return partition(arr, low, high);
}
```

<br>

### 3) 작은 배열에 삽입 정렬 사용

배열의 크기가 충분히 작을 때는 재귀 오버헤드보다 단순한 삽입 정렬이 더 빠릅니다.

일정 크기 이하의 부분 배열에 대해서는 삽입 정렬로 전환하여 성능을 개선할 수 있습니다.

```cpp
void quickSort(vector<int>& arr, int low, int high) {
  const int THRESHOLD = 10;
  
  if (high - low < THRESHOLD) {
    insertionSort(arr, low, high);
  }
  else if (low < high) {
    int pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
}
```

<br>

### 4) 3-Way 빠른 정렬 (3-Way Quick Sort)

중복된 값이 많은 배열에서 효율적인 방법입니다.

피벗과 같은 값들을 별도로 처리하여, 분할을 `피벗보다 작음`, `피벗과 같음`, `피벗보다 큼` 세 부분으로 나눕니다.

```cpp
void quickSort3Way(vector<int>& arr, int low, int high) {
  if (low >= high) return;
  
  int lt = low;
  int gt = high;
  int i = low + 1;
  int pivot = arr[low];
  
  while (i <= gt) {
    if (arr[i] < pivot) {
      swap(arr[lt++], arr[i++]);
    }
    else if (arr[i] > pivot) {
      swap(arr[i], arr[gt--]);
    }
    else {
      i++;
    }
  }
  
  quickSort3Way(arr, low, lt - 1);
  quickSort3Way(arr, gt + 1, high);
}
```

---

## 빠른 정렬의 특징

빠른 정렬은 다음과 같은 특징을 가집니다.

<br>

### 장점

- **실전 성능**: 평균적으로 가장 빠른 정렬 알고리듬 중 하나로, 실제 응용에서 널리 사용됨
- **제자리 정렬**: 추가 메모리가 거의 필요하지 않아 메모리 효율적
- **캐시 효율성**: 연속된 메모리 접근으로 캐시 적중률이 높음

<br>

### 단점

- **불안정 정렬**: 같은 값을 가진 원소들의 상대적 순서가 보장되지 않음
- **최악의 경우 성능 저하**: 피벗 선택이 불균등하면 $$O(n^2)$$의 시간 복잡도
- **재귀 스택 사용**: 재귀 깊이가 깊어지면 스택 오버플로우 위험

<br>

### 다른 정렬과 비교

| 특성 | 빠른 정렬 | 병합 정렬 | 힙 정렬 |
|------|---------|----------|---------|
| 평균 시간 복잡도 | $$O(n \log n)$$ | $$O(n \log n)$$ | $$O(n \log n)$$ |
| 최악 시간 복잡도 | $$O(n^2)$$ | $$O(n \log n)$$ | $$O(n \log n)$$ |
| 공간 복잡도 | $$O(\log n)$$ | $$O(n)$$ | $$O(1)$$ |
| 안정성 | 불안정 | 안정 | 불안정 |
| 제자리 정렬 | O | X | O |
| 실전 성능 | 가장 빠름 | 빠름 | 보통 |

---

## C++ STL의 sort 함수

C++ 표준 라이브러리의 `std::sort`는 **인트로 정렬(Introsort)**을 사용합니다.

<br>

인트로 정렬은 빠른 정렬을 기본으로 사용하되, 다음과 같은 최적화를 적용합니다:
- 재귀 깊이가 $$2 \log n$$을 초과하면 **힙 정렬**로 전환하여 최악의 경우 방지
- 작은 부분 배열에는 **삽입 정렬** 사용
- 이를 통해 평균 $$O(n \log n)$$, 최악의 경우에도 $$O(n \log n)$$ 보장

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  
  // 오름차순 정렬
  sort(arr.begin(), arr.end());
  
  // 내림차순 정렬
  sort(arr.begin(), arr.end(), greater<int>());
  
  return 0;
}
```

---

## 마무리

빠른 정렬은 분할 정복을 활용하는 정렬 알고리듬으로, 평균 $$O(n \log n)$$의 시간 복잡도를 가집니다.

피벗을 기준으로 배열을 분할하고 재귀적으로 정렬하는 방식으로 동작하며, 실전에서 가장 빠른 성능을 보이는 정렬 방법 중 하나입니다.

<br>

로무토 분할과 호어 분할 등 다양한 분할 방법이 있으며, 랜덤 피벗이나 중간값 피벗 선택, 작은 배열에 삽입 정렬 사용 등의 최적화 기법을 통해 성능을 개선할 수 있습니다.

<br>

제자리 정렬로 메모리 효율이 좋고 캐시 지역성이 뛰어나 실전에서 우수한 성능을 발휘합니다.

다만 최악의 경우 $$O(n^2)$$의 시간 복잡도를 가지므로, 모든 경우에 $$O(n \log n)$$을 보장해야 한다면 병합 정렬이나 힙 정렬을 고려할 수 있습니다.

<br>

**관련 글**:
- [이분 탐색(Binary Search)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/binary-search/)
- [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)
- [동적 계획법(Dynamic Programming)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2752] 세수정렬](https://soo-bak.github.io/algorithm/boj/sortThreeNumbers-4/)
- [[백준 11004] K번째 수](https://soo-bak.github.io/algorithm/boj/kthnum-53/)
- [[백준 11931] 수 정렬하기 4](https://soo-bak.github.io/algorithm/boj/sortdesc-44/)
- [[백준 1181] 단어 정렬](https://soo-bak.github.io/algorithm/boj/SortingWord-20/)
