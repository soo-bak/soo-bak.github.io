---
layout: single
title: "병합 정렬(Merge Sort)의 원리와 구현 - soo:bak"
date: "2025-10-26 04:00:00 +0900"
description: 분할 정복과 병합을 이용한 병합 정렬의 원리, 구현 방법, 시간 복잡도, 그리고 다양한 활용 방법을 다룹니다
---

## 병합 정렬이란?

**병합 정렬(Merge Sort)**은 **분할 정복(Divide and Conquer)** 전략을 활용하는 정렬 알고리듬입니다.

배열을 절반으로 나누어 각각을 정렬한 후, 정렬된 두 부분을 하나로 합치는 방식으로 동작합니다.

모든 경우에 $$O(n \log n)$$의 시간 복잡도를 보장하며, **안정 정렬(Stable Sort)**이라는 특징이 있습니다.

> 참고: [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)

---

## 병합 정렬의 원리

병합 정렬은 다음과 같은 과정으로 동작합니다:

1. **분할**: 배열을 절반으로 나눔
2. **재귀 정렬**: 나눈 각 부분을 재귀적으로 정렬
3. **병합**: 정렬된 두 부분을 하나의 정렬된 배열로 합침
4. **종료**: 부분 배열의 크기가 1이 되면 정렬 완료

<br>

### 단계별 예시

배열 `[5, 3, 8, 4, 9, 1, 6, 2]`를 정렬하는 과정입니다:

**분할 단계**:
```
[5, 3, 8, 4, 9, 1, 6, 2]
       ↓ 분할
[5, 3, 8, 4]  [9, 1, 6, 2]
    ↓             ↓
[5, 3] [8, 4]  [9, 1] [6, 2]
  ↓      ↓       ↓      ↓
[5][3] [8][4]  [9][1] [6][2]
```

**병합 단계**:
```
[5][3] [8][4]  [9][1] [6][2]
  ↓      ↓       ↓      ↓
[3, 5] [4, 8]  [1, 9] [2, 6]
    ↓             ↓
[3, 4, 5, 8]  [1, 2, 6, 9]
       ↓ 병합
[1, 2, 3, 4, 5, 6, 8, 9]
```

각 단계에서 두 개의 정렬된 배열을 하나로 합치면서 정렬이 완성됩니다.

---

## 병합(Merge) 과정

병합 정렬의 핵심은 두 개의 정렬된 배열을 하나의 정렬된 배열로 합치는 **병합** 과정입니다.

<br>

### 병합 과정 상세

두 개의 정렬된 배열 `[3, 5, 8]`과 `[1, 4, 9]`를 병합하는 과정:

**초기**: 
- 왼쪽 배열: `[3, 5, 8]`, 인덱스 `i = 0`
- 오른쪽 배열: `[1, 4, 9]`, 인덱스 `j = 0`
- 결과 배열: `[]`

**1단계**: `3` vs `1` → `1`이 작음 → `[1]`

**2단계**: `3` vs `4` → `3`이 작음 → `[1, 3]`

**3단계**: `5` vs `4` → `4`가 작음 → `[1, 3, 4]`

**4단계**: `5` vs `9` → `5`가 작음 → `[1, 3, 4, 5]`

**5단계**: `8` vs `9` → `8`이 작음 → `[1, 3, 4, 5, 8]`

**6단계**: 오른쪽 배열 남은 원소 복사 → `[1, 3, 4, 5, 8, 9]`

<br>

각 단계에서 두 배열의 첫 번째 원소를 비교하여 작은 값을 결과 배열에 추가합니다.

한쪽 배열이 모두 소진되면, 남은 배열의 원소들을 순서대로 복사합니다.

<br>

### 병합 함수 구현

```cpp
void merge(vector<int>& arr, int left, int mid, int right) {
  // 임시 배열 생성
  vector<int> temp(right - left + 1);
  
  int i = left;      // 왼쪽 부분의 시작 인덱스
  int j = mid + 1;   // 오른쪽 부분의 시작 인덱스
  int k = 0;         // 임시 배열의 인덱스
  
  // 두 부분을 비교하며 병합
  while (i <= mid && j <= right) {
    if (arr[i] <= arr[j]) {
      temp[k++] = arr[i++];
    } else {
      temp[k++] = arr[j++];
    }
  }
  
  // 왼쪽 부분에 남은 원소 복사
  while (i <= mid) {
    temp[k++] = arr[i++];
  }
  
  // 오른쪽 부분에 남은 원소 복사
  while (j <= right) {
    temp[k++] = arr[j++];
  }
  
  // 임시 배열을 원본 배열로 복사
  for (int idx = 0; idx < temp.size(); idx++) {
    arr[left + idx] = temp[idx];
  }
}
```

<br>

**핵심**:
- `i`, `j`: 각 부분 배열의 현재 위치
- `k`: 결과를 저장할 임시 배열의 위치
- `arr[i] <= arr[j]`: 같은 값일 때 왼쪽을 먼저 선택하여 안정 정렬 보장
- 남은 원소 처리: 한쪽이 먼저 끝나면 다른 쪽의 남은 원소를 모두 복사

---

## 구현

### 기본 구현 (재귀)

```cpp
#include <bits/stdc++.h>
using namespace std;

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
  
  while (i <= mid) {
    temp[k++] = arr[i++];
  }
  
  while (j <= right) {
    temp[k++] = arr[j++];
  }
  
  for (int idx = 0; idx < temp.size(); idx++) {
    arr[left + idx] = temp[idx];
  }
}

void mergeSort(vector<int>& arr, int left, int right) {
  // 기저 조건: 크기가 1 이하면 정렬 완료
  if (left >= right) return;
  
  // 중간 지점 계산
  int mid = left + (right - left) / 2;
  
  // 왼쪽 부분 정렬
  mergeSort(arr, left, mid);
  
  // 오른쪽 부분 정렬
  mergeSort(arr, mid + 1, right);
  
  // 두 부분 병합
  merge(arr, left, mid, right);
}

int main() {
  vector<int> arr = {5, 3, 8, 4, 9, 1, 6, 2, 7};
  
  mergeSort(arr, 0, arr.size() - 1);
  
  for (int x : arr) cout << x << " ";
  cout << "\n";
  
  return 0;
}
```

<br>

**구현 설명**:
1. **분할**: 배열을 중간 지점 `mid`를 기준으로 나눔
2. **재귀**: 왼쪽과 오른쪽 부분을 각각 재귀적으로 정렬
3. **병합**: 정렬된 두 부분을 `merge` 함수로 합침
4. **기저 조건**: `left >= right`이면 크기가 1 이하이므로 정렬 완료

<br>

### 반복 구현 (Bottom-up)

재귀 대신 반복문으로 구현할 수도 있습니다.

```cpp
void mergeSortIterative(vector<int>& arr) {
  int n = arr.size();
  
  // 크기 1, 2, 4, 8, ... 순으로 병합
  for (int size = 1; size < n; size *= 2) {
    // 크기 size인 부분 배열들을 병합
    for (int left = 0; left < n - size; left += 2 * size) {
      int mid = left + size - 1;
      int right = min(left + 2 * size - 1, n - 1);
      
      merge(arr, left, mid, right);
    }
  }
}
```

<br>

**동작 과정**:
- `size = 1`: 크기 1인 부분들을 병합하여 크기 2인 정렬된 부분 생성
- `size = 2`: 크기 2인 부분들을 병합하여 크기 4인 정렬된 부분 생성
- `size = 4`: 크기 4인 부분들을 병합하여 크기 8인 정렬된 부분 생성
- 이 과정을 배열 전체가 정렬될 때까지 반복

<br>

**장점**:
- 재귀 호출 스택을 사용하지 않음
- 스택 오버플로우 걱정 없음
- 재귀보다 약간 빠름

---

## 시간 복잡도

병합 정렬의 시간 복잡도는 모든 경우에 동일합니다.

<br>

### 모든 경우 시간 복잡도: $$O(n \log n)$$

병합 정렬은 최선, 평균, 최악의 경우 모두 $$O(n \log n)$$의 시간 복잡도를 가집니다.

<br>

**분할 과정**: $$O(\log n)$$
- 배열을 절반씩 나누므로 재귀 깊이는 $$\log n$$

**병합 과정**: 각 레벨에서 $$O(n)$$
- 각 레벨에서 모든 원소를 한 번씩 비교하고 복사

**전체**: $$\log n \times O(n) = O(n \log n)$$

<br>

예를 들어, 크기 `8`인 배열의 경우:
```
레벨 0: [8개] - 병합 작업 8번
레벨 1: [4개][4개] - 병합 작업 8번
레벨 2: [2개][2개][2개][2개] - 병합 작업 8번
레벨 3: [1][1][1][1][1][1][1][1] - 병합 작업 8번

총 레벨: log₂8 = 3
총 작업: 3 × 8 = 24번
```

<br>

입력 데이터의 초기 상태와 무관하게 항상 같은 횟수의 비교와 이동을 수행합니다.

<br>

### 공간 복잡도

- **추가 공간**: $$O(n)$$
- 병합 과정에서 임시 배열이 필요
- 재귀 호출 스택: $$O(\log n)$$

<br>

전체 공간 복잡도는 $$O(n)$$이며, 이는 제자리 정렬이 아님을 의미합니다.

> 참고: [제자리 정렬(In-place Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/in-place-sort/)

---

## 병합 정렬의 특징

<br>

### 장점

- **안정적인 성능**: 모든 경우에 $$O(n \log n)$$ 시간 복잡도 보장
- **안정 정렬**: 같은 값을 가진 원소들의 상대적 순서 유지
- **예측 가능**: 입력 데이터와 무관하게 일정한 성능
- **병렬화 가능**: 분할된 부분들을 독립적으로 처리 가능

<br>

### 단점

- **추가 메모리 필요**: $$O(n)$$의 추가 공간이 필요하여 메모리 사용량이 큼
- **작은 데이터에 비효율적**: 오버헤드로 인해 작은 배열에서는 삽입 정렬보다 느릴 수 있음
- **제자리 정렬 불가**: 추가 배열 없이는 구현이 어려움
> 참고: [제자리 정렬(In-place Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/in-place-sort/)

<br>

### 다른 정렬과 비교

| 특성 | 병합 정렬 | 빠른 정렬 | 힙 정렬 |
|------|---------|----------|---------|
| 평균 시간 복잡도 | $$O(n \log n)$$ | $$O(n \log n)$$ | $$O(n \log n)$$ |
| 최악 시간 복잡도 | $$O(n \log n)$$ | $$O(n^2)$$ | $$O(n \log n)$$ |
| 공간 복잡도 | $$O(n)$$ | $$O(\log n)$$ | $$O(1)$$ |
| 안정성 | 안정 | 불안정 | 불안정 |
| 제자리 정렬 | X | O | O |
| 실전 성능 | 빠름 | 가장 빠름 | 보통 |
| 캐시 효율성 | 낮음 | 높음 | 낮음 |

<br>

병합 정렬은 안정 정렬이 필요하거나, 최악의 경우 성능을 보장해야 할 때 유용합니다.

---

## 병합 정렬의 활용

<br>

### 1. 외부 정렬

메모리에 모두 올릴 수 없는 대용량 데이터를 정렬할 때 사용됩니다.

<br>

데이터를 작은 블록으로 나누어 메모리에 올려 정렬한 후, 정렬된 블록들을 병합하는 방식입니다.

병합 과정에서는 두 파일을 앞에서부터 순서대로 읽어가며 병합하므로, 무작위 접근 없이 순차적인 읽기/쓰기만으로 동작합니다.

이러한 순차 접근 특성 덕분에 탐색 시간이 최소화되어 대용량 파일 정렬에 효율적입니다.

<br>

**과정**:
1. 큰 파일을 메모리에 올릴 수 있는 크기의 블록으로 분할
2. 각 블록을 메모리에 로드하여 정렬 후 임시 파일로 저장
3. 정렬된 임시 파일들을 병합하여 최종 정렬 결과 생성

<br>

### 2. 연결 리스트 정렬

연결 리스트는 임의 접근이 불가능하여 빠른 정렬이나 힙 정렬을 적용하기 어렵습니다.

하지만 병합 정렬은 순차 접근만으로도 효율적으로 동작하므로 연결 리스트 정렬에 적합합니다.

```cpp
struct ListNode {
  int val;
  ListNode* next;
  ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* merge(ListNode* l1, ListNode* l2) {
  ListNode dummy(0);
  ListNode* tail = &dummy;
  
  while (l1 && l2) {
    if (l1->val <= l2->val) {
      tail->next = l1;
      l1 = l1->next;
    } else {
      tail->next = l2;
      l2 = l2->next;
    }
    tail = tail->next;
  }
  
  tail->next = l1 ? l1 : l2;
  return dummy.next;
}

ListNode* mergeSort(ListNode* head) {
  if (!head || !head->next) return head;
  
  // 중간 지점 찾기 (slow-fast pointer)
  ListNode* slow = head;
  ListNode* fast = head->next;
  
  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
  }
  
  // 리스트를 두 부분으로 분할
  ListNode* mid = slow->next;
  slow->next = nullptr;
  
  // 재귀적으로 정렬 후 병합
  return merge(mergeSort(head), mergeSort(mid));
}
```

<br>

**장점**: 추가 메모리 없이 $$O(1)$$ 공간 복잡도로 구현 가능

<br>

### 3. 역순 쌍(Inversion) 개수 세기

배열에서 `i < j`이지만 `arr[i] > arr[j]`인 쌍의 개수를 센 수 있습니다.

병합 과정에서 오른쪽 부분의 원소가 선택될 때마다, 왼쪽 부분의 남은 원소 개수만큼 역순 쌍이 존재합니다.

```cpp
long long mergeAndCount(vector<int>& arr, int left, int mid, int right) {
  vector<int> temp(right - left + 1);
  int i = left, j = mid + 1, k = 0;
  long long count = 0;
  
  while (i <= mid && j <= right) {
    if (arr[i] <= arr[j]) {
      temp[k++] = arr[i++];
    } else {
      temp[k++] = arr[j++];
      // 오른쪽 원소가 선택됨 → 왼쪽에 남은 원소 수만큼 역순 쌍
      count += (mid - i + 1);
    }
  }
  
  while (i <= mid) temp[k++] = arr[i++];
  while (j <= right) temp[k++] = arr[j++];
  
  for (int idx = 0; idx < temp.size(); idx++) {
    arr[left + idx] = temp[idx];
  }
  
  return count;
}

long long mergeSortAndCount(vector<int>& arr, int left, int right) {
  if (left >= right) return 0;
  
  int mid = left + (right - left) / 2;
  
  long long count = 0;
  count += mergeSortAndCount(arr, left, mid);
  count += mergeSortAndCount(arr, mid + 1, right);
  count += mergeAndCount(arr, left, mid, right);
  
  return count;
}
```

<br>

**시간 복잡도**: $$O(n \log n)$$ (단순 비교로는 $$O(n^2)$$)

---

## 최적화 기법

<br>

### 1. 작은 배열에 삽입 정렬 사용

배열의 크기가 충분히 작을 때는 삽입 정렬이 더 빠릅니다.

```cpp
void mergeSort(vector<int>& arr, int left, int right) {
  const int THRESHOLD = 10;
  
  // 작은 배열은 삽입 정렬 사용
  if (right - left + 1 <= THRESHOLD) {
    insertionSort(arr, left, right);
    return;
  }
  
  if (left >= right) return;
  
  int mid = left + (right - left) / 2;
  mergeSort(arr, left, mid);
  mergeSort(arr, mid + 1, right);
  merge(arr, left, mid, right);
}
```

<br>

### 2. 병합 생략 최적화

이미 정렬된 부분은 병합을 생략할 수 있습니다.

```cpp
void mergeSort(vector<int>& arr, int left, int right) {
  if (left >= right) return;
  
  int mid = left + (right - left) / 2;
  
  mergeSort(arr, left, mid);
  mergeSort(arr, mid + 1, right);
  
  // 이미 정렬되어 있으면 병합 생략
  if (arr[mid] <= arr[mid + 1]) return;
  
  merge(arr, left, mid, right);
}
```

<br>

**효과**: 거의 정렬된 데이터에서 성능 향상

<br>

### 3. 자연 병합 정렬

입력 데이터의 자연스러운 정렬 구간을 활용하는 방법입니다.

이미 정렬된 부분을 찾아 그 단위로 병합하므로, 거의 정렬된 데이터에서 효율적입니다.

---

## 실전 예제: 두 정렬된 배열 병합

### 문제

두 개의 정렬된 배열을 하나의 정렬된 배열로 병합하는 프로그램을 작성하시오.

- 입력: 정렬된 두 배열 `arr1`, `arr2`
- 출력: 병합된 정렬 배열

<br>

### 접근법

병합 정렬의 병합 과정을 그대로 적용합니다.

두 배열의 원소를 비교하며 작은 값을 결과 배열에 추가하고, 한쪽이 끝나면 나머지를 복사합니다.

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> mergeTwoArrays(vector<int>& arr1, vector<int>& arr2) {
  vector<int> result;
  int i = 0, j = 0;
  
  // 두 배열을 비교하며 병합
  while (i < arr1.size() && j < arr2.size()) {
    if (arr1[i] <= arr2[j]) {
      result.push_back(arr1[i++]);
    } else {
      result.push_back(arr2[j++]);
    }
  }
  
  // 남은 원소 복사
  while (i < arr1.size()) {
    result.push_back(arr1[i++]);
  }
  
  while (j < arr2.size()) {
    result.push_back(arr2[j++]);
  }
  
  return result;
}

int main() {
  vector<int> arr1 = {1, 3, 5, 7};
  vector<int> arr2 = {2, 4, 6, 8};
  
  vector<int> merged = mergeTwoArrays(arr1, arr2);
  
  for (int x : merged) cout << x << " ";
  cout << "\n";
  // 출력: 1 2 3 4 5 6 7 8
  
  return 0;
}
```

<br>

**시간 복잡도**: $$O(n + m)$$ ($$n$$, $$m$$은 각 배열의 크기)

**공간 복잡도**: $$O(n + m)$$

---

## C++ STL의 정렬 함수

C++ 표준 라이브러리의 `std::sort`는 병합 정렬을 직접 사용하지 않고 **인트로 정렬(Introsort)**을 사용합니다.

<br>

하지만 `std::stable_sort`는 안정 정렬이 필요할 때 사용하며, 내부적으로 병합 정렬을 기반으로 구현됩니다.

{% raw %}
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  vector<pair<int, int>> arr = {{3, 1}, {1, 2}, {3, 3}, {1, 4}};
  
  // 안정 정렬: 같은 값의 상대적 순서 유지
  stable_sort(arr.begin(), arr.end(), 
    [](const pair<int, int>& a, const pair<int, int>& b) {
      return a.first < b.first;
    });
  
  for (auto p : arr) {
    cout << "(" << p.first << ", " << p.second << ") ";
  }
  cout << "\n";
  // 출력: (1, 2) (1, 4) (3, 1) (3, 3)
  
  return 0;
}
```
{% endraw %}

<br>

`std::inplace_merge`는 이미 정렬된 두 부분을 병합할 때 사용할 수 있습니다.

```cpp
vector<int> arr = {1, 3, 5, 2, 4, 6};
inplace_merge(arr.begin(), arr.begin() + 3, arr.end());
// 결과: {1, 2, 3, 4, 5, 6}
```

---

## 마무리

병합 정렬은 분할 정복 전략을 활용하는 정렬 알고리듬으로, 모든 경우에 $$O(n \log n)$$의 시간 복잡도를 보장합니다.

<br>

배열을 절반으로 나누어 재귀적으로 정렬한 후, 정렬된 두 부분을 병합하는 방식으로 동작하며, 안정 정렬이라는 중요한 특징을 가집니다.

<br>

추가 메모리가 필요하다는 단점이 있지만, 예측 가능한 성능과 안정성 덕분에 외부 정렬, 연결 리스트 정렬 등 다양한 상황에서 활용됩니다.

특히 `std::stable_sort`의 기반이 되며, 대용량 데이터 처리나 안정 정렬이 필요한 경우에 적합합니다.

<br>

**관련 글**:
- [안정 정렬(Stable Sort)의 개념과 중요성 - soo:bak](https://soo-bak.github.io/algorithm/theory/stable-sort/)
- [빠른 정렬(Quick Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/quick-sort/)
- [힙 정렬(Heap Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/heap-sort/)
- [삽입 정렬(Insertion Sort)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/insertion-sort/)
- [이분 탐색(Binary Search)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/binary-search/)

<br>

**관련 문제**:
- [[백준 2750] 수 정렬하기](https://soo-bak.github.io/algorithm/boj/SortingNumbers-65/)
- [[백준 2751] 수 정렬하기 2](https://soo-bak.github.io/algorithm/boj/SortingNumbers-2-75/)
- [[백준 11931] 수 정렬하기 4](https://soo-bak.github.io/algorithm/boj/sortdesc-44/)

