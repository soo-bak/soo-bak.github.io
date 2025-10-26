---
layout: single
title: "퀵 정렬(Quick Sort)의 원리와 구현 - soo:bak"
date: "2025-10-26 01:00:00 +0900"
description: 분할 정복을 이용한 효율적인 정렬 알고리듬인 퀵 정렬의 원리, 구현 방법, 시간 복잡도, 최적화 기법을 다룹니다
---

## 퀵 정렬이란?

`10,000`개의 무작위로 섞인 숫자를 정렬해야 한다고 가정해보겠습니다.

단순 비교 정렬은 $$O(n^2)$$의 시간이 소요되지만, 분할 정복을 활용하면 평균 $$O(n \log n)$$으로 훨씬 빠르게 정렬할 수 있습니다.

<br>

**퀵 정렬(Quick Sort)**은 분할 정복(Divide and Conquer) 전략을 사용하는 정렬 알고리듬으로, **피벗(Pivot)**을 기준으로 배열을 분할하여 정렬합니다.

1961년 영국의 컴퓨터 과학자 토니 호어(Tony Hoare)가 개발했으며, 이름처럼 실전에서 매우 빠른 성능을 보여주는 대표적인 정렬 알고리듬입니다.

---

## 퀵 정렬의 원리

퀵 정렬은 다음과 같은 과정으로 동작합니다:

1. **피벗 선택**: 배열에서 하나의 원소를 피벗으로 선택
2. **분할(Partition)**: 피벗보다 작은 원소는 왼쪽, 큰 원소는 오른쪽으로 이동
3. **재귀 호출**: 분할된 두 부분 배열에 대해 퀵 정렬을 재귀적으로 수행
4. **종료 조건**: 부분 배열의 크기가 1 이하가 되면 정렬 완료

<br>

### 단계별 예시

배열 `[5, 3, 8, 4, 9, 1, 6, 2, 7]`을 정렬하는 과정 (피벗: 맨 오른쪽 원소):

**1단계**: 피벗 `7`을 기준으로 분할
- `7`보다 작은 원소: `[5, 3, 4, 1, 6, 2]`
- 피벗: `[7]`
- `7`보다 큰 원소: `[8, 9]`
- 결과: `[5, 3, 4, 1, 6, 2, 7, 8, 9]`

**2단계**: 왼쪽 부분 `[5, 3, 4, 1, 6, 2]`를 피벗 `2`로 분할
- `2`보다 작은 원소: `[1]`
- 피벗: `[2]`
- `2`보다 큰 원소: `[5, 3, 4, 6]`
- 결과: `[1, 2, 5, 3, 4, 6]`

**3단계**: 이 과정을 재귀적으로 반복
- 최종 결과: `[1, 2, 3, 4, 5, 6, 7, 8, 9]`

각 단계에서 피벗의 최종 위치가 확정되며, 점진적으로 정렬이 완성됩니다.

---

## 분할(Partition) 알고리듬

퀵 정렬의 핵심은 **분할(Partition)** 과정입니다.

피벗을 기준으로 배열을 효율적으로 분할하는 방법은 여러 가지가 있으며, 가장 일반적인 것은 **호어 분할(Hoare Partition)**과 **로무토 분할(Lomuto Partition)**입니다.

<br>

### 로무토 분할 (Lomuto Partition)

구현이 간단하고 이해하기 쉬운 방법입니다.

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

**동작 원리**:
- `i`는 피벗보다 작은 원소들의 경계를 표시
- 피벗보다 작은 원소를 만날 때마다 `i`를 증가시키고 해당 위치로 이동
- 마지막에 피벗을 중간 위치로 이동

<br>

### 호어 분할 (Hoare Partition)

원래 퀵 정렬에서 사용된 방법으로, 더 효율적입니다.

```cpp
int hoarePartition(vector<int>& arr, int low, int high) {
  int pivot = arr[low];  // 맨 왼쪽을 피벗으로 선택
  int i = low - 1;
  int j = high + 1;
  
  while (true) {
    // 피벗보다 큰 원소 찾기
    do {
      i++;
    } while (arr[i] < pivot);
    
    // 피벗보다 작은 원소 찾기
    do {
      j--;
    } while (arr[j] > pivot);
    
    if (i >= j) {
      return j;  // 분할 완료
    }
    
    swap(arr[i], arr[j]);  // 교환
  }
}
```

**장점**:
- 평균적으로 교환 횟수가 3배 정도 적음
- 같은 값이 많을 때 더 효율적

---

## 구현

### 기본 구현 (로무토 분할)

가장 이해하기 쉬운 형태입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

// 분할 함수
int partition(vector<int>& arr, int low, int high) {
  int pivot = arr[high];  // 피벗 선택
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

// 퀵 정렬 재귀 함수
void quickSort(vector<int>& arr, int low, int high) {
  if (low < high) {
    // 분할하여 피벗의 위치 확정
    int pi = partition(arr, low, high);
    
    // 피벗을 기준으로 양쪽 재귀 호출
    quickSort(arr, low, pi - 1);   // 왼쪽 부분 배열
    quickSort(arr, pi + 1, high);  // 오른쪽 부분 배열
  }
}

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  
  cout << "정렬 전: ";
  for (int x : arr) cout << x << " ";
  cout << "\n";
  
  quickSort(arr, 0, arr.size() - 1);
  
  cout << "정렬 후: ";
  for (int x : arr) cout << x << " ";
  cout << "\n";
  
  return 0;
}
```

<br>

### 호어 분할 구현

더 효율적인 구현입니다.

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

void quickSortHoare(vector<int>& arr, int low, int high) {
  if (low < high) {
    int pi = hoarePartition(arr, low, high);
    quickSortHoare(arr, low, pi);      // 왼쪽
    quickSortHoare(arr, pi + 1, high); // 오른쪽
  }
}

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  quickSortHoare(arr, 0, arr.size() - 1);
  
  for (int x : arr) cout << x << " ";
  cout << "\n";
  
  return 0;
}
```

---

## 시간 복잡도

### 평균 시간 복잡도: $$O(n \log n)$$

피벗이 배열을 균등하게 분할하는 경우, 각 레벨에서 $$O(n)$$의 비교 연산이 수행되고, 재귀 깊이가 $$O(\log n)$$이 됩니다.

$$
T(n) = 2T(n/2) + O(n) = O(n \log n)
$$

<br>

### 최선 시간 복잡도: $$O(n \log n)$$

피벗이 항상 중간값을 선택하여 배열을 정확히 절반으로 나누는 경우입니다.

<br>

### 최악 시간 복잡도: $$O(n^2)$$

피벗이 항상 최소값 또는 최대값이 선택되는 경우, 배열이 한쪽으로만 분할됩니다.

예를 들어, 이미 정렬된 배열 `[1, 2, 3, 4, 5]`에서 항상 맨 오른쪽을 피벗으로 선택하면:
- 1단계: `[]` + `5` + `[1, 2, 3, 4]`
- 2단계: `[]` + `4` + `[1, 2, 3]`
- ...

재귀 깊이가 $$O(n)$$이 되어 전체 시간 복잡도가 $$O(n^2)$$가 됩니다.

<br>

### 공간 복잡도

- 재귀 호출 스택: $$O(\log n)$$ (평균), $$O(n)$$ (최악)
- 제자리 정렬(In-place Sort)이므로 추가 배열 불필요

---

## 최적화 기법

### 1) 랜덤 피벗 선택

피벗을 무작위로 선택하여 최악의 경우를 회피합니다.

```cpp
int randomPartition(vector<int>& arr, int low, int high) {
  // 무작위 인덱스 선택
  int randomIndex = low + rand() % (high - low + 1);
  swap(arr[randomIndex], arr[high]);  // 맨 오른쪽으로 이동
  
  return partition(arr, low, high);
}
```

<br>

### 2) 중간값 피벗 (Median-of-Three)

배열의 첫 번째, 중간, 마지막 원소 중 중간값을 피벗으로 선택합니다.

```cpp
int medianOfThree(vector<int>& arr, int low, int high) {
  int mid = low + (high - low) / 2;
  
  // 세 값을 정렬하여 중간값을 중간 위치로
  if (arr[low] > arr[mid]) swap(arr[low], arr[mid]);
  if (arr[low] > arr[high]) swap(arr[low], arr[high]);
  if (arr[mid] > arr[high]) swap(arr[mid], arr[high]);
  
  swap(arr[mid], arr[high]);  // 중간값을 피벗 위치로
  return partition(arr, low, high);
}
```

<br>

### 3) 작은 배열에는 삽입 정렬 사용

배열의 크기가 작을 때는 삽입 정렬이 더 빠릅니다.

```cpp
void quickSortOptimized(vector<int>& arr, int low, int high) {
  const int THRESHOLD = 10;  // 임계값
  
  if (high - low < THRESHOLD) {
    // 삽입 정렬 사용
    insertionSort(arr, low, high);
  }
  else if (low < high) {
    int pi = partition(arr, low, high);
    quickSortOptimized(arr, low, pi - 1);
    quickSortOptimized(arr, pi + 1, high);
  }
}
```

<br>

### 4) 3-Way 퀵 정렬 (Dijkstra)

중복된 값이 많을 때 효율적입니다.

```cpp
void quickSort3Way(vector<int>& arr, int low, int high) {
  if (low >= high) return;
  
  int lt = low;        // 피벗보다 작은 부분의 끝
  int gt = high;       // 피벗보다 큰 부분의 시작
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
      i++;  // 피벗과 같으면 그대로
    }
  }
  
  quickSort3Way(arr, low, lt - 1);
  quickSort3Way(arr, gt + 1, high);
}
```

---

## 퀵 정렬의 특징

### 장점

1. **평균 성능이 우수**: 실전에서 가장 빠른 정렬 알고리듬 중 하나
2. **제자리 정렬**: 추가 메모리가 거의 필요 없음
3. **캐시 효율성**: 연속된 메모리 접근으로 캐시 적중률이 높음
4. **간결한 구현**: 코드가 비교적 간단함

<br>

### 단점

1. **불안정 정렬(Unstable Sort)**: 같은 값의 순서가 보장되지 않음
2. **최악의 경우 느림**: 피벗 선택이 나쁘면 $$O(n^2)$$
3. **재귀 스택**: 재귀 깊이가 깊어지면 스택 오버플로우 위험

<br>

### 다른 정렬과 비교

| 특성 | 퀵 정렬 | 병합 정렬 | 힙 정렬 |
|------|---------|----------|---------|
| 평균 시간 복잡도 | $$O(n \log n)$$ | $$O(n \log n)$$ | $$O(n \log n)$$ |
| 최악 시간 복잡도 | $$O(n^2)$$ | $$O(n \log n)$$ | $$O(n \log n)$$ |
| 공간 복잡도 | $$O(\log n)$$ | $$O(n)$$ | $$O(1)$$ |
| 안정성 | 불안정 | 안정 | 불안정 |
| 제자리 정렬 | O | X | O |
| 실전 성능 | 가장 빠름 | 빠름 | 보통 |

---

## 실전 활용

### C++ STL의 sort 함수

C++ 표준 라이브러리의 `std::sort`는 **인트로 정렬(Introsort)**을 사용합니다.

인트로 정렬은:
- 기본적으로 퀵 정렬 사용
- 재귀 깊이가 $$2 \log n$$을 초과하면 힙 정렬로 전환
- 작은 부분 배열에는 삽입 정렬 사용

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  
  // 오름차순 정렬
  sort(arr.begin(), arr.end());
  
  // 내림차순 정렬
  sort(arr.begin(), arr.end(), greater<int>());
  
  // 사용자 정의 비교 함수
  sort(arr.begin(), arr.end(), [](int a, int b) {
    return a > b;
  });
  
  return 0;
}
```

<br>

### 언제 퀵 정렬을 사용할까?

- **일반적인 정렬**: 평균 성능이 가장 좋으므로 기본 선택
- **제자리 정렬 필요**: 메모리가 제한적인 환경
- **안정성 불필요**: 같은 값의 순서가 중요하지 않을 때

<br>

**다른 정렬 고려**:
- **안정 정렬 필요**: 병합 정렬 사용
- **최악의 경우 보장**: 병합 정렬 또는 힙 정렬 사용
- **거의 정렬된 데이터**: 삽입 정렬 또는 팀 정렬 사용

---

## 마무리

퀵 정렬은 분할 정복 전략을 활용한 효율적인 정렬 알고리듬으로, 평균적으로 $$O(n \log n)$$의 시간 복잡도를 가집니다.

피벗 선택 방법과 분할 알고리듬에 따라 다양한 변형이 존재하며, 실전에서는 랜덤 피벗이나 중간값 피벗을 사용하여 최악의 경우를 회피합니다.

<br>

제자리 정렬로 메모리 효율이 좋고, 캐시 지역성이 뛰어나 실전에서 가장 빠른 성능을 보이는 정렬 알고리듬 중 하나입니다.

다만 최악의 경우 $$O(n^2)$$의 시간 복잡도를 가지므로, 최악의 경우에도 $$O(n \log n)$$을 보장해야 한다면 병합 정렬이나 힙 정렬을 고려하는 것이 좋습니다.

<br>

**관련 글**:
- [이분 탐색(Binary Search)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/binary-search/)
- [그리디 알고리듬(Greedy Algorithm, 탐욕법)의 원리와 적용 - soo:bak](https://soo-bak.github.io/algorithm/theory/greedyAlgo/)
- [동적 계획법(Dynamic Programming)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://www.acmicpc.net/problem/2750)
- [[백준 2752] 세수정렬](https://www.acmicpc.net/problem/2752)
- [[백준 11004] K번째 수](https://www.acmicpc.net/problem/11004)
- [[백준 11931] 수 정렬하기 4](https://www.acmicpc.net/problem/11931)
- [[백준 1181] 단어 정렬](https://www.acmicpc.net/problem/1181)

